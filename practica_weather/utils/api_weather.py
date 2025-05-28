import httpx

async def fetch_data(latitude: float, longitude: float):
    """Función para obtener los datos de la API externa.
    Args:
        latitude (float): Latitud de la ubicación.
        longitude (float): Longitud de la ubicación.
    API call example:
        https://api.open-meteo.com/v1/forecast?latitude=40.4165&longitude=-3.7026&hourly=temperature_2m,relative_humidity_2m,rain
    """
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,relative_humidity_2m,rain"
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            data = response.json()

            # Extract the arrays from the data
            times = data["hourly"]["time"]
            temperatures = data["hourly"]["temperature_2m"]
            humidities = data["hourly"]["relative_humidity_2m"]
            rains = data["hourly"]["rain"]

            # Create an array of objects
            weather_data = [
                {
                    "time": times[i],
                    "temperature": temperatures[i],
                    "humidity": humidities[i],
                    "rain": rains[i]
                }
                for i in range(len(times))
            ]

            return weather_data
    except httpx.RequestError as e:
        raise Exception(f"Error de conexión al consultar la API externa: {str(e)}")
    except httpx.HTTPStatusError as e:
        raise Exception(f"Respuesta inválida de la API externa: {e.response.status_code}")
    except Exception as e:
        raise Exception(f"Ocurrió un error inesperado: {str(e)}")
