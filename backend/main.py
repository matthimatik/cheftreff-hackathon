from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from service import generate_report
from plot_service import fetch_exchange_rate_csv_generator, generate_price_over_month_csv, get_countries, plot_csv
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

def get_html_png(base64):
    """
    Converts a base64 string to an HTML image tag.
    """
    return f'<img src="data:image/png;base64,{base64}" alt="plot" />'

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/countries")
async def get_countries_endpoint():
    result = get_countries()
    return {"result": result}

@app.post("/report")
async def report_endpoint(payload: dict = {}):
    print(f"REQUEST: {payload}")
    result = generate_report(payload)
    result += get_html_png(await get_plot_base64(payload["country"], "energy_prices"))
    result += get_html_png(await get_plot_base64(payload["country"], "retail_prices_key_commodities"))
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

@app.get("/plot/{country}/{context}/base64")
async def get_plot_base64(country, context):
    csv = generate_price_over_month_csv(country, context)
    base64_string = plot_csv(f'{country}_{context}', csv.read(), from_path=False)
    if "Error:" in base64_string:
        return {"error": base64_string}  # Return the error message
    return base64_string