import os
import json
import requests
from datetime import datetime, UTC  # Add UTC to the import
from typing import List, Dict
from dotenv import load_dotenv
from supabase import create_client, Client
from openai import OpenAI

# Load environment variables
load_dotenv(override=True)

# Initialize clients
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def search_brave_news(query: str) -> List[Dict]:
    """Search news using Brave Search API"""
    url = "https://api.search.brave.com/res/v1/news/search"
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": os.getenv("BRAVE_API_KEY")
    }
    params = {
        "q": query,
        "text_format": "plain",
        "count": 5
    }
    
    try:
        print(f"Making request to Brave API for query: {query}")
        response = requests.get(url, headers=headers, params=params)
        print(f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                # Add debug logging
                print(f"Raw response text: {response.text[:500]}...")  # Print first 500 chars
                data = response.json()
                print(f"Successfully parsed JSON with {len(data.get('results', []))} results")
                return data.get("results", [])
            except json.JSONDecodeError as je:
                print(f"JSON decode error at line {je.lineno}, col {je.colno}: {je.msg}")
                print(f"Error context: {response.text[max(0, je.pos-50):je.pos+50]}")
                return []
        else:
            print(f"Error response code: {response.status_code}")
            print(f"Error details: {response.text[:200]}...")
            return []
    except Exception as e:
        print(f"Error fetching news: {str(e)}")
        return []

def process_news_with_openai(news_items: List[Dict]) -> List[Dict]:
    """Process news items with OpenAI"""
    if not news_items:
        return []

    try:
        print(f"Processing {len(news_items)} news items with OpenAI...")
        response = openai_client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {
                    "role": "system",
                    "content": "Return a JSON object with 'articles' array. Each article must have 'title' and 'body' fields."
                },
                {
                    "role": "user",
                    "content": json.dumps({"articles": news_items})
                }
            ],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        print(f"OpenAI processed result: {json.dumps(result, indent=2)}")
        return result.get('articles', [])

    except Exception as e:
        print(f"OpenAI processing error: {str(e)}")
        return []

def store_news_in_supabase(news_items: List[Dict]):
    """Store news in Supabase"""
    print(f"Attempting to store {len(news_items)} news items...")
    
    for item in news_items:
        try:
            data = {
                "finance_info": {
                    "title": item.get("title"),
                    "body": item.get("body")
                }
            }
            
            print(f"Inserting data: {json.dumps(data, indent=2)}")
            result = supabase.table('eco_news').insert(data).execute()
            print(f"Insert result: {result.data}")
            
        except Exception as e:
            print(f"Storage error: {str(e)}")
            print(f"Failed data: {data}")

def fetch_crypto_news() -> List[Dict]:
    """Fetch cryptocurrency related news"""
    crypto_queries = [
        "bitcoin price market analysis",
        "cryptocurrency market trends",
        "crypto regulation news"
    ]
    crypto_news = []
    for query in crypto_queries:
        news_items = search_brave_news(query)
        if news_items:
            crypto_news.extend(news_items)
    return crypto_news

def fetch_market_news() -> List[Dict]:
    """Fetch general market and economic news"""
    market_queries = [
        "global financial markets analysis",
        "federal reserve policy news",
        "macroeconomic trends inflation"
    ]
    market_news = []
    for query in market_queries:
        news_items = search_brave_news(query)
        if news_items:
            market_news.extend(news_items)
    return market_news

def fetch_and_process_news():
    """Main function to fetch, process and store news"""
    print("Fetching crypto news...")
    crypto_news = fetch_crypto_news()
    
    print("\nFetching market news...")
    market_news = fetch_market_news()
    
    # Process both sets of news
    if crypto_news:
        crypto_processed = process_news_with_openai(crypto_news)
        store_news_in_supabase(crypto_processed)
    
    if market_news:
        market_processed = process_news_with_openai(market_news)
        store_news_in_supabase(market_processed)
    
    if not crypto_news and not market_news:
        print("No news found")

if __name__ == "__main__":
    fetch_and_process_news()