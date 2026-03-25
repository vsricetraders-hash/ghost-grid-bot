import requests
from bs4 import BeautifulSoup
import json
import random
import time

# --- TERA FIREBASE LINK ---
FIREBASE_URL = "https://ghost-grid-db-default-rtdb.firebaseio.com/.json"

def terminator_scraper(keyword):
    # Fake User-Agents taaki Amazon block na kare
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }
    
    search_query = keyword.replace(" ", "+")
    url = f"https://www.amazon.in/s?k={search_query}"
    
    print(f"🕵️ Searching Amazon for: {keyword}")
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.content, "html.parser")
        products = []
        
        # Amazon ke products dhoondna
        items = soup.select('div[data-component-type="s-search-result"]')
        
        for item in items[:10]:
            try:
                name = item.h2.text.strip()
                price_box = item.find("span", "a-price-whole")
                price = price_box.text.strip() if price_box else "N/A"
                
                products.append({
                    "product": name[:50] + "...",
                    "price": price,
                    "site": "Amazon India"
                })
            except:
                continue
        
        # --- FIREBASE FORCE UPDATE ---
        # Isse data hamesha naya dikhega
        final_package = {
            "last_check": time.ctime(),
            "bot_status": "Online",
            "current_keyword": keyword,
            "data": products
        }
        
        res = requests.put(FIREBASE_URL, json.dumps(final_package))
        
        if res.status_code == 200:
            print(f"✅ Success! {len(products)} items pushed at {time.ctime()}")
        else:
            print(f"❌ Firebase Error: {res.status_code}")

    except Exception as e:
        print(f"❌ Critical Error: {e}")

# Yahan apna keyword badlo jo search karna hai
terminator_scraper("gaming laptop")
