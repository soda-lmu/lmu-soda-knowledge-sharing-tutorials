# What is this?

You may need to log in to Microsoft Entra ID to use services like Azure OpenAI. The basic tutorial 
[Chat Completions with Azure OpenAI](../Azure_OpenAI_samples/soda_starter_code_Azure_OpenAI.py) and the
[RAG example with LlamaIndex](../Azure_OpenAI_samples/soda_starter_code_RetrievalAugmentedGeneration.py)
are two examples where your app needs to log in.

[customized_azure_login.py](src/azure_authentication/customized_azure_login.py) supports the login process. Different users 
automatically take different routes to log in, based on the environment variables they have set. We want to make it 
for every user as simple as possible to log in. Users can set their environment variables as described in 
[AuthenticationWorkflowSetup.md](AuthenticationWorkflowSetup.md).

The following code snippet shows how [customized_azure_login.py](src/azure_authentication/customized_azure_login.py)
is used to meet different user login requirements.

```
import httpimport
with httpimport.github_repo('malsch', 'lmu-soda-utils', ref='main'):
    from Azure_Authentication.login_to_azure_cognitive_services import select_credential

credential = select_credential()
token_provider = credential.get_login_token_to_azure_cognitive_services()
```

1. `select_credential()` selects the appropriate Credential class (inherited from `azure-identity`) to authenticate 
with Microsoft Azure Entra ID. It is best to be controlled by the user with environment variables.
2. `get_login_token_to_azure_cognitive_services()` returns your personal access token use Azure 
Cognitive Services (e.g. Azure OpenAI)

[customized_azure_login.py](src/azure_authentication/customized_azure_login.py)  is essentially a wrapper around a few
functions from `azure-identity`. If you prefer, you can replace the code from above with:

```
import azure.identity
credential = azure.identity.DefaultAzureCredential(exclude_interactive_browser_credential=False)
token_provider = azure.identity.get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")
```

or with

```
import azure.identity
credential = azure.identity.DefaultAzureCredential(exclude_interactive_browser_credential=False, logging_enable=False)
token=credential.get_token("https://cognitiveservices.azure.com/.default")
```

If you do this, you don't need to import the function `select_credential()` or anything else 
from `Azure_Authentication.customized_azure_login`.

`azure.identity.DefaultAzureCredential()` 
will try a chain of authentication methods, including:
1. using environment variables (`ClientSecretCredential()` or `UsernamePasswordCredential()`),
2. using the identity currently logged in with `Azure CLI`/`Azure PowerShell`/`Azure Developer CLI`
3. using interactive browser authentication with `InteractiveBrowserCredential()`

## What is the added value of [customized_azure_login.py](src/azure_authentication/customized_azure_login.py)?

[customized_azure_login.py](src/azure_authentication/customized_azure_login.py) calls 
`azure.identity.DefaultAzureCredential()` and inherits the full functionality of this class.

The added value compared to just using `azure.identity.DefaultAzureCredential()` is twofold:

1. In addition, [customized_azure_login.py](src/azure_authentication/customized_azure_login.py) supports
`azure.identity.InteractiveBrowserCredential()` (Interactive login via the browser)
with **persistent token caching on disk** (see [here](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/identity/azure-identity/TOKEN_CACHING.md)) 
if a user sets the environment variable `AZURE_SODA_WEBLOGIN=advanced`. 

This, and any future customizations, should improve the ease of use of the login process.

All customizations are controlled through environment variables that start with `AZURE_SODA_...`.

2. Moreover, the first code chunk above is shorter than the later ones based on 
`azure.identity.DefaultAzureCredential()`. It doesn't distract with superfluous details,
which is relevant, in particular, if beginners try to use this code.
