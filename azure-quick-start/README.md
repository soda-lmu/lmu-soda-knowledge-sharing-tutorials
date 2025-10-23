# Introductions to Azure

Please check out our growing list of Azure-related tutorials.

## Track 1: Azure OpenAI

Azure OpenAI Service provides REST API access to OpenAI's powerful models (e.g., GPT-4).

:rocket: Quickstart :rocket:

1. [Getting started using Azure OpenAI](./azure-open-ai-tutorial.md)
2. [Try out different recipies](../code-recipies/)

Administrative

3. Set up new Azure OpenAI instances and models

## Track 2: Working with Docker containers

Containers are portable computing environments. They let you share the app you have developed easily with others. Their deployment in the cloud is simple and cheap.

1. Share your application with a Docker container
    - Example: [Docker image of the R-package "occupationMeasurement"](https://github.com/occupationMeasurement/occupationMeasurement/tree/main/docker), running a shiny app
2. Deploy the Docker container with [Azure container apps](https://learn.microsoft.com/en-us/azure/container-apps/)

**Steps to create an Azure Container App**

1. In [Microsoft Azure Home](https://portal.azure.com/#home) go to "Create a resource".
2. Search for "Container app" and click on "Create".
3. In "Create Container App" set the following:
    - Basics tab:
        1. Select a resource group.
        2. Name your container app.
        3. Select Deployment source "Container image".
        4. Create a new container app environment.
            - Name your environment, e.g., "name-of-your-container-env".
            - Zone redundancy "Disabled"
        5. All other options can stay the same.
           
    - Container tab:
       1. Keep container name.
       2. Image cource: "Docker Hub or other registries".
       3. Image type: "Public".
       4. "Registry login server" and "Image and tag".
          - This can be found in the packages section of the public GitHub repository. Here you will find the *docker pull* command, e.g., "$ docker pull ghcr.io/path".
            Copy ".io" in "Registry login server", e.g., "ghcr.io", and the complete path after "ghcr.io/" in "Image and tag".
          - Select "CPU and memory". This setting can also be changed afterwards in your Container App -> "Application" -> "Containers", if the selected CPU and memory is not sufficient.
          - All other options can stay the same.
            
    - Ingress tab:
      1. Select "Ingress".
      2. Select "Accepting traffic from anywhere".
      3. All other options can stay the same.
     
    - Tags tab:
      Tags can be specified, but don't have to be. See [Tags Documentation](https://learn.microsoft.com/en-gb/azure/azure-resource-manager/management/tag-resources) for more information on tags.
4. After setting all options "Review + Create" gives an overview of all settings.
5. "Create" deploys the container. This can take a few minutes.
6. After deployment is completed, you can acess your container app through "Go to resource" or find it in [Microsoft Azure Home](https://portal.azure.com/#home).
7. The deployed Shiny App can be seen under "Application URL".


## Track 3: Azure Administration & Organization


1. Role-based access control
