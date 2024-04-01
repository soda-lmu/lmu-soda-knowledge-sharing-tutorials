"""Simplify authentication with Microsoft Entra ID (Azure).

Developers use their environment variables to determine the log-in workflow they want to use.

Once they have a credential, they get a bearer token for Azure Cognitive Services.

Typical usage example:

    import httpimport
    with httpimport.github_repo(username='malsch', repo='lmu-soda-utils', ref='main'):
        from azure_authentication.customized_azure_login import CredentialFactory

    credential = CredentialFactory().select_credential()
    token_provider = credential.get_login_token_to_azure_cognitive_services()
"""

import json
import os
import os.path
from typing import Callable

from dotenv import load_dotenv
from openai import AzureOpenAI

import azure.identity


class _AzureConnectors:

    def get_login_token_to_azure_cognitive_services(self) -> Callable[[], str]:
        """
        Authenticate with Microsoft Entra ID against Azure Cognitive Services.

        In simple words, this means that you get a personalized token to log in to Azure Cognitive
        Services (e.g. Azure OpenAI)

        :return: A callable that returns a bearer token.
        """
        return azure.identity.get_bearer_token_provider(self, "https://cognitiveservices.azure.com/.default")


class _CustomizedDefaultAzureCredential(azure.identity.DefaultAzureCredential, _AzureConnectors):

    def __init__(self, weblogin):
        """
        The default behavior runs ``DefaultAzureCredential(exclude_interactive_browser_credential=False)``, with
        the authentication chain described at
        https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/identity/azure-identity#defaultazurecredential.

        :param weblogin: Whether to try interactive browser authentication (weblogin='enabled') or not
            (weblogin='disabled') at the end of the authentication chain.
        """

        if weblogin == 'enabled':
            super().__init__(exclude_interactive_browser_credential=False)
        elif weblogin == 'disabled':
            super().__init__(exclude_interactive_browser_credential=True)


class _CustomizedInteractiveBrowserCredential(azure.identity.InteractiveBrowserCredential, _AzureConnectors):
    """Opens a browser to interactively authenticate users.

    We enable persistent token caching with interactive login, see the documentation at
    https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/identity/azure-identity/TOKEN_CACHING.md
    This is not possible with the class _CustomizedDefaultAzureCredential"""

    def __init__(self, allow_unencrypted_storage: bool, credential_path: str):
        self.credential_path = credential_path

        if not credential_path:
            self._create_authentication_record(allow_unencrypted_storage=True)
        else:
            if os.path.exists(self.credential_path):
                self._load_authentication_record_from_disk(allow_unencrypted_storage)
            else:
                self._create_authentication_record(allow_unencrypted_storage=allow_unencrypted_storage)
                self._persist_record_on_disk()

    def _create_authentication_record(self, allow_unencrypted_storage: bool):

        super().__init__(cache_persistence_options=azure.identity.TokenCachePersistenceOptions(
            allow_unencrypted_storage=allow_unencrypted_storage))

    def _persist_record_on_disk(self):
        if self.credential_path:
            record = self.authenticate()
            record_json = record.serialize()
            with open(self.credential_path, 'w') as f:
                json.dump(record_json, f)
        elif not self.credential_path:
            print("""You can persist token caching to reduce the number of logins required. 
                        See details in the documentation on GitHub.""")

    def _load_authentication_record_from_disk(self, allow_unencrypted_storage):

        try:
            with open(self.credential_path, 'r') as f:
                deserialized_record = azure.identity.AuthenticationRecord.deserialize(json.load(f))
                cache_persistence = azure.identity.TokenCachePersistenceOptions(allow_unencrypted_storage=True)
                super().__init__(cache_persistence_options=cache_persistence,
                                 authentication_record=deserialized_record)
        except BaseException:
            # one should not handle exceptions this way
            print("An Exception occurred:" + BaseException.__cause__)
            print("Initiating a new authentication record...")
            self._create_authentication_record(allow_unencrypted_storage=allow_unencrypted_storage)
            self._persist_record_on_disk()


