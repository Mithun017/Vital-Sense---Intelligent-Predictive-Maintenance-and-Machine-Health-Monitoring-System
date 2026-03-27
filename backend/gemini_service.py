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
    # Using 'gemini-1.5-flash' which is widely available
    MODEL = genai.GenerativeModel('gemini-1.5-flash')
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
        # Prioritize 1.5-flash for performance and reasoning
        response = await MODEL.generate_content_async(prompt)
        return response.text
    except Exception as e:
        # Fallback in case of model availability issues
        try:
            fallback_model = genai.GenerativeModel('gemini-pro')
            response = await fallback_model.generate_content_async(prompt)
            return response.text
        except:
             return f"AI Summary Error: {str(e)}"

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
        response = await MODEL.generate_content_async(prompt)
        return response.text
    except Exception as e:
        try:
            fallback_model = genai.GenerativeModel('gemini-pro')
            response = await fallback_model.generate_content_async(prompt)
            return response.text
        except:
            return f"AI Assistant Error: {str(e)}"
