# LMU SODA Utilities

Welcome. This repository is intended to share (Python/R) code with colleagues at the [LMU SODA chair](https://www.stat.lmu.de/soda/en/).

The by far most important content in this repository is some example code to help you get started using
certain technologies. Until now, the repository is only about how to access and use Azure OpenAI's models.

### Prerequisites

- Access to use Azure OpenAI Service was granted by your Azure administrator
- Basic knowledge of Python

### Next steps

1. Navigate to the folder [azure-openAI-recipes](./azure-openAI-recipes). This folder
contains illustrative code examples to get started with Azure Open AI. Scan its documentation, you will probably 
look at it more carefully while doing step 2.
2. Run the example code [Chat Completions with Azure OpenAI](./azure-openAI-recipes/soda_starter_code_Azure_OpenAI.py) 
that sits in this folder. By doing so, you will:
   - run a basic recipe that calls the GPT-3.5 Azure OpenAI API from Python using the `openai` package
   - learn how to install the `azure_authentication` package
   - log in manually to Azure OpenAI and learn how you can set environment variables via `.env` files, 
   automating the log-in process

### Bonus materials

#### More recipes

- Another recipe lets you try [Retrieval Augmented Generation (RAG)](./azure-openAI-recipes/soda_starter_code_RetrievalAugmentedGeneration.py) with `llamaIndex`.

#### Python packages

- You can find the `azure_authentication` package in the folder [azure_authentication](./azure_authentication).
It is a very simple Python package that lets us customize the login workflows by using environment variables.

#### Learning nuggets

- There are some random tutorials in the folder [technological-literacy](./technological-literacy).