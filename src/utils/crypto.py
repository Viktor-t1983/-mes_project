import hashlib
import secrets

def generate_secure_token(length: int = 32) -> str:
    """Генерирует криптографически безопасный токен."""
    return secrets.token_urlsafe(length)

def hash_password(password: str, salt: str) -> str:
    """Хеширует пароль с солью."""
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()

def verify_password(password: str, salt: str, hashed: str) -> bool:
    """Проверяет пароль."""
    return hash_password(password, salt) == hashed
