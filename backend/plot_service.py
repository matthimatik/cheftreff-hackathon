import pandas as pd
import matplotlib.pyplot as plt
import io

# all topics
TOPICS = {
  'HIGHLIGHTS': 'HIGHLIGHTS',
  'economic_updates': 'Economic Updates',
  'daily_wage': 'Daily wage',
  'global_food_prices_and_inflation_trends': 'Global food prices and inflation trends',
  'meb': 'Minimum Expenditure Basket (MEB)',
  'retail_prices_key_commodities': 'Retail prices for key commodities',
  'exchange_rate': 'Exchange rate',
  'energy_prices': 'Energy prices',
  'retail_meb_food': 'Retail prices for MEB food components',
  'retail_meb_non-food': 'Retail prices for MEB non-food components',
  'map': 'Map: Population density and MEB Mapping'
}

CSV_CONTEXT = {
    'energy_prices': {
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

