import requests
from bs4 import BeautifulSoup
import json
import time
import random

FIREBASE_URL = "https://ghost-grid-db-default-rtdb.firebaseio.com/real_estate.json"

def infinite_housing_scraper():
    # High-Tech Rotating Headers
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
    ]
    headers = {"User-Agent": random.choice(user_agents)}
    
    # Bypass logic for Housing.com Lucknow Live Properties
    search_url = "https://html.duckduckgo.com/html/"
    payload = {"q": "site:housing.com/in/buy/resale/lucknow price flats"}
    
    print("🚀 Firing Housing Infinity Scraper...")
    try:
        res = requests.post(search_url, headers=headers, data=payload, timeout=20)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        property_leads = []
        for snippet in soup.find_all('a', class_='result__snippet'):
            details = snippet.text.strip()
            if len(details) > 15:
                property_leads.append({
                    "property_details": details,
                    "city": "Lucknow",
                    "status": "Live Active Listing",
                    "timestamp": time.ctime()
                })
                
        if property_leads:
            requests.put(FIREBASE_URL, json.dumps(property_leads))
            print(f"✅ BAWAAL! {len(property_leads)} FRESH Property Leads Pushed!")
        else:
            print("⚠️ No new properties this cycle. Will retry in 6 hours.")
            
    except Exception as e:
        print(f"❌ Error in Scraping: {e}")

infinite_housing_scraper()
