import requests
import base64
import click
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


@click.command()
@click.option('--account', '-a')
@click.option('--project', '-p')
@click.option('--envs', '-e', multiple=True)
def travis_encrypt_cli(account, project, envs):
    click.echo(account)
    click.echo(project)
    click.echo(envs)

    public_key = get_public_key(account, project)
    cipher = get_cipher(public_key)

    for env in envs:
        print(encrypt(cipher, env))


if __name__ == "__main__":
    travis_encrypt_cli()
