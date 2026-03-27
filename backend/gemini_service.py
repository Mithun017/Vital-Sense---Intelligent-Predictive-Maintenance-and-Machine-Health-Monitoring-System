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
    # Primary model
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
    Analyze this machine data:
    Machine: {machine_id}
    Status: {status}
    Vitals: {sensor_data}
    Provide a 1-sentence technical diagnostic.
    """
    
    # Try multiple models in order of intelligence/cost
    models_to_try = [
        'gemini-flash-latest',
        'gemini-2.5-flash',
        'gemini-flash-lite-latest',
        'gemini-pro-latest'
    ]

    for m_name in models_to_try:
        try:
            m = genai.GenerativeModel(m_name)
            response = await m.generate_content_async(prompt)
            return response.text
        except Exception as e:
            err_str = str(e)
            if "429" in err_str:
                continue # Try next model or fallback to quota error
            continue
            
    return "AI Summary: API Quota Exceeded. Please check your Google AI Studio plan."

async def answer_user_query(query: str, last_known_state: Dict[str, Any]):
    """
    Answer user queries about the machine health using Gemini.
    """
    if not MODEL:
        return "I'm sorry, I cannot answer queries without a configured Gemini API key."

    prompt = f"""
    The user asks: "{query}"
    Machine state: {last_known_state}
    Provide a short, professional response.
    """
    
    models_to_try = [
        'gemini-flash-latest',
        'gemini-2.0-flash',
        'gemini-flash-lite-latest',
        'gemini-pro-latest'
    ]

    for m_name in models_to_try:
        try:
            m = genai.GenerativeModel(m_name)
            response = await m.generate_content_async(prompt)
            return response.text
        except Exception as e:
            if "429" in str(e):
                continue
            continue

    return "AI Assistant: Your API key has exceeded its free tier quota (429). Please try again later or upgrade your plan at ai.google.dev."
