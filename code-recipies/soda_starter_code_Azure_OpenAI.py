import os

from dotenv import load_dotenv
from openai import AzureOpenAI

# Option 1: Use httpimport to load 'azure_authentication' package remotely from GitHub without installing it
import httpimport
with httpimport.remote_repo('https://raw.githubusercontent.com/soda-lmu/azure-auth-helper-python/main/src/azure_authentication/'):
    from customized_azure_login import CredentialFactory

# Option 2: Install 'azure_authentication' via the pip command, import it afterward:
# pip install "azure_authentication@git+https://github.com/soda-lmu/azure-auth-helper-python.git"
# from azure_authentication.customized_azure_login import CredentialFactory

# Loading environment variables from .env file
load_dotenv()

print("####################################################################")
print("# Hello World example: Azure OpenAI")
print("####################################################################")

# Choose the OpenAI model you want to use.
# The model name selected here most match a deployment name from your OpenAI subscription.
# The deployment needs to be available in the region set by os.environ["AZURE_OPENAI_REGIONAL_ENDPOINT"]
DEPLOYMENT_NAME = "gpt-35-turbo-1106"

print("Authenticate User & Login to Azure Cognitive Services")
# Recommendation: Configure your own authentication workflow with environment variables, see the description at
# https://github.com/malsch/lmu-soda-utils/tree/main/azure_authentication/AuthenticationWorkflowSetup.md
credential = CredentialFactory().select_credential()
token_provider = credential.get_login_token_to_azure_cognitive_services()

print("Instantiate Azure OpenAI Client")
# %% Authentication works in various ways:
# We can authenticate in three equivalent ways:
# - pass 'token_provider()' as an argument to 'api_key'
# - pass 'token_provider()' as an argument to 'azure_ad_token'
# - pass 'token_provider' as an argument to 'azure_ad_token_provider'. Note that '()' is missing here.
# For the api_key argument we can either pass an API_KEY or the token_provider() we just created.
client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_REGIONAL_ENDPOINT"],
    api_key=token_provider(),  # alternative: insert os.getenv("AZURE_OPENAI_API_KEY")
    # azure_ad_token=token_provider(),          # same outcome
    # azure_ad_token_provider=token_provider,   # same outcome again
    api_version="2024-02-01",  # or use a preview version (e.g., "2024-03-01-preview") for the latest features.
    # api_version (How-To): https://stackoverflow.com/questions/76475419/how-can-i-select-the-proper-openai-api-version
    timeout=600.0,  # throw APITimeoutError after 10 minutes without a response (default behavior)
)

print("Call to the Azure OpenAI Chat Completions API")
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
print("Success! At this point you will probably want to explore the chat completions reference from openai:")
print("https://platform.openai.com/docs/api-reference/chat")
print("Or you can check out other tutorials. Here is a nice one:")
print("https://microsoft.github.io/generative-ai-for-beginners/#/")

####################################################################
# Error handling and usage limitations
####################################################################
#
# It may be worth mentioning some error messages and quota limitations:
#
# __APITimeoutErrors__ can have various reasons: network problems, the Azure
# servers are just slow to respond, and the longer your query is, the longer it will take
# Azure OpenAI to respond.
# Good news: You can just increase the time until an APITimeoutError happens (set via the timeout parameter),
# see the [openai-python GitHub page](https://github.com/openai/openai-python?tab=readme-ov-file#handling-errors)
#
# __AuthenticationErrors__ can have many reasons. One piece worth knowing:
# Executing the function token_provider() gives you an access token. Access tokens in Azure expire after approx. 1 hour,
# if they are not refreshed during this time. If you try using the API after the access token expired,
# you will get an authentication error.
#
# __RateLimitErrors__: Besides costs (!!!!!!!), rate limits set by Azure are the main limit we have to consider.
# You may want to execute queries asynchronously (this can save time!), but if you do so you may need to think about
# RateLimitErrors (see below).

