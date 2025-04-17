print("####################################################################")
print("# Getting serious: Asynchronous Code Execution")
print("####################################################################")
# The following code demonstrates a simple design pattern to execute multiple API queries in parallel.
# Without asynchronous execution we would need to execute one query after another,
# such that the next query can only start running after the previous query has been completed.

import asyncio
import os
import time

from dotenv import load_dotenv
from openai import AsyncAzureOpenAI

import httpimport
with httpimport.remote_repo('https://raw.githubusercontent.com/soda-lmu/azure-auth-helper-python/main/src'
                            '/azure_authentication/'):
    from customized_azure_login import CredentialFactory

# Option 2: Install 'azure_authentication' via the pip command, import it afterward:
# pip install "azure_authentication@git+https://github.com/soda-lmu/azure-auth-helper-python.git"
# from azure_authentication.customized_azure_login import CredentialFactory

# Loading environment variables from .env file
load_dotenv()

print("Authenticate User & Login to Azure Cognitive Services")
credential = CredentialFactory().select_credential()
token_provider = credential.get_login_token_to_azure_cognitive_services()

# Choose the OpenAI model (in Azure OpenAI: the deployment name) you want to use.
# The deployment needs to be available at the instance set by os.environ["AZURE_OPENAI_ENDPOINT"]
DEPLOYMENT_NAME = "gpt-4o-mini"


print("Setup completed. Lets get started ...")
# When a function definition starts with the keyword 'async def', the function is what is called a coroutine.
# Don't worry, the function code will be executed just like it would be with a standard function. There is only one
# key difference. Inside coroutines, and only inside coroutines, you can use the keyword 'await'. Whenever Python
# encounters an await expression, the coroutine will pause and suspend execution of the current coroutine until the
# results are in. In this way, Python can make a series of API requests without having to wait for the
# result from the previous request to come in. API requests then run in parallel on a different computer. The
# results from each API query are later bundled together in a list.

client = AsyncAzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
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

    # It's probably best to ignore this part about semaphores on first reading.
    # Semaphores are a way to throttle the number of API calls, just to avoid RateLimitErrors.
    # It limits the number of concurrent processes (API calls).
    # You can try setting the semaphore to 1, and you will see that all API calls are executed one after another;
    # any gains from asynchronous code execution are thus lost.
    sem = asyncio.Semaphore(10)

    # asyncio.gather calls the coroutine get_capital() separately for each country in countries.
    # While we do not know the order in which we receive the results from each API query,
    # they are gathered in a list that is sorted in correspondence with 'countries'
    results = await asyncio.gather(*(get_capital(country, sem) for country in countries))

    return results


s = time.perf_counter()
# Start asynchronous execution code block with asyncio.run
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
# For example, in Sweden Central the quota for all GPT-3.5-Turbo models we deploy is 300.000 Tokens per Minute (TPM).
# Administrators can decide how the available quota is allocated across different deployments; the instance we use here
# has 100.000 Tokens per minute for its GPT-3.5-Turbo allocated to it.

# A Requests-Per-Minute (RPM) rate limit will also be enforced, whose value is set proportionally
# to the TPM assignment using the following ratio: 6 RPM per 1000 TPM, i.e 6*100 = 600 RPM
# (or 600/60 = 10 Requests-Per-Second) are allowed with the aforementioned GPT-3.5-Turbo model. There may also be
# additional "dynamic quota" if Azure has extra capacity available, meaning that the quotas mentioned before can
# actually be higher in practice.

# If we expect that every API query runs for one second on average (this will depend on your query and the
# model you use), this suggests that we can run 10 API calls in parallel.
# Based on this reasoning we set the semaphore to 10.

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
