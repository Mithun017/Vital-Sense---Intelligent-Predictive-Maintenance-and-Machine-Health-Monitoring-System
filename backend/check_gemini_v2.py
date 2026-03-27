import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=key)

test_models = ['gemini-flash-latest', 'gemini-pro-latest', 'gemini-2.0-flash', 'gemini-1.5-flash']

for m_name in test_models:
    print(f"\n--- Testing {m_name} ---")
    try:
        model = genai.GenerativeModel(m_name)
        response = model.generate_content("Say hello")
        print(f"SUCCESS: {response.text}")
        break
    except Exception as e:
        print(f"FAILED: {str(e)}")
