import pandas as pd
import matplotlib.pyplot as plt

CSV_PATH_ENERGY = '/data/Prices-Export-Thu Apr 24 2025 16_10_15 GMT+0200 (Mitteleuropaeische Sommerzeit).csv'

def get_countries():
  df = pd.read_csv(CSV_PATH_ENERGY)
  column_names = df['Country'].unique().tolist()
  return {"countries": column_names}

