import requests
import time
import random
from datetime import datetime, timezone

# Virtual ESP32 Config
DEVICE_ID = "M-101"
API_URL = "http://localhost:8000/ingest"

def print_esp32_boot():
    print("--- ESP32 VIRTUAL HARDWARE STARTING ---")
    print("Connecting to WiFi: VitalSense_AP...")
    time.sleep(1)
    print("WiFi Connected! IP: 192.168.1.105")
    print("Connecting to Vital Sense Backend...")
    time.sleep(1)
    print("Backend Linked. Starting sensor polling...\n")

def simulate_esp32_loop():
    print_esp32_boot()
    while True:
        # Simulate ESP32 sensor readings
        temp = random.normalvariate(72, 5)
        vibe = random.normalvariate(3, 1)
        curr = random.normalvariate(15, 2)
        
        payload = {
            "machine_id": DEVICE_ID,
            "temperature": round(temp, 2),
            "vibration": round(vibe, 2),
            "current": round(curr, 2),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        try:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Sending JSON Packet...")
            print(f"  > Temp: {payload['temperature']}C | Vibe: {payload['vibration']}mm/s | Curr: {payload['current']}A")
            
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                print("  [SUCCESS] Response: 200 OK")
            else:
                print(f"  [ERROR] Server returned {response.status_code}")
                
        except Exception as e:
            print(f"  [CRITICAL ERROR] Network timeout: {e}")
            
        time.sleep(3)

if __name__ == "__main__":
    simulate_esp32_loop()
