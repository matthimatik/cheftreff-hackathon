import csv
import pandas as pd
import matplotlib.pyplot as plt
import io
import requests

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

COUNTRY_MAPPING = {
  "Afghanistan": 1,
  "Albania": 3,
  "Algeria": 4,
  "Angola": 8,
  "Argentina": 12,
  "Armenia": 13,
  "Australia": 17,
  "Austria": 18,
  "Azerbaijan": 19,
  "Bahamas": 20,
  "Bangladesh": 23,
  "Belarus": 26,
  "Belgium": 27,
  "Benin": 29,
  "Bhutan": 31,
  "Bolivia (Plurinational State of)": 33,
  "Burkina Faso": 42,
  "Burundi": 43,
  "Cambodia": 44,
  "Cameroon": 45,
  "Cape Verde": 47,
  "Cayman Islands": 48,
  "Central African Republic": 49,
  "Chad": 50,
  "Chile": 51,
  "China": 53,
  "Colombia": 57,
  "Congo": 59,
  "Costa Rica": 61,
  "CÃ´te d'Ivoire": 66,
  "Democratic People's Republic of Korea": 67,
  "Democratic Republic of the Congo": 68,
  "Djibouti": 70,
  "Dominican Republic": 72,
  "Eritrea": 77,
  "Ethiopia": 79,
  "Gabon": 89,
  "Gambia": 90,
  "Georgia": 92,
  "Ghana": 94,
  "Guatemala": 103,
  "Guinea-Bissau": 105,
  "Guinea": 106,
  "Haiti": 108,
  "Honduras": 111,
  "India": 115,
  "Iran (Islamic Republic of)": 117,
  "Iraq": 118,
  "Italy": 122,
  "Jamaica": 123,
  "Japan": 126,
  "Jordan": 130,
  "Kazakhstan": 132,
  "Kenya": 133,
  "Kyrgyzstan": 138,
  "Lao People's Democratic Republic": 139,
  "Lebanon": 141,
  "Lesotho": 142,
  "Liberia": 144,
  "Libya": 145,
  "Madagascar": 150,
  "Malawi": 152,
  "Mali": 155,
  "Mauritania": 159,
  "Mexico": 162,
  "Republic of Moldova": 165,
  "Mongolia": 167,
  "Morocco": 169,
  "Mozambique": 170,
  "Namibia": 172,
  "Nepal": 175,
  "Nicaragua": 180,
  "Niger": 181,
  "Nigeria": 182,
  "Pakistan": 188,
  "Panama": 191,
  "Paraguay": 194,
  "Peru": 195,
  "Russian Federation": 204,
  "Rwanda": 205,
  "Sao Tome and Principe": 214,
  "Saudi Arabia": 215,
  "Sierra Leone": 221,
  "Somalia": 226,
  "South Africa": 227,
  "Sri Lanka": 231,
  "Suriname": 233,
  "Eswatini": 235,
  "Syrian Arab Republic": 238,
  "Tajikistan": 239,
  "Thailand": 240,
  "Togo": 243,
  "Trinidad and Tobago": 246,
  "Tunisia": 248,
  "Turkey": 249,
  "Turkmenistan": 250,
  "Uganda": 253,
  "Ukraine": 254,
  "United Republic of Tanzania": 257,
  "Uzbekistan": 261,
  "Venezuela": 263,
  "Viet Nam": 264,
  "Yemen": 269,
  "Zambia": 270,
  "Zimbabwe": 271,
  "Indonesia": 272,
  "Myanmar": 273,
  "Papua New Guinea": 274,
  "Philippines": 275,
  "Fiji": 276,
  "Senegal": 278
}

def get_countries():
  df = pd.read_csv(CSV_CONTEXT['energy_prices']['csv_path'])
  column_names = df['Country'].unique().tolist()
  return {"countries": column_names}


def generate_price_over_month_csv(country, context):
  df = pd.read_csv(CSV_CONTEXT[context]['csv_path'])
  df['Price Date'] = pd.to_datetime(df['Price Date'])
  columns_to_keep = CSV_CONTEXT[context]['columns_to_keep']
  commodity_to_include = CSV_CONTEXT[context]['commodity_to_include']
  filtered_df = df[(df['Country'] == country) & (df['Commodity'].isin(commodity_to_include))][columns_to_keep]
  filtered_df.to_csv(f'data/{country}_{context}.csv')
  csv_buffer = io.StringIO()
  filtered_df.to_csv(csv_buffer, index=False)
  csv_buffer.seek(0)
  return csv_buffer




def fetch_exchange_rate_csv_generator(country):
    """
    Fetches exchange rate data for a given country and returns a generator
    that yields the CSV content.
    """
    base_url = "https://api.vam.wfp.org/economicExplorer/Currency/ExchangeRateExport"
    request_body = {"rateType": "Official"}
    adm0Code = COUNTRY_MAPPING.get(country)
    if adm0Code is None:
        yield f"Error: Country '{country}' not found in mapping.\n".encode('utf-8')
        return

    payload = {**request_body, "adm0Code": adm0Code}
    try:
        response = requests.post(base_url, json=payload, stream=True, timeout=10)
        response.raise_for_status()

        if 'text/csv' in response.headers.get('Content-Type', ''):
            yield response.content
        else:
            yield f"Error: Unexpected content type '{response.headers.get('Content-Type')}' for {country} ({adm0Code})\n".encode('utf-8')
            response.close()
    except requests.exceptions.RequestException as e:
        yield f"Error fetching data for {country} ({adm0Code}): {e}\n".encode('utf-8')
    except Exception as e:
        yield f"An unexpected error occurred for {country} ({adm0Code}): {e}\n".encode('utf-8')


       
