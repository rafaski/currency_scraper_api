import httpx
from datetime import datetime
from typing import List
from functools import wraps

from app.settings import WISE_BASE_URL
from app.errors import ConverterException


def httpx_error_handler(func):
    """
    A generic httpx error handler
    """
    @wraps(func)
    async def _http_error_handler(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except httpx.HTTPError as error:
            raise ConverterException(details=str(error))
    return _http_error_handler


class WiseClient:
    """
    Class wrapper over currency converter HTTP requests
    """

    # default query parameters
    params = {
        "length": 1,
        "resolution": "hourly",
        "unit": "day"
    }

    @httpx_error_handler
    async def converter_request(self, parameters: dict) -> dict:
        """
        HTTP request to fetch data from forex API
        :param parameters: query parameters
        :return: forex response in JSON
        """
        self.params.update(parameters)

        # overwriting default 5 sec timeout
        timeout = httpx.Timeout(timeout=15.0, read=None)

        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=WISE_BASE_URL,
                params=self.params,
                timeout=timeout
            )
            return response.json()

    async def convert_currency(
        self,
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
        client_response = await self.converter_request(parameters=params)

        # get required data from client's response
        mid_market_rate = client_response[-1].get("value")
        # rounded only for visual presentation, to be amended for production
        converted_amount = round(amount * mid_market_rate, 2)
        datetime_int = client_response[-1].get("time")
        datetime_object = datetime.fromtimestamp(round(datetime_int/1000))

        output_format = {
            "converted_amount": converted_amount,
            "mid_market_rate": mid_market_rate,
            "metadata": {
                # datetime object to string for visual presentation only
                "time_of_conversion": str(datetime_object),
                "from_currency": from_currency,
                "to_currency": to_currency
            }
        }
        return output_format

    async def historical_data(
        self,
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
        client_response = await self.converter_request(parameters=params)

        # get required data from client's response
        history = []
        for i in range(len(client_response)):
            mid_market_rate = client_response[i].get("value")
            datetime_str = client_response[i].get("time")
            # rounded only for the visual aspect, to be amended for production
            datetime_object = datetime.fromtimestamp(round(datetime_str / 1000))
            output_format = {
                "rate": mid_market_rate,
                # datetime object to string for visual presentation only
                "time": str(datetime_object)
            }
            history.append(output_format)
        return history

    async def average_rate(
        self,
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
        # additional query parameters required for this API call
        params = {
            "source": from_currency,
            "target": to_currency,
            "length": duration,
            "resolution": "daily",
            "unit": "day"
        }
        client_response = await self.converter_request(parameters=params)

        # get required data from client's response
        average = 0
        for i in range(len(client_response)):
            mid_market_rate = client_response[i].get("value")
            average += mid_market_rate
        # rounded only for visual presentation, to be amended for production
        average = round(average/len(client_response), 4)

        output_format = {
            "average_rate": average,
            "duration_in_days": duration
        }
        return output_format

