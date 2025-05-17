from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import os

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5  # Token valid for 5 minutes

# Archivo para almacenar tokens revocados
REVOKED_TOKENS_FILE = "revoked_tokens.txt"

# Cargar tokens revocados desde el archivo
revoked_tokens = set()
if os.path.exists(REVOKED_TOKENS_FILE):
    with open(REVOKED_TOKENS_FILE, "r") as file:
        revoked_tokens = set(line.strip() for line in file)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str):
    try:
        if token in revoked_tokens:  # Verificamos si el token está revocado
            raise JWTError("Token has been revoked")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def revoke_token(token: str):
    revoked_tokens.add(token)
    with open(REVOKED_TOKENS_FILE, "a") as file:
        file.write(f"{token}\n")
