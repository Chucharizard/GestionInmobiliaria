"""
Script temporal para generar hash de contraseña con bcrypt
"""
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

password = "Test1234"
hash_password = pwd_context.hash(password)

print(f"Contraseña: {password}")
print(f"Hash: {hash_password}")
print(f"\nHash en bytes (para PostgreSQL BYTEA):")
print(f"{hash_password.encode('utf-8')}")
