import hashlib


class EncryptMethods:
    @classmethod
    def encrypt_pwd(cls, password):
        encrypted_pwd = hashlib.sha256(password.encode()).hexdigest()
        return encrypted_pwd

