import httpx
from aiocache import cached, Cache
from aiocache.serializers import JsonSerializer
from logger import logger


@cached(ttl=600, cache=Cache.MEMORY, serializer=JsonSerializer())
async def get_weather_by_city(ciudad: str):
    if not ciudad:
        return None

    logger.info(f"Consultando clima para ciudad={ciudad}")

    async with httpx.AsyncClient(timeout=10.0) as client:
        # 1. Buscar coordenadas de la ciudad
        geo_response = await client.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": ciudad,
                "count": 1,
                "language": "es",
                "format": "json"
            }
        )
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        resultados = geo_data.get("results")
        if not resultados:
            logger.warning(f"No se encontraron coordenadas para {ciudad}")
            return {
                "ciudad": ciudad,
                "temperatura": None,
                "viento": None,
                "codigo_tiempo": None,
                "instante": None
            }

        lat = resultados[0]["latitude"]
        lon = resultados[0]["longitude"]

        # 2. Pedir clima actual
        weather_response = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current_weather": "true"
            }
        )
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        current = weather_data.get("current_weather", {})

        logger.info(f"Clima obtenido correctamente para {ciudad}")

        return {
            "ciudad": ciudad,
            "temperatura": current.get("temperature"),
            "viento": current.get("windspeed"),
            "codigo_tiempo": current.get("weathercode"),
            "instante": current.get("time")
        }