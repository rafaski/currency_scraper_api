import httpx
from datetime import datetime
from typing import List, NoReturn
import re
from functools import wraps

from app.settings import FOREX_BASE_URL
from app.errors import BadRequest, ForexException


# default query parameters
PARAMS = {
    "length": 1,
    "resolution": "hourly",
    "unit": "day"
}


def validate_input(
    value: str
) -> bool | NoReturn:
    """
    Validate if parsed currency symbol is in valid format
    :param value: User input of currency symbol
    :return: True or raise BadRequest error
    """
    pattern = f"[A-Z][A-Z][A-Z]$"
    if re.search(pattern=pattern, string=value) is None:
        raise BadRequest(details="Invalid currency")
    return True


def httpx_error_handler(func):
    """
    A generic httpx error handler
    """
    @wraps(func)
    async def _http_error_handler(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except httpx.HTTPError as error:
            raise ForexException(details=str(error))
    return _http_error_handler


# Data scraping from forex API
async def forex_request(parameters: dict) -> dict:
    """
    HTTP request to fetch data from forex API
    :param parameters: query parameters
    :return: forex response in JSON
    """
    PARAMS.update(parameters)
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url=FOREX_BASE_URL,
            params=PARAMS
        )
        return response.json()


async def convert_currency(
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
    validate_input(value=from_currency)
    validate_input(value=to_currency)

    # additional query parameters required for this API call
    params = {
        "source": from_currency,
        "target": to_currency
    }
    forex_response = await forex_request(parameters=params)

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


async def historical_data(
    from_currency: str,
    to_currency: str
) -> List[dict]:
    """
    The rate history per hour for up to 24 hours
    :param from_currency: Source currency code
    :param to_currency: Target currency code
    :return: list of dictionaries with hourly conversion rate and time
    """
    validate_input(value=from_currency)
    validate_input(value=to_currency)

    # additional query parameters required for this API call
    params = {
        "source": from_currency,
        "target": to_currency
    }
    forex_response = await forex_request(parameters=params)

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


async def average_rate(
    from_currency: str,
    to_currency: str,
    duration: int
) -> dict:
    """
    Get average conversion rate from the past X days
    :param from_currency: Source currency code
    :param to_currency: Target currency code
    :param duration: X days
    :return: average conversion rate from the past X days
    """
    validate_input(value=from_currency)
    validate_input(value=to_currency)

    # additional query parameters required for this API call
    params = {
        "source": from_currency,
        "target": to_currency,
        "length": duration,
        "resolution": "daily",
        "unit": "day"
    }
    forex_response = await forex_request(parameters=params)

    # scrape required data from forex response
    average = 0
    for i in range(len(forex_response)):
        mid_market_rate = forex_response[i].get("value")
        average += mid_market_rate
    average = round(average/len(forex_response), 4)

    output_format = {
        "average_rate": average,
        "duration_in_days": duration
    }
    return output_format

