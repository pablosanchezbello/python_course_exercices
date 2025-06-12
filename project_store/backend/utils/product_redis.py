import redis
from datetime import timedelta
import os
import json
from models.product import Product

from dotenv import load_dotenv
load_dotenv()

# Conexión a Redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def store_product(product: Product, expiration: int = 600):
    """Stores a product for 10 minutes."""
    redis_client.setex(product['id'], timedelta(seconds=expiration), json.dumps(product))

def retrieve_product(product_id: int) -> bool:
    """Get product by ID."""
    return json.loads(redis_client.get(product_id)) if redis_client.exists(product_id) == 1 else None
