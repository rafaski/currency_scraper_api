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

# forex base url
FOREX_BASE_URL = load_variable(
    name="FOREX_BASE_URL",
    default="https://wise.com/rates/history+live"
)
