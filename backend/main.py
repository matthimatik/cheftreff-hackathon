from fastapi import FastAPI
from service import generate_report

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/generate_report")
async def call_service():
    result = generate_report()
    return {"result": result}