class CredentialFactory:

    def __init__(self,
                 weblogin: str | None = None,
                 credential_path: str | None = None,
                 allow_unencrypted_storage: bool | None = None):
        """
        Create a credential object with CredentialFactory().select_credential()

        :param weblogin: Whether to try interactive browser authentication (weblogin='enabled') or not
            (weblogin='disabled'). Experimental: If you want to set additional parameters to control the authentication
            process, try weblogin='advanced'. Defaults to the value of the environment variable AZURE_SODA_WEBLOGIN. If
             not specified, weblogin='enabled' will be used.
        :param credential_path: (only used if weblogin='advanced'). Example usage: 'path_to_file/azure_credential.json'.
            Define the path and file name where you want to store/persist your AuthenticationRecord in your local
            system (it does not include sensitive information). This enables access across different applications or
            process invocations. If it is not set, the access token is only available during the current process.
            Defaults to the value of the environment variable AZURE_SODA_CREDENTIAL_PATH.
        :param allow_unencrypted_storage: (only used if weblogin='advanced') By default, the cache is encrypted with the
            current platform's user data protection API, and will raise an error when this is not available. To
            configure the cache to fall back to an unencrypted file instead of raising an
            error, specify `allow_unencrypted_storage=True`. Defaults to the value of the environment
            variable AZURE_SODA_ALLOW_UNENCRYPTED_STORAGE.
        """

        if weblogin is None:
            self.weblogin = os.environ.get("AZURE_SODA_WEBLOGIN")
        if self.weblogin is None:
            self.weblogin = "enabled"

        if allow_unencrypted_storage is None:
            self.allow_unencrypted_storage = os.environ.get("AZURE_SODA_ALLOW_UNENCRYPTED_STORAGE")
        if self.allow_unencrypted_storage is None:
            self.allow_unencrypted_storage = False

        if credential_path is None:
            self.credential_path = os.environ.get("AZURE_SODA_CREDENTIAL_PATH")
        if self.credential_path is None:
            self.credential_path = ""
        # other environment variables are handled via the azure-identity package

        # When using UsernamePasswordCredential(), the AZURE_CLIENT_ID parameter is mandatory.
        # We will just use some default client ID based on: https://github.com/Azure/azure-sdk-for-python/issues/19680
        if os.environ.get("AZURE_CLIENT_ID") is None and \
                os.environ.get("AZURE_USERNAME") is not None and os.environ.get("AZURE_PASSWORD") is not None:
            # Default to Xplat Client ID.
            os.environ["AZURE_CLIENT_ID"] = '04b07795-8ddb-461a-bbee-02f9e1bf7b46'

    def select_credential(self) \
            -> _CustomizedDefaultAzureCredential | _CustomizedInteractiveBrowserCredential:
        """
        Select the appropriate Credential class (inherited from ``azure-identity``) to authenticate with Microsoft Azure
        Entra ID. It is best to be controlled with environment variables.

        The default function behavior is based on
        ``DefaultAzureCredential(exclude_interactive_browser_credential=False)``,
        with the authentication workflow described at
        https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/identity/azure-identity#defaultazurecredential.

        :return: some type of AzureCredential
        """

        # Instead of giving control to the user with the login parameter,
        # would it make sense to TRY DefaultAzureCredential first,
        # and try _CustomizedInteractiveBrowserCredential after that?

        if self.weblogin == 'enabled':
            return _CustomizedDefaultAzureCredential(self.weblogin)
        elif self.weblogin == 'disabled':
            return _CustomizedDefaultAzureCredential(self.weblogin)
        elif self.weblogin == 'advanced':
            return _CustomizedInteractiveBrowserCredential(self.allow_unencrypted_storage,
                                                           self.credential_path)


def main():
    """
    This is not a useful application code, but it demonstrates the intended usage of this module.
    """

    load_dotenv()

    # get credentials and access token based on your environment variables
    credential = CredentialFactory().select_credential()
    token_provider = credential.get_login_token_to_azure_cognitive_services()

    # custom Azure OpenAI deployment name
    # -> this function will always throw an error when this is kept.
    DEPLOYMENT_NAME = "<your_deployment_name>"  # "gpt-35-turbo-1106"

    client = AzureOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_REGIONAL_ENDPOINT"],
        api_key=token_provider(),
        api_version="2024-02-01",
    )

    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Does Azure OpenAI support customer managed keys?"},
            {"role": "assistant", "content": "Yes, customer managed keys are supported by Azure OpenAI."},
            {"role": "user", "content": "Do other Azure AI services support this too?"}
        ]
    )

    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()

###########################################################################################
# We used azure.identity, a high-level toolkit for developers above.
# documentation:
# https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/identity/azure-identity
# https://azuresdkdocs.blob.core.windows.net/$web/python/azure-identity/latest/azure.identity.html
#
# For more deliberate user login solutions the library msal would be recommended.
# In the following, we include a brief example from a msal tutorial. This might be useful for debugging or for
# extending the functionality of select_credential() ...
#
# import msal
# import os
#
# app = msal.PublicClientApplication(
#     client_id=os.environ["AZURE_CLIENT_ID"],
#     authority="https://login.microsoftonline.com/" + os.environ["AZURE_TENANT_ID"],
#     )
#
# result = None  # It is just an initial value. Please follow instructions below.
# # possible to implement caching here, see https://learn.microsoft.com/de-de/entra/msal/python/
#
# if not result:
#     # So no suitable token exists in cache. Let's get a new one from Azure AD.
#     result = app.acquire_token_by_username_password(
#         os.environ["AZURE_USERNAME"], os.environ["AZURE_PASSWORD"],
#         scopes=["https://cognitiveservices.azure.com/.default"])
# if "access_token" in result:
#     print(result["access_token"])  # Yay!
# else:
#     print(result.get("error"))
#     print(result.get("error_description"))
#     print(result.get("correlation_id"))  # You may need this when reporting a bug
