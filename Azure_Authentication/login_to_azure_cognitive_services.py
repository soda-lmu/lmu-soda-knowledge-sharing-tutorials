import azure.identity
import json
import os.path

# simplest way to use azure.identity
# cred = azure.identity.DefaultAzureCredential(logging_enable=True)
# token=cred.get_token("https://cognitiveservices.azure.com/.default")

#
#     # try to login by:
#     # 1. using environment variables (ClientSecretCredential () or UsernamePasswordCredential()),
#     # 2. using the identity currently logged in to the Azure CLI/Azure PowerShell/Azure Developer CLI
#     #     (see https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication-local-development-dev-accounts?tabs=azure-cli%2Csign-in-azure-cli)
#     # 3. using interactive browser authentication

def select_credential(AZURE_WEBLOGIN='enabled', allow_unencrypted_storage=False, credential_path=""):
    # Would it make sense to TRY DefaultAzureCredential first,
    # and try InteractiveBrowserCredentialWithCognitiveServiceLogin after that?

    if AZURE_WEBLOGIN == 'enabled':
        return DefaultAzureCredentialWithCognitiveServiceLogin(AZURE_WEBLOGIN)
    elif AZURE_WEBLOGIN == 'disabled':
        return DefaultAzureCredentialWithCognitiveServiceLogin(AZURE_WEBLOGIN)
    elif AZURE_WEBLOGIN == 'advanced':
        return InteractiveBrowserCredentialWithCognitiveServiceLogin(allow_unencrypted_storage, credential_path)


class DefaultAzureCredentialWithCognitiveServiceLogin(azure.identity.DefaultAzureCredential):

    def __init__(self, weblogin):
        if weblogin == 'enabled':
            super().__init__(exclude_interactive_browser_credential=False)
        elif weblogin == 'disabled':
            super().__init__(exclude_interactive_browser_credential=True)

    def get_login_token_to_azure_cognitive_services(self):
        return azure.identity.get_bearer_token_provider(self, "https://cognitiveservices.azure.com/.default")


class InteractiveBrowserCredentialWithCognitiveServiceLogin(azure.identity.InteractiveBrowserCredential):
    """Opens a browser to interactively authenticate users.

    We want to enable token caching with interactive login, see the documentation at
    https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/identity/azure-identity/TOKEN_CACHING.md
    This was not possible with the class DefaultAzureCredentialWithCognitiveServiceLogin"""

    def __init__(self, allow_unencrypted_storage: bool, credential_path: str):
        self.credential_path = credential_path

        if not credential_path:
            self.create_authentication_record(allow_unencrypted_storage=True)
        else:
            if os.path.exists(self.credential_path):
                try:
                    with open(self.credential_path, 'r') as f:
                        deserialized_record = azure.identity.AuthenticationRecord.deserialize(json.load(f))
                        cache_persistence=azure.identity.TokenCachePersistenceOptions(allow_unencrypted_storage=True)
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

    def get_login_token_to_azure_cognitive_services(self):
        return azure.identity.get_bearer_token_provider(self, "https://cognitiveservices.azure.com/.default")


###########################################################################################
# We used azure.identity, a high-level toolkit for developers above.
# documentation:
# https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/identity/azure-identity
# https://azuresdkdocs.blob.core.windows.net/$web/python/azure-identity/latest/azure.identity.html
#
# For more deliberate user login solutions library msal would be recommended.
# The following is a brief example from a msal tutorial. This might be useful for debugging...
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
