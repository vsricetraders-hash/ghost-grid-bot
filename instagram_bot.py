import requests
from bs4 import BeautifulSoup
import json
import time
import random

# TERA NAYA FIREBASE FOLDER (instagram_leads)
FIREBASE_URL = "https://ghost-grid-db-default-rtdb.firebaseio.com/instagram_leads.json"

def infinite_ig_scraper():
    # Anti-Block Headers
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    ]
    
    # The "Bulk Data" Dorks (Premium US Niches)
    targets = [
        "site:instagram.com 'gaming creator' 'usa' -inurl:explore -inurl:p",
        "site:instagram.com 'dropshipping' 'entrepreneur' -inurl:explore",
        "site:instagram.com 'tech reviewer' 'contact' -inurl:explore",
        "site:instagram.com 'gta streamer' 'usa' -inurl:explore"
    ]
    
    all_leads = []
    print("🚀 Firing Instagram Bulk Scraper...")
    
    # Ye loop har category mein jayega aur bulk data nikalega
    for query in targets:
        headers = {"User-Agent": random.choice(user_agents)}
        search_url = "https://html.duckduckgo.com/html/"
        payload = {"q": query}
        
        try:
            res = requests.post(search_url, headers=headers, data=payload, timeout=20)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # Extracting the Bio and Details
            for snippet in soup.find_all('a', class_='result__snippet'):
                bio = snippet.text.strip()
                if len(bio) > 20:
                    all_leads.append({
                        "profile_bio": bio,
                        "niche": query.split("'")[1], # Auto-tags the niche
                        "platform": "Instagram",
                        "status": "Premium Lead",
                        "timestamp": time.ctime()
                    })
            # 2 second ka gap taaki engine block na kare
            time.sleep(2) 
        except Exception as e:
            continue
            
    if all_leads:
        requests.put(FIREBASE_URL, json.dumps(all_leads))
        print(f"✅ BAWAAL! {len(all_leads)} PREMIUM IG Leads Pushed!")
    else:
        print("⚠️ No IG leads this cycle. Retrying later.")

infinite_ig_scraper()
