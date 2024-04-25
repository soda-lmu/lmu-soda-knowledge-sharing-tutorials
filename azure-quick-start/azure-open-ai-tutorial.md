# Getting started using Azure Open AI

Welcome! You have been given an account from the SODA chair to use Azure OpenAI and wonder what is next? Here is a very brief introduction.

**Prerequisites**

- Access to use Azure OpenAI Service was granted by your Azure administrator
- Recommended: Basic knowledge of Python

**Check out the following links**

- Azure Portal: https://portal.azure.com/#home to complete your registration.
    - If you want to manage your personal account, go to: https://myaccount.microsoft.com/
- Azure OpenAI Studio: https://oai.azure.com/
    - Go to the Chat-Playground and start chatting with an OpenAI model.
    - Go to `Deployments` (=`Bereitstellungen`) to find all the different models you can use.

# Using Azure OpenAI with Python

> *Try the example script: [1. Chat Completions with Azure OpenAI](../code-recipies/soda_starter_code_Azure_OpenAI.py)*

From the Chat-Playground (see https://oai.azure.com/), you can view a brief Python example code that yould be tried to run the prompt you have entered. Take note of the Azure Endpoint that you would need to connect to. The format is `https://<instance-name>.openai.azure.com/`.

The problem is: At the SODA chair we do not use API keys for Azure. The example code from the playground requires an `api_key = <AZURE_OPENAI_KEY>`, but you don't have one and, thus, you cannot execute this code. Instead, you will need to log in with your Azure account to obtain your own private key.

We recommend that you start by running the very basic introduction [1. Chat Completions with Azure OpenAI](../code-recipies/soda_starter_code_Azure_OpenAI.py). It shows how you can log in using your personal account and start chatting with the GPT-3.5-ChatBot via Azure.

You can then try other models - like different versions of GPT-4 - that are available to you (see `Deployments` at https://oai.azure.com/). Azure OpenAI requires that these `deployments` have been set up by an administrator, implying that all deployments can have custom names. This is a key difference as compared to openAI's offerings (not from Azure): openAI provides a number of ready-made models, with their names being set by openAI.

After running this example recipe, you have everything what you need to access Azure OpenAI. You can continue by checking out additional [code recepies](../code-recipies/) that we provide or look at [OpenAI's API documentation](https://platform.openai.com/docs/introduction) to learn more about openAI's powerful models and how to use them.


## Store your personal credentials to speed up log-in processes

> *Become more efficient by using soda-lmu's [azure_authentication](https://github.com/soda-lmu/azure-auth-helper-python) package.*

In the example you were authorized to use Azure OpenAI with the following three lines of code (for an alternative, 
see the [documentation](https://github.com/soda-lmu/azure-auth-helper-python) of soda-lmu's `azure_authentication` package):

```
credential = select_credential()
token_provider = credential.get_login_token_to_azure_cognitive_services()
api_key = token_provider()
```

This `api_key` stays valid for only one hour. You probably had to log in via your Web browser to run this code, and after one hour you may need to log in again. This can be bothersome if you need to do this
every time when you run a script.

There is a better alternative: Log in automatically by using environment variables. The universal standard:
Store your environment variables in an `.env`-file. If you haven't heard about `.env ` files before, check out our [very brief introduction to `.env` files](../technological-literacy/env-files.md).

We recommend that you configure your own 
authentication workflow to log in with environment variables, as 
described in the [Authentication Workflow setup](https://github.com/soda-lmu/azure-auth-helper-python/blob/main/AuthenticationWorkflowSetup.md) of soda-lmu's `azure_authentication` package).

# Understand the setup

It may help to point to a couple of resources in the Azure portal. 

- Open the Azure Portal: https://portal.azure.com/#home
    - Search for `Azure OpenAI`. You should see at least one Azure OpenAI service running.
    - Search for `resource groups` \ `Ressourcengruppen`. You will find a list of ressource groups that you have access to. There can be multiple ressources in each ressource group, one of them should be the Azure OpenAI service you have found before.
- Open the Azure OpenAI service you have just identified.




# Monitor usage

Although you won't pay for Azure OpenAI, someone else does, and it can get expensive if you run many long prompts. You should check out current prices:

- [Azure OpenAI prices](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/)

How do you know how many resources you used? You should monitor your usage.



# Weblinks

- Documentation for the OpenAI-Python-Package is available at https://platform.openai.com/docs/api-reference/chat/create?lang=python 