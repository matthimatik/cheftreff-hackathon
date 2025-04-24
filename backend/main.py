from fastapi import FastAPI
from service import generate_report

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/generate_report")
async def main_endpoint(payload: dict):
    result = generate_report(payload)
    return {"result": result}
