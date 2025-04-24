from fastapi import FastAPI
from service import generate_report
from plot_service import get_countries

app = FastAPI()


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
