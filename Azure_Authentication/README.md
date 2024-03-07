# Azure Authentication for SODA

### Configurate your log-in method

We illustrate the most common authentication methods here. You can configure any one of the following via your `.env`-file

#### Login with username and password

This will throw an error if Two-factor authentication (2FA) is active for your Azure account.

```
AZURE_CLIENT_ID 	ID of a Microsoft Entra application
AZURE_USERNAME 	a username (usually an email address)
AZURE_PASSWORD 	that user's password
```

#### Interactive login with the browser

This is the default. A browser window will open for you to log-in to Azure. This even works if Two-factor 
authentication (2FA) is active. However, this can be very bothersome if log-in is required too often.

You can disable interactive browser login with:

```
AZURE_WEBLOGIN=disabled
```

#### Login with Azure developer tools (Azure CLI, Azure PowerShell, or Azure Developer CLI)

Install either Azure CLI or Azure PowerShell or Azure Developer CLI. 
You can sign-in to Azure from the command line using one of the following commands:

- Azure CLI: `az login`
- Azure PowerShell: `Connect-AzAccount`
- Azure Developer CLI: `azd auth login`

The system will detect automatically that you have signed in. There is no need to add anything to your `.env`-file.

#### Customized interactive login with the browser

You log-in via your browser. In this customized method your login token is handled in a different way.
This can hopefully reduce the number of log-ins needed. This implementation is highly experimental and not well tested.

```
AZURE_WEBLOGIN=advanced
allow_unencrypted_storage
credential_path
```

#### Service principal with secret

To be used only in exceptional use cases if everything else fails. 
You need to convince your Azure administrator to share the `AZURE_CLIENT_SECRET` with you.

```
AZURE_CLIENT_ID 	ID of a Microsoft Entra application
AZURE_TENANT_ID 	ID of the application's Microsoft Entra tenant
AZURE_CLIENT_SECRET 	one of the application's client secrets
```

### See also

These procedures make heavy use of the `azure.identity`-package. Go to Azure's [authorization documentation](https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication-overview) for additional details. 