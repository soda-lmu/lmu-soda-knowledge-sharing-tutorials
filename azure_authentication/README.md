# Installation

Option 1: Install the latest development version directly from GitHub.
```
pip install "azure_authentication@git+https://github.com/malsch/lmu-soda-utils.git/#subdirectory=azure_authentication"
```

Option 2: Use `httpimport` to load the module `azure_authentication.customized_azure_login` remotely 
from GitHub without installing it.
```
import httpimport
with httpimport.github_repo(username='malsch', repo='lmu-soda-utils', ref='main'):
    from azure_authentication.customized_azure_login import CredentialFactory
```

# Usage

You may need to log in to Microsoft Entra ID to use services like Azure OpenAI. The basic tutorial 
[Chat Completions with Azure OpenAI](../azure-openAI-recipes/soda_starter_code_Azure_OpenAI.py) and the
[RAG example with LlamaIndex](../azure-openAI-recipes/soda_starter_code_RetrievalAugmentedGeneration.py)
are two examples where your app needs to log in.

The `azure_authentication` package supports the login process. Different users 
automatically take different routes to log in, depending on the environment variables they have set. We want to make it 
for every user as simple as possible to log in. Users can set their environment variables as described in the
[Authentication Workflow Setup](AuthenticationWorkflowSetup.md).

The following code snippet shows (all) the functionality that this package currently provides.

```
from azure_authentication.customized_azure_login import CredentialFactory

credential = CredentialFactory().select_credential()
token_provider = credential.get_login_token_to_azure_cognitive_services()
```

1. `CredentialFactory().select_credential()` selects the appropriate Credential class (inherited from `azure-identity`) to authenticate 
with Microsoft Azure Entra ID. It is best to be controlled by the user with environment variables.
2. `get_login_token_to_azure_cognitive_services()` returns a user's personal access token. It can
be used later to access Azure Cognitive Services (e.g. Azure OpenAI).

Environment variables should control what exactly happens when the function `select_credential()` is called.
Environment variables that are specific to this package start with `AZURE_SODA_...`, see the [Authentication Workflow Setup](AuthenticationWorkflowSetup.md)

# Alternatives

The package is essentially a wrapper around a few
functions from the [Azure Identity library](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/identity/azure-identity). If you prefer, you can replace the code from above with:

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

If you do this, you don't need to import the `azure_authentication` package.

`azure.identity.DefaultAzureCredential()` 
will try a chain of authentication methods, including:
1. using environment variables (`ClientSecretCredential()` or `UsernamePasswordCredential()`),
2. using the identity currently logged in with `Azure CLI`/`Azure PowerShell`/`Azure Developer CLI`
3. using interactive browser authentication with `InteractiveBrowserCredential()`

More complex log-in workflows could be programmed using the [Microsoft Authentication Library (MSAL)](https://github.com/AzureAD/microsoft-authentication-library-for-python).

## What is the added value of the `azure_authentication` package?

By default, the `azure_authentication` package calls 
`azure.identity.DefaultAzureCredential()` and inherits the full functionality of this class.

The added value compared to just using `azure.identity.DefaultAzureCredential()` is twofold:

1. In addition, the package supports
`azure.identity.InteractiveBrowserCredential()` (Interactive login via the browser)
with **persistent token caching on disk** (see [here](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/identity/azure-identity/TOKEN_CACHING.md)) 
if a user sets the environment variable `AZURE_SODA_WEBLOGIN=advanced`. This feature can be super helpful for users who have Two-Factor authentication enabled.
This, and any future customizations, hopefully make the login process less burdensome. Two developers can use exactly
the same code, even if on one machine `azure.identity.DefaultAzureCredential()` is called and at a different machine 
`azure.identity.InteractiveBrowserCredential()`.

3. Moreover, the first code chunk above is shorter than alternative ones based on 
`import azure.identity`. Parameters have default values that are more appropriate in an educational context.
It doesn't distract with superfluous details, which is relevant, in particular, if beginners try to use your code.
