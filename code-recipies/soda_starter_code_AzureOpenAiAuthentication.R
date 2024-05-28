############################################################
#                    Azure OpenAI Integration              #
# This script authenticates with Azure Cognitive Services, #
# calls the OpenAI API to get completions for given        #
# prompts                                                  #
# Author: Caro Haensch                                     #
############################################################

# Load necessary libraries

library(AzureAuth)  # Library for Azure authentication
library(httr)       # Library for HTTP requests
library(readr)      # Library for reading files
library(jsonlite)   # Library for handling JSON data

# Function to load environment variables from a .env file

# The .env could look like this:
# AZURE_TENANT_ID=535d2ee1-225f-4f5a-a773-6de8f7288d12
# AZURE_APP_ID=8932b56d-abd0-4cb3-b67b-e329afec7823
# AZURE_USERNAME=YOURUSERNAME@lmuazure.onmicrosoft.com
# AZURE_PASSWORD=YOURPASSWORD
# AZURE_OPENAI_ENDPOINT=YOURENDPOINT


load_env <- function(file = ".env") {
  env_vars <- read_lines(file)  # Read all lines from the .env file
  for (line in env_vars) {
    if (nzchar(line) && !startsWith(line, "#")) {  # Ignore empty lines and comments
      key_value <- strsplit(line, "=")[[1]]  # Split the line into key and value
      if (length(key_value) == 2) {
        key <- key_value[1]  # Extract the key
        value <- key_value[2]  # Extract the value
        do.call(Sys.setenv, setNames(list(value), key))  # Set the environment variable
      }
    }
  }
}

# Load environment variables from the .env file
load_env()

# Retrieve the environment variables using Sys.getenv()
tenant_id <- Sys.getenv("AZURE_TENANT_ID")
app_id <- Sys.getenv("AZURE_APP_ID")
username <- Sys.getenv("AZURE_USERNAME")
password <- Sys.getenv("AZURE_PASSWORD")
endpoint <- Sys.getenv("AZURE_OPENAI_ENDPOINT")

# Print the retrieved environment variables
cat("Tenant ID:", tenant_id, "\n")
cat("App ID:", app_id, "\n")
cat("Endpoint:", endpoint, "\n")

# Authenticate user & log in to Azure Cognitive Services
# Refresh approximately every hour and a half
token <- get_azure_token(
  resource = "https://cognitiveservices.azure.com/",  # Azure Cognitive Services resource
  tenant = tenant_id,  # Tenant ID from environment variables
  app = app_id,        # Application (client) ID from environment variables
  username= username,  # Username from environment variables
  password = password  # Password from environment variables
)

# Instantiate Azure OpenAI Client
client <- list(
  azure_endpoint = endpoint,               # Azure OpenAI endpoint from environment variables
  api_key = token$credentials$access_token, # Use the token obtained from Azure AD
  api_version = "2024-02-01",              # API version to use
  timeout = 600.0                          # Timeout for API requests (in seconds)
)

# Function to call the OpenAI API
call_openai_api <- function(client, deployment_name, prompt) {
  url <- paste0(client$azure_endpoint, "/openai/deployments/", deployment_name, 
                "/chat/completions?api-version=", client$api_version)
  
  # Print URL for debugging
  cat("URL:", url, "\n")
  
  # Correctly structure the request body
  body <- list(
    messages = list(
      list(role = "user", content = prompt)  # Message from the user
    ),
    max_tokens = 100  # Maximum number of tokens in the response
  )
  
  # Make the POST request to the API
  response <- POST(
    url,
    add_headers(
      Authorization = paste("Bearer", client$api_key),  # Add authorization header
      `Content-Type` = "application/json"  # Specify content type
    ),
    body = toJSON(body, auto_unbox = TRUE),  # Convert body to JSON
    encode = "json"
  )
  
  # Print response for debugging
  cat("Response status:", status_code(response), "\n")
  cat("Response content:", content(response, "text"), "\n")
  
  # Check if the request was successful
  if (status_code(response) == 200) {
    return(fromJSON(content(response, "text"), flatten = TRUE))  # Parse and return the JSON response
  } else {
    stop("API request failed with status: ", status_code(response), "\n", content(response, "text"))  # Handle error
  }
}

# Define the deployment name
DEPLOYMENT_NAME <- "gpt-35-turbo-1106"

# Example usage of the function
response_json <- call_openai_api(client, DEPLOYMENT_NAME, "Hello, how are you?")

# Extract the content element from the response
content_vector <- response_json$choices$message.content

# Print the extracted content
print(content_vector)
