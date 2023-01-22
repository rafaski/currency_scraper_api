# Currency Converter Data Scraper API

## Overview
This is a Currency Converter Data Scraper API

### Motives
The main reason for creating this application was to practice 
reverse engineering APIs and web scraping.

Main features:
- FastAPI framework
- async HTTP requests using `httpx` library
- reverse engineered `wise.com` API
- `wise.com` web scraping with `BeautifulSoup`
- authentication via API key
- `regex` currency input validation
- custom error handling
- OOP where applicable

### Currency converter
Currency rates are provided by an external API `https://wise.com/gb/currency-converter/`

Supported operations are:
- Get a list of all supported currencies
- Convert currency
- Get historical data of conversion rates
- Get average conversion rate from the past X days

### Reverse engineering API
The following steps had to be taken to obtain `wise.com` data:

1. Inspecting HTTP requests from `wise.com` API
2. Identifying requests responsible for sending JSON response
3. Importing and converting cURL to HTTP request in `Postman`
4. Testing API call in `Postman`
5. Identifying query parameters and headers
6. Transferring `wise.com` API calls to `python`
7. Making async HTTP requests with `httpx`

### Web scraping
The list of all supported currency names and codes in `/currencies` endpoint 
was scraped using `BeautifulSoup` framework. 
All user currency input is validated against that list.

### Authentication
To authenticate incoming requests, we check the `api_key` header.
Create the `.env` file (use the `.env.dist` for reference) 
and add `API_KEY` to environment variables.

### Dependencies
Dependency management is handled using `requirements.txt` file. 

### Docker setup

1. Build a docker image: `docker build -t currency_scraper_api .`
2. Create a running container: `docker run -p 8080:8080 currency_scraper_api`

### Local setup

1. Install dependencies from `requirements.txt` file
2. Run the app: `uvicorn app.main:app --reload`

## Documentation
Once the application is up and running, you can access FastAPI automatic docs 
at index page `/`

### Currency converter endpoints

| Method | Endpoint    | Description                                |
|--------|-------------|--------------------------------------------|
| GET    | /currencies | get a list of all supported currencies     | 
| GET    | /convert    | convert one currency into another currency |  
| GET    | /history    | get historical exchange rates              |
| GET    | /average    | get average exchange rate from past X days |

## Status codes

| Status code | Description                               |
|-------------|-------------------------------------------|
| 200         | success                                   |
| 400         | bad request, please check your request    |
| 401         | user unauthorized, check your API key     |
| 424         | external dependency failed                |
| 500         | internal server error, application failed |

## Examples
GET `/currencies`
```json
{
  "AED": "United Arab Emirates Dirham",
  "ALL": "Albanian Lek",
  "AMD": "Armenian Dram",
  "ANG": "Netherlands Antillean Guilder",
  "AOA": "Angolan Kwanza",
  "ARS": "Argentine Peso"
}
```
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
GET `/history?from_currency=USD&to_currency=PLN`
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
```
GET `/average?from_currency=USD&to_currency=PLN&duration=30`
```json
{
	"average_rate": 4.3832,
	"duration_in_days": 30
}
```