print("####################################################################")
print("# Getting serious: Asynchronous Code Execution")
print("####################################################################")
# The following code demonstrates a simple design pattern to execute multiple API queries in parallel.
# Without asynchronous execution we would need to execute one query after another,
# such that the next query can only start running after the previous query has been completed.

import asyncio
import time
from openai import AsyncAzureOpenAI

client = AsyncAzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_REGIONAL_ENDPOINT"],
    api_key=token_provider(),
    api_version="2024-02-01",
    timeout=600.0,  # throw APITimeoutError after 10 minutes without a response (default behavior)
)


async def get_capital(country: str, sem: asyncio.Semaphore):
    """
    Query an openAI chat model for the capital of 'country'
    """
    async with sem:
        s = time.perf_counter()
        chat_completion = await client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {"role": "user", "content": "What is the capital of" + country, }
            ]
        )
        elapsed = time.perf_counter() - s
        print(chat_completion.choices[0].message.content)
        print(f"OpenAI query executed in {elapsed:0.2f} seconds.")
        return chat_completion.choices[0].message.content


async def bulk_api_calls():
    """
    Implement basic routine to run bulk API calls in a concurrent way.
    """

    print("Starting asynchronous execution of four API queries")
    countries = ["Poland", "France", "Montenegro", "Nigeria"]

    # Semaphores are a way to throttle the number of API calls, just to avoid RateLimitErrors.
    # It limits the number of concurrent processes (API calls).
    # You can try setting the semaphore to 1, and you will see that all API calls are executed one after another;
    # any gains from asynchronous code execution are thus lost.
    # It's probably best to ignore this part about semaphores on first reading.
    sem = asyncio.Semaphore(24)

    # While we do not know the order in which we receive the results from each API query,
    # they are gathered in a list that is sorted in correspondence with 'countries'
    results = await asyncio.gather(*(get_capital(country, sem) for country in countries))

    return results


s = time.perf_counter()
res = asyncio.run(bulk_api_calls())
elapsed = time.perf_counter() - s
print("~~")
print("Query results are returned in a list:")
print(res)
print(f"All OpenAI queries were executed in {elapsed:0.2f} seconds.")
print("We can see the main advantage of asynchronous execution: ")
print("All queries were executed 'in parallel', meaning that we only need to wait"
      " for the one query that took the longest.")

####################################################################
# More about rate limit errors and usage limitations
####################################################################

# There exist separate default quotas for each region and each model type.
# For example, in France Central the quota for all GTP-3.5-Turbo models we deploy is 240.000 Tokens per Minute (TPM).
# Administrators can decide how the available quota is allocated across different deployments.
# A Requests-Per-Minute (RPM) rate limit will also be enforced, whose value is set proportionally
# to the TPM assignment using the following ratio: 6 RPM per 1000 TPM, i.e 6*240 = 1440 RPM
# (or 1440/60 = 24 Requests-Per-Second) are allowed with the aforementioned GPT-3.5-Turbo model. There may also be
# additional "dynamic quota" if Azure has extra capacity available, meaning that the quotas mentioned before can
# actually be higher in practice.

# If we expect that every API query runs for one second on average (this will depend on your query and the
# model you use), this suggests that we can run 24 API calls in parallel.
# Based on this reasoning we set the semaphore to 24.

# Again, you should probably be more worried about the costs than about these quota usage limitations.

# Background reading:
# Standard deployment model quota: https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models
# More about quotas: https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/quota?tabs=rest#introduction-to-quota
#
# In case you want to carry out millions of API calls in parallel, it is easy to exceed the rate limit. Here is a script
# that optimizes large numbers of parallel requests.
# https://github.com/openai/openai-cookbook/blob/main/examples/api_request_parallel_processor.py
# 
# OpenAI introduced in April 2024 a separate API to run large batches of requests asynchronously at half the cost, see
# https://platform.openai.com/docs/api-reference/batch (as of April 2024, this feature is not available with Azure OpenAI).
