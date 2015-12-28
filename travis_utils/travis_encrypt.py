from __future__ import unicode_literals

import base64
import click
import requests
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

PUBLIC_KEY_URL = "https://api.travis-ci.org/repos/{account}/{project}/key"


def get_public_key(account, project):
    return requests.get(
        PUBLIC_KEY_URL.format(
            account=account, project=project)).json().get('key')


def get_cipher(public_key):
    key = RSA.importKey(public_key)
    return PKCS1_v1_5.new(key)


def encrypt(cipher, env):
    bytes_env = bytearray(env, 'utf-8')
    return base64.b64encode(cipher.encrypt(bytes_env)).decode('utf-8')


def print_encrypted_env(account, project, envs, verbose=False):
    public_key = get_public_key(account, project)
    cipher = get_cipher(public_key)

    for env in envs:
        print("secure: ! '{}'".format(encrypt(cipher, env)))
        if verbose:
            print(env, "===>", encrypt(cipher, env))


@click.command()
@click.option('--account', '-a')
@click.option('--project', '-p')
@click.option('--envs', '-e', multiple=True)
@click.option('--verbose', '-v', is_flag=True)
def travis_encrypt_cli(account, project, envs, verbose=False):
    """
    :param account: github account name
    :param project: github project
    :param envs: e.g. MY_VAR=VALIE
    :param verbose: default False, print more info
    :return:

    How to use from command line:
    > python travis_encrypt.py -a ACCOUNT -p PROJECT -e VAR=VALUE
    or you can use multiple envs e.g.
    > python travis_encrypt.py -a ACCOUNT -p PROJECT -e VAR=10 -e VAR1=11
    """
    print_encrypted_env(account, project, envs, verbose)


if __name__ == "__main__":
    travis_encrypt_cli()
