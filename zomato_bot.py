import requests
from bs4 import BeautifulSoup
import json
import random
import time

# --- TERA FIREBASE LINK (Naya Folder: food_prices) ---
FIREBASE_URL = "https://ghost-grid-db-default-rtdb.firebaseio.com/food_prices.json"

def zomato_terminator(city="lucknow"):
    # High-Tech Headers: Zomato bahut tight security rakhta hai
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    }
    
    # Zomato Lucknow Delivery URL
    url = f"https://www.zomato.com/{city}/delivery"
    print(f"🍟 Scanning Food Prices in: {city}")
    
    try:
        # Zomato ko dhokha dene ke liye session use karenge
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=25)
        soup = BeautifulSoup(response.content, "html.parser")
        
        food_data = []
        
        # Restaurant cards dhoondna (Latest Zomato Classes)
        cards = soup.find_all("div", {"class": "jumbo-tracker"})
        
        for card in cards[:12]:
            try:
                res_name = card.find("h4").text.strip()
                # Cuisine aur Price for two aksar yahan hote hain
                info = card.find_all("p")
                cuisine = info[0].text.strip() if len(info) > 0 else "Food"
                price_for_two = info[1].text.strip() if len(info) > 1 else "N/A"
                rating = card.find("div", {"class": "css-1q722sk"}).text.strip() if card.find("div", {"class": "css-1q722sk"}) else "NEW"

                food_data.append({
                    "restaurant": res_name,
                    "speciality": cuisine,
                    "avg_price": price_for_two,
                    "rating": rating,
                    "city": city,
                    "update_time": time.ctime()
                })
            except: continue
            
        if food_data:
            requests.put(FIREBASE_URL, json.dumps(food_data))
            print(f"🔥 Bawaal! {len(food_data)} Restaurants Pushed to Firebase!")
        else:
            print("❌ Zomato security blocked. Need more high-tech rotation.")

    except Exception as e:
        print(f"❌ Error: {e}")

# Lucknow ke liye run karo
zomato_terminator("lucknow")
