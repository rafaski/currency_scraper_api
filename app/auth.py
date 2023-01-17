from fastapi import Request

from app.settings import API_KEY
from app.errors import Forbidden


async def verify_api_key(request: Request):
    """
    Verify access api key via headers
    """
    headers = dict(request.headers)
    api_key = headers.get("api_key")
    if api_key == API_KEY:
        return api_key
    raise Forbidden()
