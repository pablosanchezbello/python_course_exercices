import httpx
import logging
from utils.product_redis import store_product, retrieve_product

# Configurar el logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Omitir logs de SQLAlchemy
logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)

async def fetch_products(q: str, limit: int, skip: int):
    """Función para obtener los datos de products de la API Dummy.
    Args:
        - q: Query to search by that term
        - limit: Number of registers to return
        - skip: Number of registers to skip
    API call example:
        https://dummyjson.com/products?q=phone&limit=10&skip=10
    """
    url = f"https://dummyjson.com/products?select=id,title,description,price"
    if q: 
        url = url + f"&q={q}"
    if limit:
        url = url + f"&limit={limit}"
    if skip:
        url = url + f"&skip={skip}"
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            data = response.json()

            return data["products"]
        
    except httpx.RequestError as e:
        raise Exception(f"Error de conexión al consultar la API externa: {str(e)}")
    except httpx.HTTPStatusError as e:
        raise Exception(f"Respuesta inválida de la API externa: {e.response.status_code}")
    except Exception as e:
        raise Exception(f"Ocurrió un error inesperado: {str(e)}")
    

async def fetch_product_by_id(id: str):
    """Función para obtener los datos de un producto por ID.
    Args:
        - id: ID of the product to fetch
    API call example:
        https://dummyjson.com/products/{id}
    """
    url = f"https://dummyjson.com/products/{id}?select=id,title,description,price"
    try:
        product = retrieve_product(id)
        if product is None:
            async with httpx.AsyncClient(verify=False) as client:
                response = await client.get(url, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                logger.info(f"Producto obtenido: {data}")
                store_product(data)
                return data
        else:
            return product
        
    except httpx.RequestError as e:
        raise Exception(f"Error de conexión al consultar la API externa: {str(e)}")
    except httpx.HTTPStatusError as e:
        raise Exception(f"Respuesta inválida de la API externa: {e.response.status_code}")
    except Exception as e:
        raise Exception(f"Ocurrió un error inesperado: {str(e)}")
