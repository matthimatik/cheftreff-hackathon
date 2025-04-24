from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
from io import StringIO
from datetime import datetime, timedelta

@app.post("/process-csv")
async def process_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted.")

    contents = await file.read()
    df = pd.read_csv(StringIO(contents.decode("utf-8")))

    if "Date" not in df.columns or "Value" not in df.columns:
        raise HTTPException(status_code=400, detail="CSV must contain 'Date' and 'Value' columns.")

    # Parse the Date
    try:
        df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Date parsing failed: {e}")

    # Filter out rows older than 12 months
    one_year_ago = datetime.now() - timedelta(days=365)
    df = df[df["Date"] >= one_year_ago]

    # Clean up Value column
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
    df = df.dropna(subset=["Value"])

    # Group by date and calculate average
    grouped = df.groupby(df["Date"].dt.date)["Value"].mean().round(2).reset_index()
    grouped.columns = ["Date", "AverageValue"]

    # Return as JSON
    return JSONResponse(content=grouped.to_dict(orient="records"))
