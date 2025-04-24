import base64
import csv
import pandas as pd
import matplotlib.pyplot as plt
import io
import requests
from datetime import datetime, timedelta

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
        'columns_to_keep' : ['Commodity', 'Price Date', 'Price', 'Unit', 'Currency']
    },
    'retail_prices_key_commodities' : {
        'commodity_to_include':['Rice', 'Chicken', 'Wheat', 'Eggs'],
        'csv_path':'data/key_prices.csv',
        'columns_to_keep' : ['Commodity', 'Price Date', 'Price', 'Unit', 'Currency']

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
  print(context)
  if context == "exchange_rate":
    print("Fetching exchange rate data...")
    return fetch_parallel_exchange_rate_csv(country)
  
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


def plot_csv(title, csv, from_path=False):
    if from_path:
        df = pd.read_csv(csv)
    else:
        df = pd.read_csv(io.StringIO(csv))
    unit = df['Unit'].iloc[0]
    currency = df['Currency'].iloc[0]
    pivot_table = df.pivot_table(index='Price Date', columns='Commodity', values='Price')
    plt.figure(figsize=(12, 6))
    for product in pivot_table.columns:
      plt.plot(pivot_table.index, pivot_table[product], marker='o', label=product)
    plt.xlabel('Month')
    plt.ylabel(f'Price {currency} per {unit}')
    plt.title(f'{title}')
    plt.legend()
    plt.grid(True)
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format="png")
    img_buf.seek(0)  # Reset buffer position to the beginning

    # Encode the image to Base64
    base64_encoded = base64.b64encode(img_buf.read()).decode("utf-8")
    plt.close()  # Close the figure to free memory
    return base64_encoded

def fetch_parallel_exchange_rate_csv(country):
  # Import necessary libraries

  # Assume your CSV file is named 'exchange_rates.csv'
  # file_path = 'parallel_exchange_rates.csv'
  
  base_url = "https://api.vam.wfp.org/economicExplorer/Currency/ExchangeRateExport"
  request_body = {"rateType": "Parallel"}
  adm0Code = COUNTRY_MAPPING.get(country)
  if adm0Code is None:
      yield f"Error: Country '{country}' not found in mapping.\n".encode('utf-8')
      return

  payload = {**request_body, "adm0Code": adm0Code}
  
  try:
        response = requests.post(base_url, json=payload, stream=True, timeout=10)
        response.raise_for_status()
        print("Response: ", response.content)

        if 'text/csv' in response.headers.get('Content-Type', ''):
          
            # get csv from content
            csv_content = response.content.decode('utf-8')
            
            print("CSV content fetched successfully.")
            
            # Print the first 500 characters of the CSV content
            print(csv_content[:2000])  # Print the first 500 characters for debugging
            
            # read dataframe from csv string
            # df = pd.read_csv(io.StringIO(csv_content))
            
            df = pd.read_csv(
                io.StringIO(csv_content),
                skip_blank_lines=True,
                skipinitialspace=True  # remove spaces after commas
            )
            
            print("Parsed columns:", df.columns.tolist())
            # Check if the expected columns are present
            if 'Date' not in df.columns or 'Value' not in df.columns:
                yield f"Error: CSV does not contain 'Date' and 'Value' columns.\n".encode('utf-8')
                return
            # Print the first few rows of the DataFrame for debugging
            print("first rows of the DataFrame:", df.head())
            
            lines = csv_content.splitlines()
            print("Total lines:", len(lines))
            print("First 5 lines:")
            for line in lines[:5]:
              print(repr(line))
            
            # print("CSV content loaded into DataFrame.", df.head())
            
            # Convert the 'Date' column to datetime format
            df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce')
            
            # Calculate the date 12 months ago from today
            twelve_months_ago = datetime.now() - timedelta(days=365) # Assuming an average of 365 days in a year

            # Filter the DataFrame to keep only entries with dates within the last 12 months
            df_cleaned = df[df['Date'] >= twelve_months_ago]

            # Group the DataFrame by 'Date' and calculate the average of the 'Value' for each day
            daily_aggregated_value = df_cleaned.groupby('Date')['Value'].mean().reset_index()

            # Rename the 'Value' column to 'Aggregated_Value' for clarity
            daily_aggregated_value.rename(columns={'Value': 'Aggregated_Value'}, inplace=True)

            # Print the resulting aggregated DataFrame
            print("Daily Aggregated Values:")
            print(daily_aggregated_value)


            # Save the cleaned DataFrame back to a new CSV file (optional, but good practice)
            cleaned_file_path = 'parallel_exchange_rates_cleaned.csv'
            daily_aggregated_value.to_csv(cleaned_file_path, index=False)

            # send the cleaned data to the user
            csv_buffer = io.StringIO()
            daily_aggregated_value.to_csv(csv_buffer, index=False)
            
            csv_buffer.seek(0)
            return csv_buffer
        else:
            yield f"Error: Unexpected content type '{response.headers.get('Content-Type')}' for {country} ({adm0Code})\n".encode('utf-8')
            response.close()
            
  except requests.exceptions.RequestException as e:
        yield f"Error fetching data for {country} ({adm0Code}): {e}\n".encode('utf-8')
  except Exception as e:
        yield f"An unexpected error occurred for {country} ({adm0Code}): {e}\n".encode('utf-8')
