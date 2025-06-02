import redis
from datetime import timedelta
import os

from dotenv import load_dotenv
load_dotenv()

# Conexión a Redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def revoke_token(token: str, expiration: int = 3601):
    """Revoca un token almacenándolo en Redis con un tiempo de expiración."""
    redis_client.setex(token, timedelta(seconds=expiration), "revoked")

def is_token_revoked(token: str) -> bool:
    """Verifica si un token ha sido revocado."""
    return redis_client.exists(token) == 1
