## A very brief introduction to `.env` files

Your personal _config_ is anything that is likely to vary between different developers. It can be related
to the programs you have up and running on your machine, resource handles to your databases, or your personal 
credentials (like passwords) that only you use. Because it is personal, it describes _your_ environment, using
_environment variables_.

Environment variables are often stored in simple text file, called `.env`. 

Here is such a small text document, called `.env`. Here is an example what its content may look like:

```
USER_NAME=erica.musterfrau
API_ENDPOINT=<your_endpoint_url>
API_KEY=abc123
```

The environment variables stored here let you connect to an API.

This is information that is only relevant to run this specific app from your computer. The `.env` file is
typically saved in the root directory of your project.

Here is the pythonic way to load environment variables from an `.env` file:

```
from dotenv import load_dotenv

# Loading environment variables from .env file
load_dotenv()

os.environ["USER_NAME"]         # returns erica.mustermann
os.environ["API_ENDPOINT"]      # returns <your_endpoint_url>
os.environ["API_KEY"]           # returns abc123
```

Much of your config is personal: You don't want to share it with others, and it would certainly be a bad idea to share
your API_KEY with everyone online on GitHub. It is common practice to add the `.env` file to `.gitignore`, so that
the environment variables are not public.  Keep it secret!

Weblinks:

- [python-dotenv documentation](https://pypi.org/project/python-dotenv/)
- [How To Create And Use .env Files In Python](https://www.geeksforgeeks.org/how-to-create-and-use-env-files-in-python/)
