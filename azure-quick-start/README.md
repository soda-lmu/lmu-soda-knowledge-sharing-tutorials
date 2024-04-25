## Store your personal credentials to speed up log-in processes

Both examples authorize users with the following two lines of code (for an alternative, 
see the [documentation](../azure_authentication/README.md) of the `azure-authentication` package):

```
credential = select_credential()
token_provider = credential.get_login_token_to_azure_cognitive_services()
```

You probably had to log in via your Web browser to run this code. This can be bothersome if you need to do this
every time when you run a script.

There is a better alternative: Log in automatically by using environment variables. The universal standard:
Store your environment
variables in an `.env`-file. If you haven't heard about `.env ` files before, check out our [very brief introduction 
to `.env` files](../technological-literacy/env-files.md).

We recommend that you configure your own 
authentication workflow to log in with environment variables, as 
described in the [Authentication Workflow Setup](../azure_authentication/AuthenticationWorkflowSetup.md).