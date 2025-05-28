import httpx

async def fetch_characters():
    """Función para obtener los datos de la API externa."""
    url = "https://rickandmortyapi.com/api/character"
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            characters = [
                {
                    "name": char["name"],
                    "species": char["species"],
                    "number_of_chapters": len(char["episode"])  # Contar episodios
                }
                for char in data.get("results", [])
            ]
            return sorted(characters, key=lambda x: x["number_of_chapters"], reverse=True)
    except httpx.RequestError as e:
        raise Exception(f"Error de conexión al consultar la API externa: {str(e)}")
    except httpx.HTTPStatusError as e:
        raise Exception(f"Respuesta inválida de la API externa: {e.response.status_code}")
    except Exception as e:
        raise Exception(f"Ocurrió un error inesperado: {str(e)}")
