import os
from dotenv import load_dotenv
from openai import AzureOpenAI

print("Loading environment variables from .env file")
load_dotenv()

client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_SODA_FR_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_SODA_FR_KEY"],
    # azure_ad_token_provider=token_provider, # an alternative to using the api_key
    api_version="2023-12-01-preview",
)

response = client.chat.completions.create(
    model=os.environ["AZURE_OPENAI_SODA_DEPLOYMENT_NAME"],  # model = "deployment_name"
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Does Azure OpenAI support customer managed keys?"},
        {"role": "assistant", "content": "Yes, customer managed keys are supported by Azure OpenAI."},
        {"role": "user", "content": "Do other Azure AI services support this too?"}
    ]
)

print(response.choices[0].message.content)