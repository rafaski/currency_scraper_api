import httpx
import asyncio

from app.settings import FOREX_BASE_URL

"""
I reversed engineered `wise` API with postman (import curl http request)
"""
# todo: exception mapper, handling errors


"""
https://fastapi.tiangolo.com/tutorial/handling-errors/
"""

FROM_CURRENCY = "USD"
TO_CURRENCY = "PLN"
LENGTH = 24
UNIT = "hour"

params = {
    "source": FROM_CURRENCY,
    "target": TO_CURRENCY,
    "length": LENGTH,
    "resolution": "hourly",
    "unit": UNIT
}

resp1 = [{'source': 'USD', 'target': 'PLN', 'value': 4.3316, 'time': 1673816400000}, {'source': 'USD', 'target': 'PLN', 'value': 4.3313, 'time': 1673820000000}, {'source': 'USD', 'target': 'PLN', 'value': 4.33235, 'time': 1673823600000}, {'source': 'USD', 'target': 'PLN', 'value': 4.3364, 'time': 1673827200000}, {'source': 'USD', 'target': 'PLN', 'value': 4.32855, 'time': 1673830800000}, {'source': 'USD', 'target': 'PLN', 'value': 4.31905, 'time': 1673834400000}, {'source': 'USD', 'target': 'PLN', 'value': 4.31875, 'time': 1673838000000}, {'source': 'USD', 'target': 'PLN', 'value': 4.32165, 'time': 1673841600000}, {'source': 'USD', 'target': 'PLN', 'value': 4.324, 'time': 1673845200000}, {'source': 'USD', 'target': 'PLN', 'value': 4.3221, 'time': 1673848800000}, {'source': 'USD', 'target': 'PLN', 'value': 4.32985, 'time': 1673852400000}, {'source': 'USD', 'target': 'PLN', 'value': 4.33945, 'time': 1673856000000}, {'source': 'USD', 'target': 'PLN', 'value': 4.35085, 'time': 1673859600000}, {'source': 'USD', 'target': 'PLN', 'value': 4.34185, 'time': 1673863200000}, {'source': 'USD', 'target': 'PLN', 'value': 4.3375, 'time': 1673866800000}, {'source': 'USD', 'target': 'PLN', 'value': 4.3366, 'time': 1673870400000}, {'source': 'USD', 'target': 'PLN', 'value': 4.33795, 'time': 1673874000000}, {'source': 'USD', 'target': 'PLN', 'value': 4.33975, 'time': 1673877600000}, {'source': 'USD', 'target': 'PLN', 'value': 4.335, 'time': 1673881200000}, {'source': 'USD', 'target': 'PLN', 'value': 4.33405, 'time': 1673884800000}, {'source': 'USD', 'target': 'PLN', 'value': 4.33345, 'time': 1673888400000}, {'source': 'USD', 'target': 'PLN', 'value': 4.336, 'time': 1673892000000}, {'source': 'USD', 'target': 'PLN', 'value': 4.3378, 'time': 1673895600000}, {'source': 'USD', 'target': 'PLN', 'value': 4.33405, 'time': 1673899200000}, {'source': 'USD', 'target': 'PLN', 'value': 4.33685, 'time': 1673906333093}]

resp2 = [
    {
        "rate": 1.12695,
        "source": "GBP",
        "target": "EUR",
        "time": "2023-01-16T21:13:22+0000"
    }
]


# scraping data from forex API.
async def forex_request() -> dict:
    """
    Async HTTP request to fetch data from forex API
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url=FOREX_BASE_URL,
            params=params
        )
        return response.json()

print(asyncio.run(forex_request()))
