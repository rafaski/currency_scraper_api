from fastapi import FastAPI

from app.routers.converter import router as converter_router

description = """
## Currency Converter Data Scraper API

Currency rates are provided by an external API 
`https://wise.com/gb/currency-converter/`. 

### Supported operations are:
- Convert currency
- Get historical data of conversion rates
- Get average conversion rate from the past X days

To authenticate incoming requests, we check the `api_key` header.
Please make sure to include it when calling this API.
"""

app = FastAPI(
    title="Currency Converter Data Scraper API",
    docs_url="/",
    description=description
    )

app.include_router(router=converter_router)
