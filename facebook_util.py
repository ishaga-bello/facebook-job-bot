import requests, os

from dotenv import load_dotenv
from utils import get_path

dotenv_path = get_path(".env")
load_dotenv(dotenv_path)

cli_id = os.environ.get("CLIENT_ID")
cli_secrets = os.environ.get("CLIENT_SECRETS")
p_id = os.environ.get("PAGE_ID")
u_token = os.environ.get("USER_TOKEN")

url = "https://graph.facebook.com/v15.0/{}".format(p_id)
#oauth/access_token"

payload = {
    'fields': 'name,access_token',
    'client_id': cli_id,
    'clien_secret': cli_secrets,
    'access_token': u_token,
    }

page = requests.get(url, data=payload)
print(page.text)
