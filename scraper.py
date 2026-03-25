import requests
from bs4 import BeautifulSoup
import json
import random
import time

FIREBASE_URL = "https://ghost-grid-db-default-rtdb.firebaseio.com/scraped_data.json"

# Sabse tagde User-Agents ka collection
AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
]

def heavy_duty_scraper(keyword):
    headers = {
        "User-Agent": random.choice(AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }
    
    url = f"https://www.amazon.in/s?k={keyword.replace(' ', '+')}"
    print(f"🚀 Launching Attack on Amazon for: {keyword}")
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        products = []
        
        # Amazon ke products nikalne ka sabse pakka tarika
        for item in soup.select('div[data-component-type="s-search-result"]'):
            try:
                name = item.h2.text.strip()
                price_tag = item.find("span", "a-price-whole")
                price = price_tag.text.strip() if price_tag else "Check Website"
                
                products.append({
                    "product": name[:60] + "...", # Naam thoda chota rakhenge
                    "price_inr": price,
                    "search_tag": keyword,
                    "update_time": time.ctime()
                })
            except: continue
            
        if products:
            requests.put(FIREBASE_URL, json.dumps(products))
            print(f"✅ Mission Success: {len(products)} Items in Firebase!")
        else:
            print("⚠️ Amazon blocked us or no results. Retrying next time.")
            
    except Exception as e:
        print(f"❌ Error: {e}")

# Ab hum "Latest Gadgets" ka data bhar dete hain
heavy_duty_scraper("gaming laptop")
