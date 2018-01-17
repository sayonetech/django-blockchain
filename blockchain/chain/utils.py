from cryptography.fernet import Fernet, base64, InvalidSignature, InvalidToken
import hashlib
from django.contrib.auth.hashers import make_password, PBKDF2PasswordHasher, BasePasswordHasher, get_random_string
import logging

log = logging.getLogger(__name__)
import requests


class JsonApi(object):

    @classmethod
    def get(cls, base_url, api_url):
        url = '{}{}'.format(base_url, api_url)
        data = {}
        response = None
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
        except Exception as exc:
            log.warning('GET failed: {} - {}'.format(url, exc))
            if response is not None and hasattr(response, 'content'):
                log.warning('RESPONSE {}'.format(response.content))
        finally:
            return data


    @classmethod
    def post(cls, base_url, api_url, data):
        url = '{}{}'.format(base_url, api_url)
        response_data = {}
        response = None
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            if response.status_code == 201:
                log.info('Peer {} accepted block.'.format(base_url))
            if not len(response.content):
                if response.status_code == 304:
                    log.warning('Peer {}: unable to accept block.'.format(base_url))
            else:
                response_data = response.json()
        except Exception as exc:
            log.warning('POST failed: {} - {}'.format(url, exc))
            if response is not None and hasattr(response, 'content'):
                log.warning('RESPONSE {}'.format(response.content))
        finally:
            return response_data


class SymmetricEncryption(object):
    """
    AES256 encryption driven through Fernet library
    """
    @staticmethod
    def generate_key():
        return Fernet.generate_key()

    @staticmethod
    def safe_encode(value):
        if type(value) is str:
            value = value.encode('utf-8')
        return base64.urlsafe_b64encode(value)

    @staticmethod
    def generate_salt(length=12):
        return get_random_string(length=length)

    @classmethod
    def build_encryption_key(cls, password_hash):
        reduced = password_hash[:32].encode('utf-8')
        return base64.urlsafe_b64encode(reduced)

    @staticmethod
    def encrypt(key, secret):
        if type(key) is bytes:
            pass
        if type(secret) is str:
            secret = secret.encode('utf-8')
        if type(secret) is not bytes:
            raise TypeError('%s: Encryption requires string or bytes' % type(secret))

        return Fernet(key).encrypt(secret)

    @staticmethod
    def decrypt(key, token):
        return Fernet(key).decrypt(token)

    @staticmethod
    def hash(key):
        return hashlib.sha512(key).hexdigest()


class EncryptionApi(object):

    @staticmethod
    def make_password(raw_password, salt):
        """10000 iterations of pbkdf2 and return only hash"""
        hasher = PBKDF2PasswordHasher()
        hashed_password = hasher.encode(raw_password, salt)
        return hashed_password.split('$').pop()

    @classmethod
    def encrypt(cls, raw_password, data):
        salt = SymmetricEncryption.generate_salt()
        password = cls.make_password(raw_password, salt)
        encryption_key = SymmetricEncryption.build_encryption_key(password)
        e_data = SymmetricEncryption.encrypt(encryption_key, data)
        return '{}${}'.format(salt, e_data.decode('utf-8'))

    @classmethod
    def decrypt(cls, raw_password, stored_data):
        salt, e_data = stored_data.split('$')
        password = cls.make_password(raw_password, salt)
        encryption_key = SymmetricEncryption.build_encryption_key(password)
        data = SymmetricEncryption.decrypt(encryption_key, e_data.encode('utf-8'))
        return data.decode('utf-8')


