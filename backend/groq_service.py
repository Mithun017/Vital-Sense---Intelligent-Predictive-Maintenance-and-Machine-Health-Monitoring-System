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

# Primary model for industrial reasoning
MODEL = "llama-3.3-70b-versatile"

async def generate_health_summary(machine_id: str, sensor_data: Dict[str, Any], status: str):
    """
    Use Groq (Llama-3) to generate a human-friendly health summary.
    """
    if not client:
        return "Groq AI is not configured. (Check GROQ_API_KEY in .env)"

    prompt = f"""
    You are an expert industrial maintenance assistant.
    Analyze the following machine data and provide a concise, natural language summary:
    
    Machine ID: {machine_id}
    Current Status: {status}
    Sensor Data:
    - Temperature: {sensor_data.get('temperature')}°C
    - Vibration: {sensor_data.get('vibration')} mm/s
    - Motor Load: {sensor_data.get('current')}A
    
    Summarize what this means for the machine and suggest a quick action if necessary.
    Keep it professional and actionable (max 2 sentences).
    """
    
    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        return completion.choices[0].message.content
    except Exception as e:
        # Fallback to a smaller/faster model if 70B is hit
        try:
            fallback = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100
            )
            return fallback.choices[0].message.content
        except:
            return f"AI Summary: Monitoring active. (Reasoning engine paused: {str(e)})"

async def answer_user_query(query: str, last_known_state: Dict[str, Any]):
    """
    Answer user queries about the machine health using Groq.
    """
    if not client:
        return "I'm sorry, I cannot answer queries without a configured Groq API key."

    prompt = f"""
    You are Vital Sense AI, an autonomous predictive maintenance assistant.
    The user is asking: "{query}"
    The current machine state is: {last_known_state}
    Provide a helpful, technical yet easy-to-understand answer based on this state.
    """
    
    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return completion.choices[0].message.content
    except Exception:
        try:
            fallback = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[{"role": "user", "content": prompt}]
            )
            return fallback.choices[0].message.content
        except:
            return "AI Assistant is experiencing connectivity issues with Groq Cloud. Please check your API key."
