import os
import requests
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv(override=True)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_and_store_btc_price():
    try:
        # Debug: Print environment variables (redacted)
        print("Supabase URL exists:", bool(os.getenv("SUPABASE_URL")))
        print("Supabase KEY exists:", bool(os.getenv("SUPABASE_KEY")))

        # Fetch BTC price
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin",
            "vs_currencies": "usd"
        }
        
        # Debug: API request
        print("Fetching from CoinGecko API...")
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise exception for bad status codes
        
        data = response.json()
        print("API Response:", data)
        
        btc_price_usd = data["bitcoin"]["usd"]
        
        # Debug: Print price before insert
        print(f"Price to insert: ${btc_price_usd}")
        
        # Insert data into Supabase
        data = {
            "price": btc_price_usd
        }
        
        # Debug: Supabase insert
        print("Inserting into Supabase...")
        result = supabase.table('btc_prices').insert(data).execute()
        print("Insert result:", result)
        
        print(f"The current price of Bitcoin (BTC) is: ${btc_price_usd:,.2f} USD")
        print("Data successfully stored in Supabase")
        
    except requests.exceptions.RequestException as e:
        print(f"API Error: {str(e)}")
    except KeyError as e:
        print(f"Data parsing error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        print(f"Error type: {type(e)}")

if __name__ == "__main__":
    fetch_and_store_btc_price()