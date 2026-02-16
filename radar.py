import requests
import time

# HARDCODED SETTINGS
WEBHOOK_URL = "https://discord.com/api/webhooks/1472942848822218786/gKaQB1wLENdtt0i9owillaaD_gyj7rz5DGAf8-K2vx6B61WzcxCwqIFOlyOPxAV-ZiCU"
ROLE_ID = "1469862498583973942"
TARGET_TAG = "XXX"

# Germany Airspace Box
LAT_MIN, LAT_MAX = 47.2, 55.1
LON_MIN, LON_MAX = 5.8, 15.1

def scan():
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
                lat, lon = float(p.get("lat", 0)), float(p.get("lon", 0))
                
                if LAT_MIN <= lat <= LAT_MAX and LON_MIN <= lon <= LON_MAX:
                    print(f"🎯 TARGET SPOTTED: {cs} at {lat}, {lon}")
                    scramble(cs)
                else:
                    print(f"🔍 Target {cs} found, but outside Germany.")
                    
    except Exception as e:
        print(f"⚠️ Error: {e}")

def scramble(cs):
    payload = {
        "content": f"🚨 **SCRAMBLE! SCRAMBLE! SCRAMBLE!** 🚨\n<@&{ROLE_ID}> **INTERCEPT TARGET:** `{cs}` detected in GERMANY!"
    }
    r = requests.post(WEBHOOK_URL, json=payload)
    print(f"🚀 Scramble Status: {r.status_code}")

# Run once for GitHub Actions
scan()
