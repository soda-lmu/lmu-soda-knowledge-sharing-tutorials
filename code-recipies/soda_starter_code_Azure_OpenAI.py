import os

from dotenv import load_dotenv
from openai import AzureOpenAI

# Option 1: Use httpimport to load 'azure_authentication' package remotely from GitHub without installing it
import httpimport
with httpimport.remote_repo('https://raw.githubusercontent.com/soda-lmu/azure-auth-helper-python/main/src'
                            '/azure_authentication/'):
    from customized_azure_login import CredentialFactory

# Option 2: Install 'azure_authentication' via the pip command, import it afterward:
# pip install "azure_authentication@git+https://github.com/soda-lmu/azure-auth-helper-python.git"
# from azure_authentication.customized_azure_login import CredentialFactory

# Loading environment variables from .env file
load_dotenv()

print("####################################################################")
print("# Hello World example: Azure OpenAI")
print("####################################################################")

# Choose the OpenAI model (in Azure OpenAI: the deployment name) you want to use.
# The deployment needs to be available at the instance set by os.environ["AZURE_OPENAI_ENDPOINT"]
DEPLOYMENT_NAME = "gpt-4o-mini"

print("Authenticate User & Login to Azure Cognitive Services")
# Recommendation: Configure your own authentication workflow with environment variables, see the description at
# https://github.com/soda-lmu/azure-auth-helper-python/blob/main/AuthenticationWorkflowSetup.md
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
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
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
# __RateLimitErrors__: Besides costs (!!!!!!!), rate limits set by administrators and by Azure are
# the main limit we have to consider.
# You may want to execute queries asynchronously (this can save time!). However,
# if you do so you may need to think about RateLimitErrors.
# Without asynchronous execution we would need to execute one query after another,
# such that the next query can only start running after the previous query has been completed.
# The next starter code in the series, 2. soda_starter_code_Asynchronous_Azure_OpenAI.py, demonstrates
# how to run code asynchronously.
