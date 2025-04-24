from fastapi import FastAPI
from service import generate_report, generate_report_for_country
from fastapi.responses import StreamingResponse
from service import generate_report
from plot_service import generate_price_over_month_csv, get_countries
from fastapi.middleware.cors import CORSMiddleware

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

@app.post("/generate_report")
async def main_endpoint(payload: dict):
    result = generate_report(payload)
    return {"result": result}

@app.get("/countries")
async def get_countries_endpoint():
    result = get_countries()
    return {"result": result}

@app.post("/report")
async def report_endpoint(payload: dict):
    result = generate_report_for_country(payload)
    return {"result": result}

@app.get("/csv/{country}/{context}")
async def generate_price_over_month_csv_endpoint(country, context):
    result = generate_price_over_month_csv(country, context)
    headers = {
        "Content-Disposition": "attachment; filename=export.csv",
        "Content-Type": "text/csv",
    }
    return StreamingResponse(result, headers=headers, media_type="text/csv")
