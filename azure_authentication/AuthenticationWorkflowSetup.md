# Azure Authentication for SODA

## Configure your preferred log-in method

We illustrate the most common authentication workflows here. By adding one of the following code snippets to 
your `.env`-file, you can implement the authentication workflow that works best for you.

### Login with username and password _(recommended)_

Log in with your username and password.

This will throw an error if Two-factor authentication (2FA) is active for your Azure account.

```
## Configure Azure login with username and password
AZURE_CLIENT_ID=<application_client_id> 	    # Ask your adminstrator for the ID of the Microsoft Entra application
AZURE_USERNAME=<your_azure_username>        
AZURE_PASSWORD=<your_azure_password>
```

### Interactive login with the browser _(default behavior, recommended)_

Log in interactively via your Web browser.

This is the default. A browser window will open for you to log in to Azure. This even works if Two-factor 
authentication (2FA) is active. However, this can be very bothersome if log-in is required too often.

You can disable interactive browser login with:

```
AZURE_SODA_WEBLOGIN=disabled
```

### Customized interactive login with the browser

Again, you log in via your browser. However, with customized interactive login your login authentication token is stored on your hard drive.

Why use it?
- Easy setup, and it even works if Two-factor authentication (2FA) is active.
- Compared to the default behavior, you (hopefully) need to authenticate yourself less often via your Web browser.

Security risks:
- Your secret login authentication token for Azure is stored on your hard drive. It is your responsibility to make sure that nobody other than you has access to it.

The implementation here is highly experimental 
and not well tested. The [azure-identity documentation on token caching](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/identity/azure-identity/TOKEN_CACHING.md)
provides further information of what happens behind the scene. 

```
## Configure customized interactive login with the browser
AZURE_SODA_WEBLOGIN=advanced

# Define path & file name where you want to store your AuthenticationRecord (it does not include sensitive information)
AZURE_SODA_CREDENTIAL_PATH=path_to_file/azure_credential.json

# You can set AZURE_SODA_ALLOW_UNENCRYPTED_STORAGE=True if your system does not support token encryption. 
# Be aware of the risk: Without encryption anyone, who has access to your system, can access sensitive information
# and log in to Azure using your identity.
AZURE_SODA_ALLOW_UNENCRYPTED_STORAGE=False 

```

### Login with Azure developer tools (Azure CLI, Azure PowerShell, or Azure Developer CLI)

Install either Azure CLI or Azure PowerShell or Azure Developer CLI. 
You can sign in to Azure from the command line using one of the following commands:

- Azure CLI: `az login`
- Azure PowerShell: `Connect-AzAccount`
- Azure Developer CLI: `azd auth login`

The system will detect automatically that you have signed in. There is no need to add anything to your `.env`-file.

### Service principal with secret

To be used only in exceptional use cases if everything else fails. 
You need to convince your Azure administrator to share the `AZURE_CLIENT_SECRET` with you.

```
# Configure service principal with secret
# This does not require user credentials!!
AZURE_TENANT_ID=<tenant_id>                 # Ask your adminstrator for the ID of the application's Microsoft Entra tenant
AZURE_CLIENT_ID=<application_client_id>     # Ask your adminstrator for the ID of the Microsoft Entra application
AZURE_CLIENT_SECRET=<client_secret>         # Ask your adminstrator for one of the application's client secrets
```

## See also

These procedures make heavy use of the `azure.identity`-package. Go to Azure's [authorization documentation](https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication-overview) 
and its [GitHub page](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/identity/azure-identity) for 
additional details. 
