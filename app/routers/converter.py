from fastapi import APIRouter, Request, Depends
from typing import List

from app.auth.verify import verify_api_key
from app.auth.validate import validate_input
from app.dependencies.wise_client import WiseClient
from app import schemas

router = APIRouter(
    tags=["converter"],
    dependencies=[Depends(verify_api_key)]
    )


@router.get("/currencies")
async def currencies(request: Request) -> dict:
    """
    Get a list of all supported currencies
    """
    results = await WiseClient().currencies()
    return results


@router.get("/convert")
async def convert(
    request: Request,
    amount: int,
    from_currency: str,
    to_currency: str
) -> schemas.ConvertCurrency:
    """
    Convert an amount of one currency into another currency
    """
    is_valid = validate_input(
        from_currency=from_currency,
        to_currency=to_currency
    )
    if is_valid:
        results = await WiseClient().convert_currency(
            from_currency=from_currency,
            to_currency=to_currency,
            amount=amount
        )
        return results


@router.get("/historical_rates")
async def get_historical_rates(
    request: Request,
    from_currency: str,
    to_currency: str
) -> List[schemas.HistoricalRates]:
    """
    Get historical data on currency conversion (up to 24 hours),
    hourly intervals
    """
    is_valid = validate_input(
        from_currency=from_currency,
        to_currency=to_currency
    )
    if is_valid:
        results = await WiseClient().historical_data(
            from_currency=from_currency,
            to_currency=to_currency
        )
        return results


@router.get("/all_requests")
async def get_all_requests(
    request: Request
) -> List[dict]:
    """
    Get a list of all currency conversions that you've requested so fat
    """
    all_requests = WiseClient.all_requests
    return all_requests


@router.get("/average")
async def average(
    request: Request,
    from_currency: str,
    to_currency: str,
    duration: int
) -> schemas.AverageRate:
    """
    Get average conversion rate from the past X days
    """
    is_valid = validate_input(
        from_currency=from_currency,
        to_currency=to_currency
    )
    if is_valid:
        results = await WiseClient().average_rate(
            from_currency=from_currency,
            to_currency=to_currency,
            duration=duration
        )
        return results
