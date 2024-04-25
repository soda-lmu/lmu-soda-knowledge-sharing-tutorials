# Overview

This folder contains recipies that will help you start and understand certain technologies related to our work.

You want to share some useful educational material? Please do so. You find an error or want to improve the documentation? Please do so! Providing these recipies and keeping them up to date is a group effort. It would be great if this collection grows and improves over time.

## Working with Azure OpenAI

**Prerequisites**:

- Access to use Azure OpenAI Service was granted by your administrator
- You have been given a value for the environment variable `AZURE_OPENAI_REGIONAL_ENDPOINT` (probably within the .env file you should have received).

We recommend that you start by running the very basic introduction [1. Chat Completions with Azure OpenAI](soda_starter_code_Azure_OpenAI.py).
It shows how you can log in and use the GPT-3.5-ChatBot via Azure.

The second example demonstrates common workflows when using Retrieval Augmented Generation.

|    | Sample                                                                                                    | Language | Main Package         | References                                                                                                                                                                                   | 
|----|-----------------------------------------------------------------------------------------------------------|----------|----------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1. | [Chat Completions with Azure OpenAI](soda_starter_code_Azure_OpenAI.py)                                   | Python   | `import openai`      | [Developer Quickstart by OpenAI](https://platform.openai.com/docs/quickstart?context=python), <br/>[Azure OpenAI documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/) |
| 2. | [Retrieval Augmented Generation (RAG) with LlamaIndex](soda_starter_code_RetrievalAugmentedGeneration.py) | Python   | `llama-index` bundle | [LlamaIndex Documentation](https://docs.llamaindex.ai/en/stable/getting_started/installation.html), <br/>[LlamaIndex on GitHub](https://github.com/run-llama/llama_index)                    |


## Working with ...

You have any materials you would like to add?