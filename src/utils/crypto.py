from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def encrypt_data( str, key: bytes) -> str:
    f = Fernet(key)
    return f.encrypt(data.encode()).decode()

def decrypt_data(encrypted_ str, key: bytes) -> str:
    f = Fernet(key)
    return f.decrypt(encrypted_data.encode()).decode()
