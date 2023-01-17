import httpx
import asyncio
from datetime import datetime
import requests
from typing import List

from app.settings import FOREX_BASE_URL

# todo: exception mapper, handling errors


"""
https://fastapi.tiangolo.com/tutorial/handling-errors/
"""


# # scraping data from forex API.
# async def forex_request(params: dict) -> dict:
#     """
#     HTTP request to fetch data from forex API
#     :param params: query parameters
#     :return: forex response in JSON
#     """
#     async with httpx.AsyncClient() as client:
#         response = await client.get(
#             url=FOREX_BASE_URL,
#             params=params
#         )
#         return response.json()


# default query parameters
PARAMS = {
    "length": 1,
    "resolution": "hourly",
    "unit": "day"
}


def forex_request(parameters: dict) -> dict:
    """
    HTTP request to fetch data from forex API
    :param parameters: query parameters
    :return: forex response in JSON
    """
    PARAMS.update(parameters)
    response = requests.get(
        url=FOREX_BASE_URL,
        params=PARAMS
    )
    return response.json()

# print(asyncio.run(forex_request()))


def convert_currency(
    from_currency: str,
    to_currency: str,
    amount: int
) -> dict:
    """
    Convert an amount of one currency into another currency
    :param from_currency: Source currency code
    :param to_currency: Target currency code
    :param amount: Base currency unit amount
    :return: dict with converted_amount, mid_market_rate and metadata
    """
    # additional query parameters required for this API call
    params = {
        "source": from_currency,
        "target": to_currency
    }
    forex_response = forex_request(parameters=params)

    # scrape required data from forex response
    mid_market_rate = forex_response[-1].get("value")
    converted_amount = round(amount * mid_market_rate, 2)
    datetime_int = forex_response[-1].get("time")
    datetime_object = datetime.fromtimestamp(round(datetime_int/1000))

    output_format = {
        "converted_amount": converted_amount,
        "mid_market_rate": mid_market_rate,
        "metadata": {
            "time_of_conversion": str(datetime_object),
            "from_currency": from_currency,
            "to_currency": to_currency
        }
    }
    return output_format


def historical_data(
    from_currency: str,
    to_currency: str
) -> List[dict]:
    """
    The rate history per hour for up to 24 hours
    :param from_currency: Source currency code
    :param to_currency: Target currency code
    :return: list of dictionaries with hourly conversion rate and time
    """
    # additional query parameters required for this API call
    params = {
        "source": from_currency,
        "target": to_currency
    }
    forex_response = forex_request(parameters=params)

    # scrape required data from forex response
    history = []
    for i in range(len(forex_response)):
        mid_market_rate = forex_response[i].get("value")
        datetime_str = forex_response[i].get("time")
        datetime_object = datetime.fromtimestamp(round(datetime_str / 1000))
        historical_output = {
            "rate": mid_market_rate,
            "time": str(datetime_object)
        }
        history.append(historical_output)

    return history

# r = asyncio.run(convert(from_currency="USD", to_currency="PLN", amount=1000))

#
# r = convert_currency(from_currency="USD", to_currency="PLN", amount=1000)
# b = historical_data(from_currency="USD", to_currency="PLN")
#
# print(r)
# print(b)
