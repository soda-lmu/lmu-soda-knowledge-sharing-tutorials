# Overview

This folder contains recipies that will help you start and understand certain technologies related to our work.

You want to share some useful educational material? Please do so. You find an error or want to improve the documentation? Please do so! Providing these recipies and keeping them up to date is a group effort. It would be great if this collection grows and improves over time.

## Working with Azure OpenAI

**Prerequisites**:

- Access to use Azure OpenAI Service was granted by your administrator
- You have been given a value for the environment variable `AZURE_OPENAI_ENDPOINT` (probably within the .env file you should have received).

**Related tutorials**:

- [Getting started using Azure Open AI](../azure-quick-start/azure-open-ai-tutorial.md)

If you use Python, we recommend that you start with the tutorial and run the very basic introduction [1. Chat Completions with Azure OpenAI in Python](soda_starter_code_Azure_OpenAI.py). If you use R, essentially the same content is also available in [4. Chat Completions with Azure OpenAI in R](soda_starter_code_AzureOpenAiAuthentication.R).
Both scripts show how you can log in and use the GPT-3.5-ChatBot via Azure.

The second example demonstrates how you can speed up computation by running queries to the API asynchroniously. The third example demonstrates common workflows when using Retrieval Augmented Generation.

|    | Sample                                                                                                    | Language | Main Package                    | References                                                                                                                                                                                   | 
|----|-----------------------------------------------------------------------------------------------------------|----------|---------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1. | [Chat Completions with Azure OpenAI](soda_starter_code_Azure_OpenAI.py)                                   | Python   | `import openai`                 | [Developer Quickstart by OpenAI](https://platform.openai.com/docs/quickstart?context=python), <br/>[Azure OpenAI documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/) |
| 2. | [Asynchronous code execution with Azure OpenAI](soda_starter_code_Asynchronous_Azure_OpenAI.py)           | Python   | `import asyncio`, `import openai` |  |
| 3. | [Retrieval Augmented Generation (RAG) with LlamaIndex](soda_starter_code_RetrievalAugmentedGeneration.py) | Python   | `llama-index` bundle            | [LlamaIndex Documentation](https://docs.llamaindex.ai/en/stable/getting_started/installation.html), <br/>[LlamaIndex on GitHub](https://github.com/run-llama/llama_index)                    |
| 4. | [Chat Completions with Azure OpenAI in R](soda_starter_code_AzureOpenAiAuthentication.R)                    | R  | `httr`, `jsonlite` |  |


## Working with ...

You have any materials you would like to add?