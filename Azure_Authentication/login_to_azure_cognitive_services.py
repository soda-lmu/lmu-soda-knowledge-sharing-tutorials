import azure.identity
import json
import os.path
from typing import Callable

# %% The simplest way to use azure.identity:
# credential = azure.identity.DefaultAzureCredential(logging_enable=False, exclude_interactive_browser_credential=False)
# token=credential.get_token("https://cognitiveservices.azure.com/.default")
#
# This will try a chain of authentication methods, including:
# 1. using environment variables (ClientSecretCredential () or UsernamePasswordCredential()),
# 2. using the identity currently logged in to the Azure CLI/Azure PowerShell/Azure Developer CLI
# 3. using interactive browser authentication InteractiveBrowserCredential()
#
# The classes and functions implemented in this file still use the same functionality from `azure.identity`. Then,
# why do we need this file?
#
# This file
# - simplifies authentication with Microsoft Entra ID for Azure Cognitive Services for Python beginners.
#   It uses shorter and more expressive function and parameter names, so that using this process becomes a nuisance.
# - is completely configurable with environment variables. This means different people (beginners!) who
#   want/need to set different environment variables can still execute identical code in their respective environments.
# - implements InteractiveBrowserCredential() with **persistent Token caching on disk**
#   (see https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/identity/azure-identity/TOKEN_CACHING.md) as
#   an additional alternative that seems to be impossible when using DefaultAzureCredential()


class DefaultAzureCredentialWithCognitiveServiceLogin(azure.identity.DefaultAzureCredential):

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

    def get_login_token_to_azure_cognitive_services(self) -> Callable[[], str]:
        """
        Authenticate with Microsoft Entra ID against Azure Cognitive Services.

        In simple words, this means that you get a personalized token to log in to Azure Cognitive
        Services (e.g. Azure OpenAI)

        :return: A callable that returns a bearer token.
        """
        return azure.identity.get_bearer_token_provider(self, "https://cognitiveservices.azure.com/.default")


class InteractiveBrowserCredentialWithCognitiveServiceLogin(azure.identity.InteractiveBrowserCredential):
    """Opens a browser to interactively authenticate users.

    We want to enable token caching with interactive login, see the documentation at
    https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/identity/azure-identity/TOKEN_CACHING.md
    This is not possible with the class DefaultAzureCredentialWithCognitiveServiceLogin"""

    def __init__(self, allow_unencrypted_storage: bool, credential_path: str):
        self.credential_path = credential_path

        if not credential_path:
            self.create_authentication_record(allow_unencrypted_storage=True)
        else:
            if os.path.exists(self.credential_path):
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
                    self.create_authentication_record(allow_unencrypted_storage=allow_unencrypted_storage)
                    self.persist_record_on_disk()
            else:
                self.create_authentication_record(allow_unencrypted_storage=allow_unencrypted_storage)
                self.persist_record_on_disk()

    def create_authentication_record(self, allow_unencrypted_storage: bool):

        super().__init__(cache_persistence_options=azure.identity.TokenCachePersistenceOptions(
            allow_unencrypted_storage=allow_unencrypted_storage))

    def persist_record_on_disk(self):
        if self.credential_path:
            record = self.authenticate()
            record_json = record.serialize()
            with open(self.credential_path, 'w') as f:
                json.dump(record_json, f)
        elif not self.credential_path:
            print("""You can persist token caching to reduce the number of logins required. 
                        See details in the documentation on GitHub.""")

    def get_login_token_to_azure_cognitive_services(self)-> Callable[[], str]:
        """
        Authenticate with Microsoft Entra ID against Azure Cognitive Services.

        In simple words, this means that you get a personalized token to log in to Azure Cognitive
        Services (e.g. Azure OpenAI)

        :return: A callable that returns a bearer token.
        """
        return azure.identity.get_bearer_token_provider(self, "https://cognitiveservices.azure.com/.default")


def select_credential(weblogin: str | None = None,
                      credential_path: str | None = None,
                      allow_unencrypted_storage: bool | None = None) \
        -> DefaultAzureCredentialWithCognitiveServiceLogin | InteractiveBrowserCredentialWithCognitiveServiceLogin:
    """
    Select the appropriate Credential class (inherited from ``azure-identity``) to authenticate with Microsoft Azure
    Entra ID. It is best to be controlled with environment variables.

    The default function behavior runs ``DefaultAzureCredential(exclude_interactive_browser_credential=False)``, with
    the authentication workflow described at
    https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/identity/azure-identity#defaultazurecredential.

    :param weblogin: Whether to try interactive browser authentication (weblogin='enabled') or not
        (weblogin='disabled'). Experimental: If you want to set additional parameters to control the authentication
        process, try weblogin='advanced'. Defaults to the value of the environment variable AZURE_SODA_WEBLOGIN. If not
         specified, weblogin='enabled' will be used.
    :param credential_path: (only used if weblogin='advanced'). Example usage: 'path_to_file/azure_credential.json'.
        Define the path and file name where you want to store/persist your AuthenticationRecord in your local
        system (it does not include sensitive information). This enables access across different applications or
        process invocations. If it is not set, the access token is only available during the current process.
        Defaults to the value of the environment variable AZURE_SODA_CREDENTIAL_PATH.
    :param allow_unencrypted_storage: (only used if weblogin='advanced') By default, the cache is encrypted with the
        current platform's user data protection API, and will raise an error when this is not available. To configure
        the cache to fall back to an unencrypted file instead of raising an
        error, specify `allow_unencrypted_storage=True`. Defaults to the value of the environment
        variable AZURE_SODA_ALLOW_UNENCRYPTED_STORAGE.

    :return: some type of AzureCredential
    """

    # Instead of giving control to the user with the login parameter,
    # would it make sense to TRY DefaultAzureCredential first,
    # and try InteractiveBrowserCredentialWithCognitiveServiceLogin after that?

    if weblogin is None:
        weblogin = os.environ.get("AZURE_SODA_WEBLOGIN")
    if weblogin is None:
        weblogin = "enabled"

    if allow_unencrypted_storage is None:
        allow_unencrypted_storage = os.environ.get("AZURE_SODA_ALLOW_UNENCRYPTED_STORAGE")
    if allow_unencrypted_storage is None:
        allow_unencrypted_storage = False

    if credential_path is None:
        credential_path = os.environ.get("AZURE_SODA_CREDENTIAL_PATH")
    if credential_path is None:
        credential_path = ""

    if weblogin == 'enabled':
        return DefaultAzureCredentialWithCognitiveServiceLogin(weblogin)
    elif weblogin == 'disabled':
        return DefaultAzureCredentialWithCognitiveServiceLogin(weblogin)
    elif weblogin == 'advanced':
        return InteractiveBrowserCredentialWithCognitiveServiceLogin(allow_unencrypted_storage, credential_path)


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
