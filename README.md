# Currency Converter Data Scraper API

## Overview
This is a mid-market currency converter API using FastAPI

### Motives
The main reason for creating this application was to practice 
reverse engineering private API and data scraping from that API.

Main features:
- FastAPI framework
- async HTTP requests using `httpx` library
- reverse engineered forex API
- authentication via API key

### Currency converter
Currency rates are provided by an external API `https://wise.com/gb/currency-converter/`. 

Supported operations are:
- Convert currency
- Get historical data of conversion rates

### Reverse engineering API
The following steps had to be taken to obtain forex data:

1. Inspecting HTTP requests from forex API
2. Identifying requests responsible for sending JSON response
3. Importing and converting cURL to HTTP request in `Postman`
4. Testing API call in `Postman`
5. Identifying query parameters and headers
6. Transferring forex API calls to `python`
7. Making async HTTP requests with `httpx`

### Authentication
To authenticate incoming requests, we check the `api_key` header.
 
## Get started
To run the API you will need an API key from `https://www.fastforex.io/`.
Create the `.env` file (use the `.env.dist` for reference) and add the 
Fast Forex API key.

### Dependencies
Dependency management is handled using `requirements.txt` file. 

### Docker setup

1. Build a docker image: `docker build -t currency_converter_api .`
2. Start redis server with : `docker-compose up -d --build --force-recreate currency_converter_api`
3. Create a running container: `docker run -p 80:80 currency_converter_api`

### Local setup

1. Install dependencies from `requirements.txt` file
2. Run the app: `uvicorn app.main:app --reload`

## Documentation
Once the application is up and running, you can access FastAPI automatic docs 
at index page `/`.

### Currency converter endpoints

| Method | Endpoint | Description                                |
|--------|----------|--------------------------------------------|
| GET    | /convert | convert one currency into another currency |       |
| GET    | /history | get historical exchange rates              |

## Status codes

| Status code | Description                               |
|-------------|-------------------------------------------|
| 200         | success                                   |
| 400         | bad request, please check your request    |
| 401         | user unauthorized, check your API key     |
| 424         | external dependency failed                |
| 429         | rate limit violation                      |
| 500         | internal server error, application failed |

## Examples

GET `/convert?amount=1000&from_currency=USD&to_currency=PLN`
```json
{
   "converted_amount":4343.35,
   "mid_market_rate":4.34335,
   "metadata":{
      "time_of_conversion":"2023-01-17 12:27:29",
      "from_currency":"USD",
      "to_currency":"PLN"
   }
}
```
GET `/convert?amount=1000&from_currency=USD&to_currency=PLN`
```json
[
   {
      "rate":4.3375,
      "time":"2023-01-16 12:00:00"
   },
   {
      "rate":4.3366,
      "time":"2023-01-16 13:00:00"
   },
   {
      "rate":4.33795,
      "time":"2023-01-16 14:00:00"
   }
]
