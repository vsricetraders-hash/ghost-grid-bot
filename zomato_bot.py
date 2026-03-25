import requests
from bs4 import BeautifulSoup
import json
import time
import random

FIREBASE_URL = "https://ghost-grid-db-default-rtdb.firebaseio.com/food_prices.json"

def infinite_zomato_scraper():
    # High-Tech Rotating Headers (Bypass Security)
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    ]
    headers = {"User-Agent": random.choice(user_agents)}
    
    # DuckDuckGo Bypass to scrape Live Zomato Lucknow Pages without getting blocked
    search_url = "https://html.duckduckgo.com/html/"
    payload = {"q": "site:zomato.com lucknow restaurants menu prices"}
    
    print("🚀 Firing Zomato Infinity Scraper...")
    try:
        res = requests.post(search_url, headers=headers, data=payload, timeout=20)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        fresh_leads = []
        # Scraping live dynamic snippets
        for snippet in soup.find_all('a', class_='result__snippet'):
            data_text = snippet.text.strip()
            if len(data_text) > 10:
                fresh_leads.append({
                    "restaurant_info": data_text,
                    "location": "Lucknow",
                    "status": "Live Scraped",
                    "timestamp": time.ctime()
                })
                
        if fresh_leads:
            # Pushing unlimited fresh data to Firebase
            requests.put(FIREBASE_URL, json.dumps(fresh_leads))
            print(f"✅ BAWAAL! {len(fresh_leads)} FRESH Zomato Leads Pushed!")
        else:
            print("⚠️ No new data this cycle. Will retry in 6 hours.")
            
    except Exception as e:
        print(f"❌ Error in Scraping: {e}")

infinite_zomato_scraper()
