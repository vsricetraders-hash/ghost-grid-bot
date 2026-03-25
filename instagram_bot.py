import requests
from bs4 import BeautifulSoup
import json
import time
import random

FIREBASE_URL = "https://ghost-grid-db-default-rtdb.firebaseio.com/instagram_leads.json"

def advanced_ig_scraper():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
    ]
    
    # Premium US Queries
    targets = [
        "site:instagram.com 'gaming creator' 'usa' -inurl:explore -inurl:p",
        "site:instagram.com 'dropshipping' 'usa' -inurl:explore -inurl:p",
        "site:instagram.com 'tech reviewer' -inurl:explore -inurl:p"
    ]
    
    all_leads = []
    print("🚀 Firing Advanced IG Lead Extractor...")
    
    for query in targets:
        headers = {"User-Agent": random.choice(user_agents)}
        search_url = "https://html.duckduckgo.com/html/"
        payload = {"q": query}
        
        try:
            res = requests.post(search_url, headers=headers, data=payload, timeout=20)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # Ab hum pura result block uthayenge taaki Link aur Bio dono mile
            results = soup.find_all('div', class_='result')
            
            for row in results:
                url_tag = row.find('a', class_='result__url')
                snippet_tag = row.find('a', class_='result__snippet')
                
                if url_tag and snippet_tag:
                    raw_url = url_tag.text.strip() # Ye deta hai 'instagram.com/username'
                    bio = snippet_tag.text.strip()
                    
                    # Sirf asli profiles uthana, kachra links nahi
                    if 'instagram.com/' in raw_url and '/p/' not in raw_url:
                        # Username extract karna
                        username = raw_url.split('instagram.com/')[-1].replace('/', '').strip()
                        
                        # Followers extract karna (Smart Jugaad)
                        followers = "N/A"
                        if "Followers" in bio:
                            followers = bio.split("Followers")[0].strip().split()[-1]
                        
                        # Agar username valid hai, tabhi database mein daalo
                        if username and len(username) < 30:
                            all_leads.append({
                                "username": "@" + username,
                                "profile_link": "https://www.instagram.com/" + username,
                                "followers": followers,
                                "niche": query.split("'")[1],
                                "timestamp": time.ctime()
                            })
            time.sleep(2)
        except Exception as e:
            continue
            
    if all_leads:
        requests.put(FIREBASE_URL, json.dumps(all_leads))
        print(f"✅ BAWAAL! {len(all_leads)} REAL ACTIONABLE IG Leads Pushed!")
    else:
        print("⚠️ No leads this cycle.")

advanced_ig_scraper()
