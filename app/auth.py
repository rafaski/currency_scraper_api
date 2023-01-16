from fastapi import Request, HTTPException
from app.settings import API_KEY


async def verify_api_key(request: Request):
    """
    Verify access api key
    """
    headers = dict(request.headers)
    api_key = headers.get("api_key")
    if api_key == API_KEY:
        return api_key
    raise HTTPException(status_code=403, detail="Access forbidden")
