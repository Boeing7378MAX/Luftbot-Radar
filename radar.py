import requests
import time

# --- 1. CONFIGURATION ---
# Replace with your actual Discord Webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1472942848822218786/gKaQB1wLENdtt0i9owillaaD_gyj7rz5DGAf8-K2vx6B61WzcxCwqIFOlyOPxAV-ZiCU"
ROLE_ID = "1469862498583973942"
TARGET_TAG = "XXX" # The tag to hunt

# Geographic Bounds: Germany
LAT_MIN, LAT_MAX = 47.2, 55.1
LON_MIN, LON_MAX = 5.8, 15.1

# This set keeps track of who we already pinged
alerted_ids = set()

def scan():
    # FIXED: Global must be declared FIRST
    global alerted_ids 
    
    # Mimics a mobile browser to bypass basic bot filters
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
        "Referer": "https://www.geo-fs.com/"
    }
    
    try:
        # Fetch data from the direct MPS stream
        response = requests.get("https://mps.geo-fs.com/map?v=3.9", headers=headers, timeout=10)
        data = response.json()
        
        if "instance" in data:
            pilots = data["instance"]
            print(f"[{time.strftime('%H:%M:%S')}] 📡 Scan: {len(pilots)} pilots online.")
            
            for p in pilots:
                # Force everything to uppercase for recognition
                cs = str(p.get("cs", "")).upper()
                p_id = p.get("id")
                
                # Check for the tag anywhere in the callsign
                if TARGET_TAG.upper() in cs:
                    lat, lon = float(p["lat"]), float(p["lon"])
                    
                    # Germany Airspace check
                    if LAT_MIN <= lat <= LAT_MAX and LON_MIN <= lon <= LON_MAX:
                        if p_id not in alerted_ids:
                            scramble(cs)
                            alerted_ids.add(p_id)
            
            # Maintenance: Remove pilots who disconnected so they can be caught again later
            current_ids = {p["id"] for p in pilots}
            alerted_ids = {aid for aid in alerted_ids if aid in current_ids}
            
    except Exception as e:
        print(f"⚠️ Connection blip: {e}")

def scramble(cs):
    # This is the 'Scramble' alert for Discord
    payload = {
        "content": f"🚨 **SCRAMBLE! SCRAMBLE! SCRAMBLE!** 🚨\n<@&{ROLE_ID}> **INTERCEPT TARGET:** `{cs}` detected in GERMANY!"
    }
    try:
        requests.post(WEBHOOK_URL, json=payload)
        print(f"🚀 SCRAMBLE ALERT SENT FOR: {cs}")
    except:
        print("❌ Failed to reach Discord.")

# --- MAIN LOOP ---
print("====================================")
print("   LUFTBOT RADAR v3.9 (PYTHON)      ")
print("====================================")

while True:
    scan()
    # Wait 60 seconds to avoid being IP banned
    time.sleep(60)
