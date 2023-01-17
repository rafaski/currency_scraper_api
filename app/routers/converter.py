from fastapi import APIRouter, Request, Depends
from typing import List

from app.auth import verify_api_key
from app.dependencies.forex_client import ForexClient


router = APIRouter(
    tags=["converter"],
    dependencies=[Depends(verify_api_key)]
    )


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
    results = await ForexClient().convert_currency(
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
    results = await ForexClient().historical_data(
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
    results = await ForexClient().average_rate(
        from_currency=from_currency,
        to_currency=to_currency,
        duration=duration
    )
    return results
