import requests
from bs4 import BeautifulSoup
import json
import time

FIREBASE_URL = "https://ghost-grid-db-default-rtdb.firebaseio.com/scraped_data.json"

def scrape_amazon_stealth(keyword):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    search_query = keyword.replace(" ", "+")
    url = f"https://www.amazon.in/s?k={search_query}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    products = []
    items = soup.select('div[data-component-type="s-search-result"]')
    for item in items[:10]:
        try:
            name = item.h2.text.strip()
            price = item.find("span", "a-price-whole").text.strip()
            products.append({"product_name": name, "price_in_inr": price, "source": "Amazon India"})
        except: continue
    if len(products) > 0:
        requests.put(FIREBASE_URL, json.dumps(products))
        print(f"Done! {len(products)} items pushed.")

scrape_amazon_stealth("samsung s24 ultra")
