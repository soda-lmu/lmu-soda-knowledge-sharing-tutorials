# Working with Azure OpenAI

We provide two minimal code examples in this directory. They can be used to get started with Azure OpenAI.

**Prerequisites**:

- Access to use Azure OpenAI Service was granted by your administrator

We recommend that you start by running the very basic introduction [1. Chat Completions with Azure OpenAI](soda_starter_code_Azure_OpenAI.py).
It shows how you can log in and use the GPT-3.5-ChatBot via Azure.

The second example (optional) demonstrates common workflows when using Retrieval Augmented Generation.

|    | Sample                                                                                                    | Language | Main Package         | References                                                                                                                                                                                   | 
|----|-----------------------------------------------------------------------------------------------------------|----------|----------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1. | [Chat Completions with Azure OpenAI](soda_starter_code_Azure_OpenAI.py)                                   | Python   | `import openai`      | [Developer Quickstart by OpenAI](https://platform.openai.com/docs/quickstart?context=python), <br/>[Azure OpenAI documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/) |
| 2. | [Retrieval Augmented Generation (RAG) with LlamaIndex](soda_starter_code_RetrievalAugmentedGeneration.py) | Python   | `llama-index` bundle | [LlamaIndex Documentation](https://docs.llamaindex.ai/en/stable/getting_started/installation.html), <br/>[LlamaIndex on GitHub](https://github.com/run-llama/llama_index)                    |

### Store your personal credentials to speed up log-in processes

Both examples authorize users with the following two lines of code (for an alternative, 
see [the documentation of the `azure-authentication` package](../azure_authentication/README.md)):

```
credential = select_credential()
token_provider = credential.get_login_token_to_azure_cognitive_services()
```

You probably needed to log in via your Web browser to run this code. This can be bothersome if you need to do this
every time when you run a script.

There is a better alternative: Log in automatically by using environment variables. The universal standard:
Store your environment
variables in an `.env`-file. If you haven't heard about `.env ` files before, check out our [very brief introduction 
to `.env` files](../technological-literacy/env-files.md).

We recommend that you configure your own 
authentication workflow to log in with environment variables, as 
described in the [Authentication Workflow Setup](../azure_authentication/AuthenticationWorkflowSetup.md).