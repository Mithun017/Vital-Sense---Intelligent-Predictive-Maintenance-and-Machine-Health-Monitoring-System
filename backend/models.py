from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import List, Optional

class SensorData(BaseModel):
    machine_id: str
    temperature: float
    vibration: float
    current: float
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class PredictionResponse(BaseModel):
    machine_id: str
    health_status: str  # NORMAL, WARNING, CRITICAL
    failure_probability: float
    estimated_rul: Optional[float] = None
    timestamp: datetime

class Alert(BaseModel):
    machine_id: str
    severity: str  # LOW, MEDIUM, HIGH
    message: str
    timestamp: datetime
