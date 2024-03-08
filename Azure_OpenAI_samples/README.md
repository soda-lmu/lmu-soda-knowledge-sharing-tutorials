# Working with Azure OpenAI

We provide two minimal code examples in this directory. They can be used to get started with Azure OpenAI.

**Prerequisites**:

- Access to use Azure OpenAI Service was granted by your administrator
- Appropriate environment variables have been set. Our recommendation: Use an `.env` files to do this (if your are not
`.env `files, see the very brief intro below).

We recommend that you start by running the very basic introduction [Chat Completions with Azure OpenAI](https://github.com/malsch/lmu-soda-utils/blob/main/Basic_Samples/soda_starter_code_Azure_OpenAI.py).
It shows how you can log in and use the GPT-3.5-ChatBot via Azure.

The second example (optional) demonstrates common workflows when using Retrieval Augmented Generation.

|    | Sample                                               | Language | Main Package         | References                                                                                                                                                                                   | 
|----|------------------------------------------------------|----------|----------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1. | Chat Completions with Azure OpenAI                   | Python   | `import openai`      | [Developer Quickstart by OpenAI](https://platform.openai.com/docs/quickstart?context=python), <br/>[Azure OpenAI documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/) |
| 2. | Retrieval Augmented Generation (RAG) with LlamaIndex | Python   | `llama-index` bundle | [LlamaIndex Documentation](https://docs.llamaindex.ai/en/stable/getting_started/installation.html), <br/>[LlamaIndex on GitHub](https://github.com/run-llama/llama_index)                    |

### About personalized login to Azure OpenAI

Both examples authorize users with two lines of code:

```
credential = select_credential()
token_provider = credential.get_login_token_to_azure_cognitive_services()
```

You probably needed to log in via your Web browser to run this code. We recommend that you configure your own 
authentication workflow with environment variables, as 
described at https://github.com/malsch/lmu-soda-utils/tree/main/Azure_Authentication.

If you prefer, you can replace the two lines of code from above with the following:

```
import azure.identity
credential = azure.identity.DefaultAzureCredential(exclude_interactive_browser_credential=False)
token_provider = azure.identity.get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")
```

If you do this, you don't need to import anything from `Azure_Authentication.login_to_azure_cognitive_services`.
Though, authentication workflows that use environment variables starting with `AZURE_SODA_...` won't work
any longer for people using your code.


## A very brief introduction to `.env` files

Your personal _config_ is anything that is likely to vary between different developers. It can be related
to the programs you have up and running on your machine, resource handles to your databases, or your personal 
credentials (like passwords) that only you use.

This config is often stored in `.env` files. It is just a small text document, called `.env`, that lets
your app connect to the OpenAI API. It's content may look like this:

```
USER_NAME=erica.musterfrau
OPENAI_ENDPOINT=<your_endpoint_url>
OPENAI_API_KEY=abc123
```

This is information that is only relevant to run this specific app from your computer. The `.env` file is
typically saved in the root directory of your project.

Here is the pythonic way to load environment variables from an `.env` file:

```
from dotenv import load_dotenv

# Loading environment variables from .env file
load_dotenv()

os.environ["USER_NAME"]             # returns erica.mustermann
os.environ["OPENAI_ENDPOINT"]       # returns <your_endpoint_url>
os.environ["OPENAI_API_KEY"]        # returns abc123
```

Much of your config is personal: You don't want to share it with others, and it would certainly be a bad idea to share
your API_KEY with everyone online on GitHub. It is common practice to add the `.env` file to `.gitignore`, so that
the environment variables are not public.  Keep it secret!

Weblinks:

- [python-dotenv documentation](https://pypi.org/project/python-dotenv/)
- [How To Create And Use .env Files In Python](https://www.geeksforgeeks.org/how-to-create-and-use-env-files-in-python/)
