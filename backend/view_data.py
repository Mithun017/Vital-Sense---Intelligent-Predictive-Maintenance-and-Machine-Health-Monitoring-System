import pymongo
import os
import json
from datetime import datetime

# MongoDB Config
MONGODB_URL = os.environ.get("MONGODB_URL", "mongodb://localhost:27017")
client = pymongo.MongoClient(MONGODB_URL)
db = client.vital_sense

def view_latest_data():
    print("==========================================================")
    print("   VITAL SENSE AI - RAW DATABASE VIEWER")
    print("==========================================================\n")

    # 1. View Latest Readings
    print("--- LATEST SENSOR READINGS ---")
    readings = list(db.sensor_readings.find({}, {"_id": 0}).sort("timestamp", -1).limit(3))
    for r in readings:
        print(f"[{r['timestamp']}] {r['machine_id']} | T:{r['temperature']}C | V:{r['vibration']} | C:{r['current']}A")
    print("")

    # 2. View Latest Predictions
    print("--- LATEST AI PREDICTIONS ---")
    predictions = list(db.predictions.find({}, {"_id": 0}).sort("timestamp", -1).limit(3))
    for p in predictions:
        print(f"[{p['timestamp']}] {p['health_status']} | RUL: {p['estimated_rul']}h | Prob: {round(p['failure_probability']*100, 1)}%")
        print(f"  AI Summary: {p.get('ai_summary', 'N/A')[:100]}...")
    print("\n==========================================================")

if __name__ == "__main__":
    view_latest_data()
