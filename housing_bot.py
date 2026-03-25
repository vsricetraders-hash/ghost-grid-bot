import requests
from bs4 import BeautifulSoup
import json
import random
import time

# TERA FIREBASE LINK (Naya Folder: real_estate)
FIREBASE_URL = "https://ghost-grid-db-default-rtdb.firebaseio.com/real_estate.json"

def housing_terminator(city="lucknow"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }
    
    # Housing.com Lucknow Buy Section
    url = f"https://housing.com/in/buy/resale/{city}/{city}"
    print(f"🏘️ Scanning Real Estate Market in: {city}")
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.content, "html.parser")
        listings = []
        
        # Housing.com ki latest property classes
        cards = soup.select('article')
        
        for card in cards[:15]:
            try:
                # Title, Price aur Location nikalna
                title = card.find("h2").text.strip() if card.find("h2") else "Property"
                # Housing prices aksar spans mein hote hain
                price = card.find("div", {"class": "css-1ni9965"}).text.strip() if card.find("div", {"class": "css-1ni9965"}) else "Contact for Price"
                loc = card.find("div", {"class": "css-1698223"}).text.strip() if card.find("div", {"class": "css-1698223"}) else "Lucknow"
                
                listings.append({
                    "property_name": title,
                    "price": price,
                    "location": loc,
                    "timestamp": time.ctime()
                })
            except:
                continue
            
        if listings:
            requests.put(FIREBASE_URL, json.dumps(listings))
            print(f"✅ Bawaal! {len(listings)} Real Estate items pushed!")
        else:
            print("❌ No data found. Security check needed.")

    except Exception as e:
        print(f"❌ Error: {e}")

# Run for Lucknow
housing_terminator("lucknow")
