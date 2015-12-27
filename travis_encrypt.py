import requests
import base64
import argparse

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5


PUBLIC_KEY_URL = "https://api.travis-ci.org/repos/{account}/{project}/key"


def get_public_key(account, project):
    return requests.get(
        PUBLIC_KEY_URL.format(
            account=account, project=project)).json().get('key')


def get_cipher(public_key):
    key = RSA.importKey(public_key)
    return PKCS1_v1_5.new(key)


def encrypt(cipher, env):
    return base64.b64encode(cipher.encrypt(str.encode(env)))


if __name__ == "__main__":
    account = "hopsmdev"
    project = "data_fetcher"
    env = "TEST=TEST"
    public_key = get_public_key(account, project)
    print(public_key)
    cipher = get_cipher(public_key)
    print(cipher)
    encrypted = encrypt(cipher, env)
    print(encrypted)
