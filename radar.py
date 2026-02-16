import os
import requests
import time

# FETCH SECRETS FROM GITHUB
WEBHOOK_URL = os.getenv("WEBHOOK_URL") 
ROLE_ID = "1469862498583973942"
TARGET_TAG = "XXX"

# Germany Box
LAT_MIN, LAT_MAX = 47.2, 55.1
LON_MIN, LON_MAX = 5.8, 15.1

def scan():
    # Verify the secret is actually loaded (it will show as 'Loaded' or 'MISSING')
    print(f"DEBUG: Webhook status: {'Loaded' if WEBHOOK_URL else 'MISSING'}")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15",
        "Referer": "https://www.geo-fs.com/"
    }
    
    try:
        response = requests.get("https://mps.geo-fs.com/map?v=3.9", headers=headers, timeout=10)
        data = response.json()
        pilots = data.get("instance", [])
        print(f"📡 Scan: {len(pilots)} pilots online.")

        for p in pilots:
            cs = str(p.get("cs", "")).upper()
            if TARGET_TAG.upper() in cs:
                lat, lon = float(p["lat"]), float(p["lon"])
                
                # Recognition check
                if LAT_MIN <= lat <= LAT_MAX and LON_MIN <= lon <= LON_MAX:
                    print(f"🎯 TARGET SPOTTED: {cs} in Germany!")
                    scramble(cs)
                else:
                    print(f"🔍 Found {cs}, but they are at {lat}, {lon} (Outside Germany).")
                    
    except Exception as e:
        print(f"⚠️ Connection error: {e}")

def scramble(cs):
    if not WEBHOOK_URL:
        print("❌ CRITICAL: WEBHOOK_URL is missing! Check your GitHub Secrets and YAML.")
        return
    
    payload = {
        "content": f"🚨 **SCRAMBLE! SCRAMBLE! SCRAMBLE!** 🚨\n<@&{ROLE_ID}> **INTERCEPT TARGET:** `{cs}` detected in GERMANY!"
    }
    r = requests.post(WEBHOOK_URL, json=payload)
    print(f"🚀 Scramble Signal Status: {r.status_code} (204 = Success)")

# Run the scan once (GitHub Actions handles the loop)
scan()
