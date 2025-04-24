from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from service import generate_report
from plot_service import fetch_exchange_rate_csv_generator, generate_price_over_month_csv, get_countries
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI()
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows the listed origins to make requests
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/countries")
async def get_countries_endpoint():
    result = get_countries()
    return {"result": result}

@app.post("/report")
async def report_endpoint(payload: dict = {}):
    result = generate_report(payload)
    return {"result": result}

@app.get("/csv/{country}/{context}")
async def generate_price_over_month_csv_endpoint(country, context):
    result = generate_price_over_month_csv(country, context)
    headers = {
        "Content-Disposition": "attachment; filename=export.csv",
        "Content-Type": "text/csv",
    }
    return StreamingResponse(result, headers=headers, media_type="text/csv")

@app.get("/exchange-rate/{country}")
async def get_exchange_rate(country: str):
    """
    Returns the exchange rate data as a CSV file for a given country.
    """
    csv_generator = fetch_exchange_rate_csv_generator(country)
    headers = {
        "Content-Disposition": f"attachment; filename=exchange_rate_{country.replace(' ', '_')}.csv",
        "Content-Type": "text/csv",
    }
    return StreamingResponse(csv_generator, headers=headers, media_type="text/csv")

            