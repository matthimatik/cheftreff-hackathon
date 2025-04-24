import pandas as pd
import matplotlib.pyplot as plt
import io

CSV_CONTEXT = {
    'energy': {
        'commodity_to_include':['Fuel (diesel, heating, parallel market)', 'Fuel (diesel, transport, parallel market)', 'Fuel (diesel)',  'Oil'],
        'csv_path':'data/energy_prices.csv',
        'columns_to_keep' : ['Commodity', 'Price Date', 'Price']
    },
    'retail_prices_key_commodities' : {
        'commodity_to_include':['Rice', 'Chicken', 'Wheat', 'Eggs'],
        'csv_path':'data/key_prices.csv',
        'columns_to_keep' : ['Commodity', 'Price Date', 'Price']

    }
}


def get_countries():
  df = pd.read_csv(CSV_CONTEXT['energy']['csv_path'])
  column_names = df['Country'].unique().tolist()
  return {"countries": column_names}




    
    


def generate_price_over_month_csv(country, context):
  df = pd.read_csv(CSV_CONTEXT[context]['csv_path'])
  df['Price Date'] = pd.to_datetime(df['Price Date'])
  columns_to_keep = CSV_CONTEXT[context]['columns_to_keep']
  commodity_to_include = CSV_CONTEXT[context]['commodity_to_include']
  filtered_df = df[(df['Country'] == country) & (df['Commodity'].isin(commodity_to_include))][columns_to_keep]
  filtered_df.to_csv(f'.data/{country}_{context}.csv')
  csv_buffer = io.StringIO()
  filtered_df.to_csv(csv_buffer, index=False)
  csv_buffer.seek(0)
  return csv_buffer

