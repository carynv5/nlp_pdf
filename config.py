import os
import sys
import logging
from datetime import datetime
from dotenv import load_dotenv

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

load_dotenv()

class AzureConfig:
    KEY_VAULT_NAME = os.environ.get("KEY_VAULT_NAME")
    KV_URI = f"https://{KEY_VAULT_NAME}.vault.azure.net" if KEY_VAULT_NAME else None
    _secret_client = None

    @classmethod
    def get_secret_client(cls):
        if cls._secret_client is None:
            if not cls.KV_URI:
                raise ValueError("KEY_VAULT_NAME environment variable is not set")
            credential = DefaultAzureCredential()
            cls._secret_client = SecretClient(vault_url=cls.KV_URI, credential=credential)
        return cls._secret_client

    @classmethod
    def get_secret(cls, secret_name):
        client = cls.get_secret_client()
        try:
            return client.get_secret(secret_name).value
        except Exception as e:
            logging.error(f"Error retrieving secret '{secret_name}': {str(e)}")
            return None