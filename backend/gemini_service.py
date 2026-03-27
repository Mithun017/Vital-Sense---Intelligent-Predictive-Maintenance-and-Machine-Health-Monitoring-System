import google.generativeai as genai
from groq import Groq
import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    MODEL = genai.GenerativeModel('gemini-flash-latest')
else:
    MODEL = None

# Configure Groq
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_CLIENT = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

async def get_ai_response(prompt: str):
    """
    Orchestrate multiple AI providers to get a response.
    Gemini (Primary) -> Groq (Fallback)
    """
    
    # 1. Try Gemini Models
    gemini_models = ['gemini-flash-latest', 'gemini-2.0-flash', 'gemini-pro-latest']
    for m_name in gemini_models:
        try:
            m = genai.GenerativeModel(m_name)
            # generate_content_async is not always available in all SDK versions, 
            # using sync for stability if needed, but keeping async if possible
            response = m.generate_content(prompt)
            return response.text
        except Exception as e:
            if "429" in str(e) or "404" in str(e):
                continue
            
    # 2. Try Groq (Ultra-fast Fallback)
    if GROQ_CLIENT:
        try:
            chat_completion = GROQ_CLIENT.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"AI Error (Gemini/Groq Exhausted): {str(e)}"

    return "AI Providers are offline or quota-limited. Please check API keys."

async def generate_health_summary(machine_id: str, sensor_data: Dict[str, Any], status: str):
    """
    Use multi-provider AI to generate a human-friendly health summary.
    """
    prompt = f"""
    Analyze this machine data:
    Machine: {machine_id}
    Status: {status}
    Vitals: {sensor_data}
    Provide a 1-sentence technical diagnostic summary for an engineer.
    """
    return await get_ai_response(prompt)

async def answer_user_query(query: str, last_known_state: Dict[str, Any]):
    """
    Answer user queries about the machine health using multi-provider AI.
    """
    prompt = f"""
    Context: Industrial Predictive Maintenance System
    Machine state: {last_known_state}
    User Query: "{query}"
    Provide a short, professional, and technical answer.
    """
    return await get_ai_response(prompt)
