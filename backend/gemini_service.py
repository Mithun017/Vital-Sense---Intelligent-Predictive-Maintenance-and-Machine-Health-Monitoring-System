import google.generativeai as genai
import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    # Using 'gemini-flash-latest' which was verified via diagnostics
    MODEL = genai.GenerativeModel('gemini-flash-latest')
else:
    MODEL = None

async def generate_health_summary(machine_id: str, sensor_data: Dict[str, Any], status: str):
    """
    Use Gemini to generate a human-friendly health summary.
    """
    if not MODEL:
        return "Gemini AI is not configured. (Check GEMINI_API_KEY)"

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
        # 1. Primary: gemini-flash-latest
        response = await MODEL.generate_content_async(prompt)
        return response.text
    except Exception:
        try:
            # 2. Secondary: gemini-pro-latest
            fallback_1 = genai.GenerativeModel('gemini-pro-latest')
            response = await fallback_1.generate_content_async(prompt)
            return response.text
        except Exception:
             return "AI Summary Error: Model availability issues. Please check your API key quota."

async def answer_user_query(query: str, last_known_state: Dict[str, Any]):
    """
    Answer user queries about the machine health using Gemini.
    """
    if not MODEL:
        return "I'm sorry, I cannot answer queries without a configured Gemini API key."

    prompt = f"""
    The user is asking: "{query}"
    The current machine state is: {last_known_state}
    Provide a helpful, technical yet easy-to-understand answer based on this state.
    """
    
    try:
        # 1. Primary
        response = await MODEL.generate_content_async(prompt)
        return response.text
    except Exception:
        try:
            # 2. Secondary
            fallback_1 = genai.GenerativeModel('gemini-pro-latest')
            response = await fallback_1.generate_content_async(prompt)
            return response.text
        except Exception:
            return "AI Assistant Error: Connectivity issue with Gemini models. Check your API settings."
