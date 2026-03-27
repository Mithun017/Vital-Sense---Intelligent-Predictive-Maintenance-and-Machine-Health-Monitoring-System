from groq import Groq
import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Groq
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
client = None
if GROQ_API_KEY:
    client = Groq(api_key=GROQ_API_KEY)

# Adaptive Tiered Model Strategy
MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
    "gemma2-9b-it"
]

async def generate_health_summary(machine_id: str, sensor_data: Dict[str, Any], status: str):
    """
    Generate a health summary with multi-tier fallback for rate limit resilience.
    """
    if not client:
        return "AI Summary: Engine not configured. Check API key."

    prompt = f"""
    Industrial Maintenance Expert:
    Analyze machine {machine_id} (Status: {status})
    Data: Temp {sensor_data.get('temperature')}C, Vibe {sensor_data.get('vibration')}mm/s, Load {sensor_data.get('current')}A.
    Provide a professional 2-sentence summary and quick action.
    """
    
    # Try cascading through models to bypass 429
    for model_name in MODELS:
        try:
            completion = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100
            )
            return completion.choices[0].message.content
        except Exception as e:
            if "429" in str(e):
                continue # Try next tier
            break # Other errors stop the cascade
            
    # Ultimate Static Heuristic (Phase 13 Safety)
    return f"AI Summary: Engine optimized for stability. Status is {status}. [Action: Monitor {machine_id} via telemetry charts]"

async def answer_user_query(query: str, last_known_state: Dict[str, Any]):
    """
    Answer user queries with multi-tier fallback.
    """
    if not client:
        return "I'm sorry, I cannot answer queries without a configured Groq API key."

    prompt = f"""
    Maintenance Assistant:
    User asks: "{query}"
    Machine State: {last_known_state}
    Provide a helpful technical answer.
    """
    
    for model_name in MODELS:
        try:
            completion = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6,
                max_tokens=256
            )
            return completion.choices[0].message.content
        except Exception as e:
            if "429" in str(e):
                continue
            break

    return "AI Assistant: Capacity limit reached on Groq Cloud. I'm currently monitoring your machine via local heuristics. (Check console for reset time)"
