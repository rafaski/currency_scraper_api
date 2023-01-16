from fastapi import APIRouter, Request, Depends
from app.auth import verify_api_key


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
):
    """
    Convert an amount of one currency into another currency.

    :param request: access Request object
    :param amount: Amount of source currency to convert
    :param from_currency: Base currency symbol
    :param to_currency: Target currency symbol
    :return: The converted amount and mid-market rate
    """
    return {"message": "Hello, world"}


@router.get("/history")
async def history(
    request: Request,
    currency_code: str
):
    """
    Get historical data on currency conversion (up to 24 hours)

    :param request: access Request object
    :param currency_code: Base currency symbol
    :return: the rate history per hour for up to 24 hours
    """
    return {"message": "Hello, world"}
