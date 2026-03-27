import requests
import time
import random
import argparse
from datetime import datetime, timezone

# Configuration
API_URL = "http://localhost:8000/ingest"
INTERVAL = 3  # Seconds between readings

def generate_sensor_data(machine_id, fault_type=None):
    """
    Generate dynamic sensor readings.
    fault_type: "OVERHEAT", "VIBRATION", "OVERLOAD", or None (NORMAL)
    """
    # Base normal values
    temp = random.normalvariate(65, 3)
    vibe = random.normalvariate(2, 0.3)
    curr = random.normalvariate(12, 0.5)
    
    # Inject Faults (Phase 11: Failure Simulation)
    if fault_type == "OVERHEAT":
        temp = random.uniform(90, 110)
    elif fault_type == "VIBRATION":
        vibe = random.uniform(7, 12)
    elif fault_type == "OVERLOAD":
        curr = random.uniform(22, 35)
    elif random.random() < 0.02: # Occasional random spike
        temp += random.uniform(10, 20)
        
    # Voltage (Phase 10)
    volt = random.normalvariate(230, 2)
    
    return {
        "machine_id": machine_id,
        "temperature": round(temp, 2),
        "vibration": round(vibe, 2),
        "current": round(curr, 2),
        "voltage": round(volt, 1),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

def main():
    parser = argparse.ArgumentParser(description="Advanced Sensor Simulation")
    parser.add_argument("--id", default="M-101", help="Machine ID")
    parser.add_argument("--fault", choices=["OVERHEAT", "VIBRATION", "OVERLOAD"], help="Force a failure type")
    args = parser.parse_args()

    print(f"Starting advanced simulation for {args.id}...")
    if args.fault:
        print(f"--- FAILURE SIMULATION MODE ACTIVE: {args.fault} ---")
    
    while True:
        data = generate_sensor_data(args.id, args.fault)
        try:
            response = requests.post(API_URL, json=data)
            if response.status_code == 200:
                res_json = response.json()
                pred = res_json.get("prediction", {})
                status = pred.get("health_status", "UNKNOWN")
                rul = pred.get("estimated_rul", "N/A")
                
                print(f"[{datetime.now().strftime('%H:%M:%S')}] {args.id} | Status: {status} | RUL: {rul}h")
                
                energy = pred.get("energy_metrics", {})
                if energy:
                    print(f"     >> Energy: {energy.get('power_watts')}W | Eff: {energy.get('efficiency_pct')}%")
                
                if "alert" in res_json:
                    print(f"!!! ALERT: {res_json['alert']['message']} !!!")
            else:
                print(f"Failed to send data: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("Error: Could not connect to backend.")
            
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
