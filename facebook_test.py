from dotenv import load_dotenv
import requests
from utils import get_path
import os, json

dotenv_path = get_path(".env")
load_dotenv(dotenv_path)

fb_token = os.environ.get("USER_TOKEN")
fb_page_id = os.environ.get("USER_ID")

with open("outfile.json", "r") as file:
    jobs = json.load(file)
    
msg = jobs[0].get("content")

fb_post_url = "https://graph.facebook.com/{}/accounts".format(fb_page_id)

payload = {
    'fields': {"name"},
    'access_token': fb_token,
    
}

fb_post = requests.get(fb_post_url, data=payload)
print(fb_post.text)
    

