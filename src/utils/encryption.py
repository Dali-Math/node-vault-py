import base64, secrets
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class CryptoManager:
    def __init__(self, password=None, salt=None):
        self.salt = salt or secrets.token_bytes(16)
        self.key = self.derive_key(password, self.salt) if password else None
        self.cipher_suite = Fernet(self.key) if self.key else None

    def derive_key(self, password, salt, iterations=100_000):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=iterations,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    def encrypt(self, data):
        if not self.cipher_suite or not data:
            return data
        d = data.encode() if isinstance(data, str) else data
        return self.cipher_suite.encrypt(d).decode()

    def decrypt(self, data):
        if not self.cipher_suite or not data:
            return data
        d = data.encode() if isinstance(data, str) else data
        return self.cipher_suite.decrypt(d).decode()
