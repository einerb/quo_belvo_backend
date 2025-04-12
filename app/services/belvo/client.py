import httpx
import base64

from app.core.config import settings

def get_auth_headers():
    credentials = f"{settings.BELVO_SECRET_ID}:{settings.BELVO_SECRET_PASSWORD}".encode()
    token = base64.b64encode(credentials).decode()
    return {"Authorization": f"Basic {token}"}

async def belvo_get(endpoint: str):
    url = f"{settings.BELVO_API_URL}/{endpoint}"
    headers = get_auth_headers()
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

async def belvo_post(endpoint: str, payload: dict):
    url = f"{settings.BELVO_API_URL}/{endpoint}"
    headers = get_auth_headers()
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            try:
                error_detail = exc.response.json()
                print(f"Error detail: {error_detail}")
                if isinstance(error_detail, list) and "message" in error_detail[0]:
                    raise Exception(error_detail[0]["message"])
                elif isinstance(error_detail, dict) and "message" in error_detail:
                    raise Exception(error_detail["message"])
                else:
                    raise Exception("Unexpected error format from Belvo.")
            except Exception as parse_error:
                raise Exception(f"Unknown error: {str(parse_error)}")
        return response.json()