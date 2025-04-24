import os
from pathlib import Path
import pandas as pd
# import matplotlib.pyplot as plt

CSV_PATH_ENERGY = Path('data/prices1.csv')

def get_countries():
  print(os.getcwd())
  df = pd.read_csv(CSV_PATH_ENERGY)
  column_names = df['Country'].unique().tolist()
  return {"countries": column_names}

