import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# import httpimport
# with httpimport.github_repo('malsch', 'lmu-soda-utils', ref='main'):
#     from Azure_Authentication.login_to_azure_cognitive_services import select_credential
from Azure_Authentication.login_to_azure_cognitive_services import select_credential

# Loading environment variables from .env file
load_dotenv()

# Choose the OpenAI model you want to use.
# The model name selected here most match a deployment name from your OpenAI subscription.
# The deployment needs to be available in the region set by os.environ["AZURE_OPENAI_REGIONAL_ENDPOINT"]
DEPLOYMENT_NAME = "gpt-35-turbo-1106"

print("Authenticate User & Login to Azure Cognitive Services")
# ToDO variable validation & use .envs 
credential = select_credential(AZURE_WEBLOGIN='enabled', allow_unencrypted_storage=True, credential_path="azure_credential.json")
token_provider = credential.get_login_token_to_azure_cognitive_services()

# The following would be the default way of doing things if login_to_azure_cognitive_services were not available:
# import azure.identity
# credential = azure.identity.DefaultAzureCredential(exclude_interactive_browser_credential=False)
# token_provider = azure.identity.get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")

print("Instantiate Azure OpenAI Client")
# %% Authentication works in various ways:
# For the api_key argument we can either pass an API_KEY or the token_provider() we just created.
# We can even authenticate in three equivalent ways:
# - pass 'token_provider()' as an argument to 'api_key'
# - pass 'token_provider()' as an argument to 'azure_ad_token'
# - pass 'token_provider' as an argument to 'azure_ad_token_provider'
client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_REGIONAL_ENDPOINT"],
    api_key=token_provider(),  # alternative: insert os.environ["AZURE_OPENAI_SODA_FR_KEY"],
    # azure_ad_token=token_provider(),  # same outcome
    # azure_ad_token_provider=token_provider, # same outcome again
    api_version="2023-12-01-preview",
)

print("A simple call to the OpenAI API")
response = client.chat.completions.create(
    model=DEPLOYMENT_NAME,  # model = "deployment_name"
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Does Azure OpenAI support customer managed keys?"},
        {"role": "assistant", "content": "Yes, customer managed keys are supported by Azure OpenAI."},
        {"role": "user", "content": "Do other Azure AI services support this too?"}
    ]
)

print(response.choices[0].message.content)
