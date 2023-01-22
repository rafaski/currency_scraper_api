import os
from typing import Any
from dotenv import load_dotenv

load_dotenv()


def load_variable(name: str, default: Any = None) -> str:
    variable = os.getenv(name, default)
    if variable is None:
        print(f"Unable to load variable {name}")
    return variable


# access api key
API_KEY = load_variable(name="API_KEY")

# wise base url
WISE_BASE_URL = load_variable(
    name="WISE_BASE_URL",
    default="https://wise.com/rates/history+live"
)
WISE_CURRENCIES_URL = load_variable(
    name="WISE_CURRENCIES_URL",
    default="https://wise.com/gb/currency-converter/currencies"
)