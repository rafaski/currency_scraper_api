from fastapi import APIRouter, Request, Depends
from typing import List

from app.auth.verify import verify_api_key
from app.auth.validate import validate_input
from app.dependencies.wise_client import WiseClient


router = APIRouter(
    tags=["converter"],
    dependencies=[Depends(verify_api_key)]
    )


@router.get("/currencies")
async def currencies(request: Request) -> list:
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
) -> dict:
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


@router.get("/history")
async def history(
    request: Request,
    from_currency: str,
    to_currency: str
) -> List[dict]:
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


@router.get("/average")
async def average(
    request: Request,
    from_currency: str,
    to_currency: str,
    duration: int
) -> dict:
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
