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
        # Fetch BTC price
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin",
            "vs_currencies": "eur"
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        btc_price = data["bitcoin"]["eur"]
        
        # Insert data into Supabase
        supabase.table('btc_prices').insert({"price": btc_price}).execute()
        
        print(f"${btc_price:,.2f}")
        return(f"${btc_price:,.2f}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    fetch_and_store_btc_price()