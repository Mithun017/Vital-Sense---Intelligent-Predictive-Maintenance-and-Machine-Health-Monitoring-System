import motor.motor_asyncio
import os
from datetime import datetime
from typing import List, Dict, Any

# MongoDB Configuration
MONGODB_URL = os.environ.get("MONGODB_URL", "mongodb://localhost:27017")
CLIENT = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
DB = CLIENT.vital_sense

async def save_sensor_data(data: Dict[str, Any]):
    await DB.sensor_readings.insert_one(data)

async def save_prediction(prediction: Dict[str, Any]):
    await DB.predictions.insert_one(prediction)

async def save_alert(alert: Dict[str, Any]):
    await DB.alerts.insert_one(alert)

async def get_latest_readings(machine_id: str, limit: int = 50) -> List[Dict[str, Any]]:
    cursor = DB.sensor_readings.find({"machine_id": machine_id}, {"_id": 0}).sort("timestamp", -1).limit(limit)
    return await cursor.to_list(length=limit)

async def get_active_alerts(limit: int = 10) -> List[Dict[str, Any]]:
    cursor = DB.alerts.find({}, {"_id": 0}).sort("timestamp", -1).limit(limit)
    return await cursor.to_list(length=limit)

async def get_machine_health(machine_id: str) -> Dict[str, Any]:
    health = await DB.predictions.find_one({"machine_id": machine_id}, {"_id": 0}, sort=[("timestamp", -1)])
    return health
