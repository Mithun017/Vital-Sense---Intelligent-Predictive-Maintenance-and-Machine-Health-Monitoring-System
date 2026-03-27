import numpy as np
import pandas as pd
from datetime import datetime, timezone
from typing import Dict, Any, Tuple, List
from sklearn.linear_model import LinearRegression

# Thresholds for machine health status
THRESHOLDS = {
    "temperature": {"warning": 80.0, "critical": 95.0, "max": 120.0},
    "vibration": {"warning": 5.0, "critical": 8.0, "max": 15.0},
    "current": {"warning": 15.0, "critical": 22.0, "max": 40.0}
}

class AdvancedMLEngine:
    def __init__(self):
        self.history = {}  # Store recent history per machine for RUL
        self.model_version = "v1.2.0"

    def calculate_health_score(self, data: Dict[str, Any]) -> float:
        """
        Calculates a health score from 0 (failed) to 100 (perfect).
        """
        scores = []
        for feature, val in data.items():
            if feature in THRESHOLDS:
                # Simple normalization: 100 at 0, 0 at max threshold
                max_val = THRESHOLDS[feature]["max"]
                score = max(0, 100 - (val / max_val * 100))
                scores.append(score)
        return np.mean(scores) if scores else 50.0

    def predict_status_and_xai(self, sensor_data: Dict[str, Any]) -> Tuple[str, float, Dict[str, float]]:
        """
        Predict status, failure probability, and explain which features contributed most.
        """
        temp = sensor_data.get("temperature", 0)
        vibe = sensor_data.get("vibration", 0)
        curr = sensor_data.get("current", 0)
        
        # Feature importance (XAI) - Higher value means higher contribution to 'Warning/Critical'
        explanations = {
            "temperature": max(0, (temp - THRESHOLDS["temperature"]["warning"]) / 10),
            "vibration": max(0, (vibe - THRESHOLDS["vibration"]["warning"]) / 2),
            "current": max(0, (curr - THRESHOLDS["current"]["warning"]) / 5)
        }
        
        status = "NORMAL"
        failure_prob = 0.05
        
        if temp >= THRESHOLDS["temperature"]["critical"] or vibe >= THRESHOLDS["vibration"]["critical"] or curr >= THRESHOLDS["current"]["critical"]:
            status = "CRITICAL"
            failure_prob = np.random.uniform(0.8, 0.99)
        elif temp >= THRESHOLDS["temperature"]["warning"] or vibe >= THRESHOLDS["vibration"]["warning"] or curr >= THRESHOLDS["current"]["warning"]:
            status = "WARNING"
            failure_prob = np.random.uniform(0.4, 0.7)
            
        return status, failure_prob, explanations

    def estimate_rul(self, machine_id: str, current_readings: List[Dict[str, Any]]) -> float:
        """
        Estimate Remaining Useful Life (RUL) in hours using simple linear regression.
        Requires at least 5 readings to perform a trend analysis.
        """
        if len(current_readings) < 5:
            return 720.0  # Default 30 days if not enough data
            
        df = pd.DataFrame(current_readings)
        df['ts_numeric'] = pd.to_datetime(df['timestamp']).map(datetime.timestamp)
        
        # Calculate a composite health index for regression
        df['health_index'] = df.apply(lambda row: self.calculate_health_score(row), axis=1)
        
        X = df[['ts_numeric']].values
        y = df['health_index'].values
        
        model = LinearRegression().fit(X, y)
        slope = model.coef_[0]
        
        if slope >= 0:
            return 1000.0  # Improving or stable health
            
        # Target 0 health index
        current_health = y[0]
        # rul_seconds = (target_y - intercept) / slope - current_ts
        # Simplified: rul_seconds = current_health / abs(slope)
        rul_seconds = current_health / abs(slope)
        return round(rul_seconds / 3600, 1)  # Return hours

    def get_maintenance_recommendation(self, status: str, xai: Dict[str, float]) -> List[str]:
        """
        Phase 4: Smart Maintenance Recommendations based on XAI.
        """
        recs = []
        if status == "NORMAL":
            return ["No immediate action required.", "Continue regular inspection schedule."]
            
        top_contributor = max(xai, key=xai.get)
        
        if top_contributor == "temperature":
            recs = ["Check cooling system and ventilation.", "Inspect motor insulation.", "Reduce load if temperature continues to rise."]
        elif top_contributor == "vibration":
            recs = ["Check bearing lubrication.", "Inspect for mechanical imbalance.", "Tighten mounting bolts."]
        elif top_contributor == "current":
            recs = ["Inspect electrical connections.", "Check for motor winding issues.", "Verify supply voltage stability."]
            
        if status == "CRITICAL":
            recs.insert(0, "IMMEDIATE EMERGENCY SHUTDOWN RECOMMENDED")
            
        return recs

    def calculate_efficiency_metrics(self, sensor_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Phase 10: Energy & Efficiency Calculation.
        Models mechanical and electrical losses based on thermal and frictional state.
        """
        voltage = sensor_data.get("voltage", 230.0)
        current = sensor_data.get("current", 12.0)
        temp = sensor_data.get("temperature", 65.0)
        vibe = sensor_data.get("vibration", 2.0)
        
        # 1. Power Consumption (Watts)
        # Assuming P = V * I * pf (Industrial Power Factor ~0.85)
        power_factor = 0.85
        power_watts = voltage * current * power_factor
        
        # 2. Efficiency Index (%)
        # Base efficiency for a premium motor is ~96%
        # Thermal degradation: loss of ~0.1% per 5°C above nominal (65°C)
        thermal_loss = max(0, (temp - 65) * 0.02)
        # Frictional/Vibrational loss: loss of ~0.2% per 2mm/s above nominal (2mm/s)
        mechanical_loss = max(0, (vibe - 2) * 0.1)
        
        efficiency = 96.5 - thermal_loss - mechanical_loss
        
        return {
            "power_watts": round(power_watts, 2),
            "efficiency_pct": round(max(75.0, efficiency), 1),
            "voltage_v": round(voltage, 1)
        }

# Singleton instance
ENGINE = AdvancedMLEngine()
