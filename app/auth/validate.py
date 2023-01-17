from typing import NoReturn
import re

from app.errors import BadRequest


def validate_input(
    from_currency: str,
    to_currency: str
) -> bool | NoReturn:
    """
    Validate if parsed currency symbol is in valid format
    :param from_currency: Source currency code
    :param to_currency: Target currency code
    :return: True or raise BadRequest error
    """
    pattern = f"[A-Z][A-Z][A-Z]$"
    if re.fullmatch(pattern=pattern, string=from_currency) is None:
        raise BadRequest(details="Invalid currency")
    if re.fullmatch(pattern=pattern, string=to_currency) is None:
        raise BadRequest(details="Invalid currency")
    return True
