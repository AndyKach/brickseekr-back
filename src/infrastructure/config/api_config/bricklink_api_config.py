import os
import requests
from dotenv import load_dotenv
from requests_oauthlib import OAuth1

load_dotenv()

consumer_key = os.getenv("BRICKLINK_CONSUMER_TOKEN")
consumer_secret = os.getenv("BRICKLINK_CONSUMER_SECRET_TOKEN")
oauth_token = os.getenv("BRICKLINK_OAUTH_TOKEN")
oauth_token_secret = os.getenv("BRICKLINK_OAUTH_SECRET_TOKEN")

bricklink_auth = OAuth1(consumer_key, consumer_secret, oauth_token, oauth_token_secret)
