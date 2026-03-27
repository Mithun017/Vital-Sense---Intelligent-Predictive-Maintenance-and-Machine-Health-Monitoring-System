from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

from models import SensorData, PredictionResponse, Alert
from database import save_sensor_data, save_prediction, save_alert, get_latest_readings, get_active_alerts, get_machine_health
from ml_engine import ENGINE
from groq_service import generate_health_summary, answer_user_query

app = FastAPI(title="Vital Sense AI - Advanced Predictive Maintenance")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from typing import List, Dict, Any, Optional, Union

def sanitize_data(data: Any) -> Any:
    """Recursively remove _id and other non-serializable objects from data."""
    if isinstance(data, list):
        return [sanitize_data(i) for i in data]
    elif isinstance(data, dict):
        return {k: sanitize_data(v) for k, v in data.items() if k != "_id"}
    return data

@app.get("/")
async def root():
    return {"message": "Vital Sense AI Advanced Backend is running."}

@app.post("/ingest", response_model=Dict[str, Any])
async def ingest_sensor_data(data: SensorData):
    sensor_dict = data.dict()
    await save_sensor_data(sensor_dict)
    
    # 1. Advanced ML Processing
    status, failure_prob, xai_data = ENGINE.predict_status_and_xai(sensor_dict)
    
    # 2. RUL Prediction (Phase 2)
    history = await get_latest_readings(data.machine_id, 30)
    rul_hours = ENGINE.estimate_rul(data.machine_id, history)
    
    # 3. Smart Recommendations (Phase 4)
    recommendations = ENGINE.get_maintenance_recommendation(status, xai_data)
    
    # 4. Gemini Health Summary (Phase 5)
    # Note: Using small delay or background task if it's too slow in production
    ai_summary = await generate_health_summary(data.machine_id, sensor_dict, status)
    
    # 5. Energy & Efficiency (Phase 10)
    energy_data = ENGINE.calculate_efficiency_metrics(sensor_dict)
    
    prediction = {
        "machine_id": data.machine_id,
        "health_status": status,
        "failure_probability": failure_prob,
        "estimated_rul": rul_hours,
        "xai_explanations": xai_data,
        "recommendations": recommendations,
        "ai_summary": ai_summary,
        "energy_metrics": energy_data,
        "timestamp": datetime.now(timezone.utc)
    }
    await save_prediction(prediction)
    prediction.pop("_id", None)  # Remove internal ID immediately
    
    # 5. Alert Escalation (Phase 8)
    if status in ["WARNING", "CRITICAL"]:
        alert = {
            "machine_id": data.machine_id,
            "severity": "HIGH" if status == "CRITICAL" else "MEDIUM",
            "message": f"{status} state detected: {ai_summary}",
            "timestamp": datetime.now(timezone.utc)
        }
        await save_alert(alert)
        res = {"machine_id": data.machine_id, "status": "SAVED", "alert": alert, "prediction": prediction}
        return sanitize_data(res)
        
    res = {"machine_id": data.machine_id, "status": "SAVED", "prediction": prediction}
    return sanitize_data(res)

@app.get("/alerts", response_model=List[Dict[str, Any]])
async def get_alerts():
    # Fetch latest 20 active alerts
    alerts = await get_active_alerts(20)
    return sanitize_data(alerts)

@app.get("/dashboard-stats/{machine_id}", response_model=Dict[str, Any])
async def get_dashboard_stats(machine_id: str):
    readings = await get_latest_readings(machine_id, 20)
    health = await get_machine_health(machine_id)
    return {
        "latest_readings": readings,
        "current_health": health
    }

@app.get("/active-machines")
async def get_active_machines():
    # Phase 6: Multi-machine support
    return ["M-101", "M-102"]

@app.get("/history/{machine_id}")
async def get_long_history(machine_id: str, limit: int = 50):
    """Get long-term history for advanced visualization."""
    readings = await get_latest_readings(machine_id, limit)
    return sanitize_data(readings)

@app.get("/system-overview")
async def get_system_overview():
    """Get a high-level overview of all monitored machines."""
    machines = ["M-101", "M-102"]
    overview = []
    for m in machines:
        health = await get_machine_health(m)
        overview.append({
            "machine_id": m,
            "status": health.get("health_status", "UNKNOWN") if health else "OFFLINE",
            "probability": health.get("failure_probability", 0) if health else 0
        })
    return sanitize_data(overview)

@app.post("/assistant/query")
async def handle_assistant_query(query: Dict[str, str] = Body(...)):
    # Phase 5: Talk to Gemini assistant
    machine_id = query.get("machine_id", "M-101")
    health = await get_machine_health(machine_id)
    answer = await answer_user_query(query.get("text", ""), health)
    return {"answer": answer}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
