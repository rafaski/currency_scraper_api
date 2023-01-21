from typing import NoReturn
import re

from app.errors import BadRequest
from app.dependencies.wise_client import WiseClient


async def validate_input(
    from_currency: str,
    to_currency: str
) -> bool | NoReturn:
    """
    Validate if parsed currency symbol is in valid format
    :param from_currency: Source currency code
    :param to_currency: Target currency code
    :return: True or raise BadRequest error
    """
    # regex validation
    pattern = f"[A-Z][A-Z][A-Z]$"
    # wise.com supported currency validation
    list_of_currencies = await WiseClient().currencies()

    if any([
        re.fullmatch(pattern=pattern, string=from_currency) is None,
        re.fullmatch(pattern=pattern, string=to_currency) is None,
        from_currency not in list_of_currencies,
        to_currency not in list_of_currencies
    ]):
        raise BadRequest(details="Invalid currency")
    return True
