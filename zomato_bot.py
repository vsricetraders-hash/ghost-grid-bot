import requests
import json
import time

FIREBASE_URL = "https://ghost-grid-db-default-rtdb.firebaseio.com/food_prices.json"

def zomato_bypass():
    backup_food = [
        {"restaurant": "Tunday Kababi", "item": "Galouti Kebab", "price": "₹450", "rating": "4.8"},
        {"restaurant": "Royal Cafe", "item": "Basket Chaat", "price": "₹350", "rating": "4.6"},
        {"restaurant": "Idris Biryani", "item": "Mutton Biryani", "price": "₹500", "rating": "4.7"}
    ]
    
    try:
        res = requests.put(FIREBASE_URL, json.dumps(backup_food))
        if res.status_code == 200:
            print("✅ Zomato Food Data Pushed Successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")

zomato_bypass()
