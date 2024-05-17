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

From the Chat-Playground (see https://oai.azure.com/), you can view a brief Python example code that you might try. Take note of the Azure Endpoint that you would need to connect to. The format is `https://<instance-name>.openai.azure.com/`.

The problem is: At the SODA chair we do not use API keys for Azure. The example code from the playground requires an `api_key = <AZURE_OPENAI_KEY>`, but you don't have one and, thus, cannot execute this code. Instead, you will need to log in with your Azure account to obtain your own private key.

We recommend that you start by running the very basic introduction [1. Chat Completions with Azure OpenAI](../code-recipies/soda_starter_code_Azure_OpenAI.py). It shows how you can log in using your personal account and start chatting with the GPT-3.5-ChatBot via Azure.

> [!TIP]
> Run now the example code :arrow_forward: [Chat Completions with Azure OpenAI](../code-recipies/soda_starter_code_Azure_OpenAI.py). You will:
> - run a basic recipe that calls the GPT-3.5 Azure OpenAI API from Python using the `openai` package
> - learn how to install the `azure_authentication` package
> - log in manually to Azure OpenAI and learn how you can set environment variables via `.env` files, 
>   automating the log-in process

You can then try other models - like different versions of GPT-4 - that are available to you (see `Deployments` at https://oai.azure.com/). Azure OpenAI requires that these `deployments` have been set up by an administrator, implying that all deployments can have custom names. This is a key difference as compared to openAI's offerings (not from Azure): openAI provides a number of ready-made models, with their names being set by openAI.

After running this example recipe, you have everything what you need to access Azure OpenAI. You can continue by checking out additional [code recipies](../code-recipies/) that we provide or look at [OpenAI's API documentation](https://platform.openai.com/docs/introduction) to learn more about openAI's powerful models and how to use them.

### Troubleshooting

Did you encounter any errors when running the example code? Here are a few hints:

- When you executed the function `token_provider()`, an access token was given to you. Access tokens in Azure expire after approx. 1 hour, if they are not refreshed during this time. Writing prompts after the token has expired will result in an `AuthenticationError: Error code: 401`
- API keys and other features, like the uploading of datasets, are disabled for you. Some error messages may appear in https://oai.azure.com/ when you try to use these features anyway. Don't worry, the basic functionality of chatting with openai's chat models will still work. 
    - Please talk to your supervisor/administrator if you need any additional features for your project.
    - Azures help page for [Role-based access control](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/role-based-access-control) describes in detail the permissions and features you can access. The default role you currently have is `Cognitive Services OpenAI User`.

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
    - Search for `Resource groups`. You will find a list of ressource groups that you have access to. There can be multiple ressources in each ressource group, one of them should be the Azure OpenAI service you have found before.

The Azure OpenAI service and other services you have just identified do not belong to you. They are shared ressources that accomodate multiple users. Keep this in mind when we now explore how the Azure OpenAI service is currently being used.

- Open the Azure OpenAI service you have just identified. On the left, you should see a number of tabs: `Overview`, `Activity log`, `Access control (IAM)`, and so on. A couple of them can be helpful for you:
    - Via `Keys and Endpoint` you get to see the Azure endpoint (Format: `https://<instance-name>.openai.azure.com/`) that you use for your queries.
    - Via `Cost analysis` you can explore & analyze how much money all the different API calls to this ressource cost.
    - Via `Metrics` you can explore & analyze by how much and in which ways this ressource was recently being used. This can be a bit confusing. The `Overview` tab is probably more helpful for a first glimpse on current usage.
 
# Monitor usage

Although you won't pay for Azure OpenAI, someone else does, and it can get expensive, especially if you run many long prompts. You should check out current prices:

- [Azure OpenAI prices](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/)

We run this service for small workloads only. If you plan to make <ins>**more than 500 requests to the API within a single month**</ins> (or 10.000 requests if you are using the very fast and cheap GPT-3.5-Turbo model), please talk to your supervisor/administrator first and inform her about the number of API requests and the approximate budget you plan to spend.

How do you know how many resources you used? You should monitor your usage. To do this, there is one more tool that we haven't described yet:

- Open the Azure Portal: https://portal.azure.com/#home and 
    - Search for `Dashboard` or `Dashboard Hub`.
    - You should be able to find a Dashboard called `Openai easyAccess Monitor`.

This dashboard is meant to inform all users who use the same shared instance about their joint recent usage.

### Quotas

Besides cost, there is one additional constraint you may face: Administrators can set quotas separately for each deployment, for example, the quota for GPT-3.5 is set to 100k tokens per minute (TPM). You can check the available quota at https://oai.azure.com/ in the "Deployments" tab. A Requests-Per-Minute (RPM) rate limit will also be enforced, whose value is set proportionally to the TPM assignment using the following ratio: 6 RPM per 1000 TPM; i.e., 6*100 = 600 RPM (or 600/60 = 10 Requests-Per-Second) are allowed with the aforementioned GPT-3.5-Turbo model.

If you are using cheap models, like GPT-3.5, these quotas will most likely not matter in practice for your work. With more expensive models this may be different. Please contact your SODA LMU contact person if the preset quotas impair your productivity.

# Weblinks

- Documentation of the `openai`-Package (Python):
    - https://github.com/openai/openai-python
    - https://platform.openai.com/docs/api-reference/chat/create?lang=python
- [Azure OpenAI pricing](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/#pricing)
- Azure OpenAI documentation:
    - [Intro to Azure OpenAI Service](https://learn.microsoft.com/en-us/training/modules/explore-azure-openai/)
    - [Documentation Overview](https://learn.microsoft.com/en-us/azure/ai-services/openai/)