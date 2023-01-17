from fastapi import FastAPI

from app.routers.converter import router as converter_router

description = """
### Mid-market currency converter API using FastAPI

### It allows you to:
* Convert supported currencies
* Get historical data on currency exchange rates

"""

app = FastAPI(
    title=" Mid-market currency converter API ",
    docs_url="/",
    description=description
    )

app.include_router(router=converter_router)
