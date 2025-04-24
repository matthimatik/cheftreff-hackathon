from fastapi import FastAPI
from service import generate_report, generate_report_for_country
from plot_service import get_countries
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