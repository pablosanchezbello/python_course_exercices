import os
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

from auth.redis import is_token_revoked

SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY", "your_refresh_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES_VIEWER = 15
ACCESS_TOKEN_EXPIRE_MINUTES_USER = 30
ACCESS_TOKEN_EXPIRE_MINUTES_ADMIN = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Archivo para almacenar tokens revocados
REVOKED_TOKENS_FILE = "revoked_tokens.txt"

# Cargar tokens revocados desde el archivo
revoked_tokens = set()
if os.path.exists(REVOKED_TOKENS_FILE):
    with open(REVOKED_TOKENS_FILE, "r") as file:
        revoked_tokens = set(line.strip() for line in file)

def create_access_token(data: dict, role: str, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES_USER):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    if role == "admin":
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES_ADMIN)
    elif role == "viewer":
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES_VIEWER)
    to_encode.update({"exp": expire, "role": role})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str):
    try:
        if token in revoked_tokens or is_token_revoked(token):  # Verificar si el token está revocado
            raise JWTError("Token has been revoked")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def verify_refresh_token(token: str):
    try:
        payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def revoke_token(token: str):
    """Revocar un token y almacenarlo en el archivo."""
    revoked_tokens.add(token)
    with open(REVOKED_TOKENS_FILE, "a") as file:
        file.write(f"{token}\n")
