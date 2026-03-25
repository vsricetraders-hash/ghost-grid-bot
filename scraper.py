import requests
from bs4 import BeautifulSoup
import json
import random
import time

# --- TERA FIREBASE SETUP ---
FIREBASE_URL = "https://ghost-grid-db-default-rtdb.firebaseio.com/scraped_data.json"

# High-Tech: Har baar naya device dikhayenge Amazon ko
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1"
]

def get_data(keyword):
    results = []
    
    # --- 1. AMAZON ATTACK ---
    amz_url = f"https://www.amazon.in/s?k={keyword.replace(' ', '+')}"
    headers = {"User-Agent": random.choice(USER_AGENTS), "Accept-Language": "en-US,en;q=0.5"}
    
    try:
        res = requests.get(amz_url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.content, "html.parser")
        items = soup.select('div[data-component-type="s-search-result"]')
        for item in items[:5]:
            name = item.h2.text.strip()
            price = item.find("span", "a-price-whole").text.strip() if item.find("span", "a-price-whole") else "N/A"
            results.append({"name": name, "price": price, "site": "Amazon", "tag": keyword})
    except: pass

    time.sleep(2) # Gap taaki block na ho

    # --- 2. FLIPKART ATTACK ---
    fk_url = f"https://www.flipkart.com/search?q={keyword.replace(' ', '+')}"
    try:
        res = requests.get(fk_url, headers={"User-Agent": random.choice(USER_AGENTS)}, timeout=10)
        soup = BeautifulSoup(res.content, "html.parser")
        # Flipkart ki classes badalti rehti hain, ye current latest hai
        titles = soup.find_all("div", {"class": "KzY6M-"}) or soup.find_all("a", {"class": "wY9S_c"})
        prices = soup.find_all("div", {"class": "Nx9R0j"})
        
        for t, p in zip(titles[:5], prices[:5]):
            results.append({"name": t.text.strip(), "price": p.text.strip(), "site": "Flipkart", "tag": keyword})
    except: pass

    # --- FIREBASE MEIN PUSH ---
    if results:
        requests.put(FIREBASE_URL, json.dumps(results))
        print(f"🔥 Bawaal! {len(results)} items (Amazon+Flipkart) pushed to Firebase!")
    else:
        print("❌ Dono sites ne block kar diya. IP badalna padega.")

# Isko "iPhone 15" ke liye set kar dete hain
get_data("iphone 15")
