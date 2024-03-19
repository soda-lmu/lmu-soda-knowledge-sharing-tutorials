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
