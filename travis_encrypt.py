import requests

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

PUBLIC_KEY_URL = "https://api.travis-ci.org/repos/{account}/{project}/key"


def get_public_key(account, project):
    return requests.get(
        PUBLIC_KEY_URL.format(account=account, project=project)).text

