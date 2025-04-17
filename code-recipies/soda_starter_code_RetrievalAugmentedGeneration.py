# Implement RAG pipeline using llama.index
# Based on the starter tutorial from https://docs.llamaindex.ai/en/stable/getting_started/starter_example.html
# Examples from https://github.com/run-llama/llama_index/blob/main/docs/examples/ might be better than the documentation

# !pip install llama-index
# !pip install llama_index.llms.azure_openai
# !pip install llama-index-embeddings-azure-openai

# %%

import logging
import os.path
import shutil
import sys
import urllib.request

from dotenv import load_dotenv
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
    Settings
)
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.core.node_parser import SentenceSplitter

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

# Choose the OpenAI Chat and Embedding models you want to use.
# The deployment needs to be available at the instance set by os.environ["AZURE_OPENAI_ENDPOINT"]
LLM_DEPLOYMENT_NAME = "gpt-4o-mini"
EMBEDDING_DEPLOYMENT_NAME = "text-embedding-ada-002"

print("Authenticate User & Login to Azure Cognitive Services")
credential = CredentialFactory().select_credential()
token_provider = credential.get_login_token_to_azure_cognitive_services()

#######################################################
# RAG involves the following high-level steps:
# 1. Retrieve information from your data sources first,
# 2. Add it to your question as context, and
# 3. Ask the LLM to answer based on the enriched prompt.
#
# We now create a temporary directory "tmp", our data source.
# While it could contain thousands of documents, we just add a single document to our data source.
# %%

tmp_dir_name = "tmp"
file_name = "paul_graham_essay.txt"
url = ("https://raw.githubusercontent.com/run-llama/llama_index/main/docs/docs/examples/data/"
       "paul_graham/paul_graham_essay.txt")
os.makedirs(tmp_dir_name, exist_ok=True)

with urllib.request.urlopen(url) as response, open(os.path.join(tmp_dir_name, file_name), 'wb') as out_file:
    shutil.copyfileobj(response, out_file)

# We have now a single file called 'paul_graham_essay.txt' in our temporary directory:
print(os.listdir(tmp_dir_name))

#######################################################
# %% Configuration
# 1. Set up the embedding model that will be used to retrieve information from the data source
# 2. Set up a large language model that will answer our questions.

# Use AzureOpenAI Embeddings with llama.index
embed_model = AzureOpenAIEmbedding(
    model="text-embedding-ada-002",
    deployment_name=EMBEDDING_DEPLOYMENT_NAME,
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    # use_azure_ad=True, # only useful for debugging purposes?
    api_key=token_provider(),
    api_version="2024-02-01"  # or use a preview version (e.g., "2024-03-01-preview") for the latest features.
    # api_version (How-To): https://stackoverflow.com/questions/76475419/how-can-i-select-the-proper-openai-api-version
)
# Alternative: Use HuggingFace Embeddings locally(!!) with llama.index instead of the default embedding-ada-002?
# The following requires on my machine >1.5 GB disk space:
# !pip install llama-index-embeddings-huggingface
# from llama_index.embeddings.huggingface import HuggingFaceEmbedding
# embed_model = HuggingFaceEmbedding(
#     model_name="BAAI/bge-small-en-v1.5"
# )

llm = AzureOpenAI(
    engine=LLM_DEPLOYMENT_NAME, model="gpt-35-turbo-16k", temperature=0.0,
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    # use_azure_ad=True, # only useful for debugging purposes?
    api_key=token_provider(),
    # azure_ad_token=token_provider(),
    # azure_ad_token_provider=token_provider,
    api_version="2024-02-01",
    max_retries=3, timeout=60.0  # llama.index default is to time out after only 60 seconds and throw an APITimeoutError
    # better handling of timeouts is possible with a httpx client
)

# make these models the default to be used by llamaIndex
Settings.llm = llm
Settings.embed_model = embed_model

# add logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)  # logging.DEBUG for more verbose output
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

######################################################
# %% A basic RAG pipeline

# The simplest way to load the data in tmp_dir_name and build an index goes as follows:
#
# documents = SimpleDirectoryReader(tmp_dir_name).load_data()
# index = VectorStoreIndex.from_documents(documents)

# By default, the index is stored in memory as a series of vector embeddings.
# You can save time (and requests to OpenAI) by saving the embeddings to disk.
# Only if the embedding index in PERSIST_DIR does not exist yet, we will need to create it.

# check if storage already exists
PERSIST_DIR = "./storage"
if not os.path.exists(PERSIST_DIR):
    # load the documents and create the index
    documents = SimpleDirectoryReader(tmp_dir_name).load_data()
    index = VectorStoreIndex.from_documents(
        # Note that we split the documents in chunks of length 512 here
        # that means we will create one embedding for each chunk
        documents, transformations=[SentenceSplitter(chunk_size=512)]
    )
    # store it for later
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    # load the existing index
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

# %%
# Now let's do the fun part:
# Create an engine for Q&A over your index and ask a simple question
#
# You should get back a response similar to the following:
# "The author wrote short stories and tried to program on an IBM 1401."

query_engine = index.as_query_engine()
response = query_engine.query("What did the author do growing up?")
print(response)

# %%
# You may want to clean up your working directory:
shutil.rmtree(PERSIST_DIR)
shutil.rmtree(tmp_dir_name)
