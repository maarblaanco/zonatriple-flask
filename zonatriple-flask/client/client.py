import asyncio
import httpx

BASE_URL = "http://127.0.0.1:5000/api/v1"


async def get_equipos(client):
    print("\nGET /equipos")
    try:
        response = await client.get(f"{BASE_URL}/equipos")
        response.raise_for_status()
        print(response.json())
    except httpx.HTTPStatusError as exc:
        print(f"Error HTTP al obtener equipos: {exc.response.status_code}")
    except httpx.RequestError as exc:
        print(f"Error de red al obtener equipos: {exc}")


async def get_equipo_by_id(client, equipo_id):
    print(f"\nGET /equipos/{equipo_id}")
    try:
        response = await client.get(f"{BASE_URL}/equipos/{equipo_id}")
        response.raise_for_status()
        print(response.json())
    except httpx.HTTPStatusError as exc:
        print(f"Error HTTP al obtener equipo {equipo_id}: {exc.response.status_code}")
    except httpx.RequestError as exc:
        print(f"Error de red al obtener equipo {equipo_id}: {exc}")


async def create_equipo(client):
    print("\nPOST /equipos")

    nuevo = {
        "nombre": "Equipo Prueba",
        "ciudad": "Sevilla",
        "fundacion": 2000,
        "liga": "ACB",
        "pabellon": "Pabellon Test",
        "aforo": 5000,
        "cantera": True,
        "user_id": "5af18195-77f6-489d-a2eb-568379105163"
    }

    try:
        response = await client.post(f"{BASE_URL}/equipos", json=nuevo)
        response.raise_for_status()
        data = response.json()
        print(data)
        return data.get("id")
    except httpx.HTTPStatusError as exc:
        print(f"Error HTTP al crear equipo: {exc.response.status_code}")
        try:
            print(exc.response.json())
        except Exception:
            print(exc.response.text)
    except httpx.RequestError as exc:
        print(f"Error de red al crear equipo: {exc}")

    return None


async def delete_equipo(client, equipo_id):
    print(f"\nDELETE /equipos/{equipo_id}")
    try:
        response = await client.delete(f"{BASE_URL}/equipos/{equipo_id}")
        response.raise_for_status()
        print(response.json())
    except httpx.HTTPStatusError as exc:
        print(f"Error HTTP al eliminar equipo: {exc.response.status_code}")
    except httpx.RequestError as exc:
        print(f"Error de red al eliminar equipo: {exc}")


async def main():
    async with httpx.AsyncClient() as client:
        await get_equipos(client)
        await get_equipo_by_id(client, 1)
        equipo_id = await create_equipo(client)

        if equipo_id:
            await delete_equipo(client, equipo_id)


if __name__ == "__main__":
    asyncio.run(main())