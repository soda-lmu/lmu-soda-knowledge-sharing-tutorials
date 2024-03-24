import os

from dotenv import load_dotenv
from openai import AzureOpenAI

# Option 1: Use httpimport to load 'azure_authentication' package remotely from GitHub without installing it
import httpimport
with httpimport.github_repo(username='malsch', repo='lmu-soda-utils', ref='main'):
    from azure_authentication.customized_azure_login import CredentialFactory

# Option 2: Install 'azure_authentication' via the pip command, import it afterward:
# pip install "azure_authentication@git+https://github.com/malsch/lmu-soda-utils.git/#subdirectory=azure_authentication"
# from azure_authentication.customized_azure_login import CredentialFactory

# Loading environment variables from .env file
load_dotenv()

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
credential.get_token("https://cognitiveservices.azure.com/.default")

####################################################################
# Error handling and usage limitations
####################################################################
#
# It may be worth mentioning some error messages and quota limitations:
#
# __APITimeoutErrors__ can have various reasons: network problems, the Azure
# servers are just slow to respond, and the longer your query is, the longer it will take
# Azure OpenAI to respond.
# Good news: You can just increase the time until an  APITimeoutError happens,
# see the [openai-python GitHub page](https://github.com/openai/openai-python?tab=readme-ov-file#handling-errors)
#
# __AuthenticationErrors__ can have many reasons. One piece worth knowing:
# Executing the function token_provider() gives you an access token. Access tokens in Azure expire after approx. 1 hour,
# if they are not refreshed during this time. If you try using the API after the access token expired,
# you will get an authentication error.
#
# __RateLimitErrors__: Besides costs (!!!!!!!), rate limits are the main limit we have to consider.
# Though, I have not seen this error occur in practice.
#
# There exist separate default quotas for each region and each model type.
# For example in France Central the quota for all GTP-3.5-Turbo models we deploy is 240.000 Tokens per Minute (TPM).
# Administrators can decide how the available quota is allocated across different deployments.
# A Requests-Per-Minute (RPM) rate limit will also be enforced whose value is set proportionally
# to the TPM assignment using the following ratio: 6 RPM per 1000 TPM, i.e 6*240 = 1440 RPM are
# following ratio: 6 RPM per 1000 TPM, i.e 6*240 = 1440 RPM are allowed with the aforementioned
# GPT-3.5-Turbo model.

# Background reading:
# Standard deployment model quota: https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models
# More about quotas: https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/quota?tabs=rest#introduction-to-quota
#
# In case you want to carry out millions of API calls in parallel, it is easy to exceed the rate limit. Here is a script
# that optimizes large numbers of parallel requests.
# https://github.com/openai/openai-cookbook/blob/main/examples/api_request_parallel_processor.py
