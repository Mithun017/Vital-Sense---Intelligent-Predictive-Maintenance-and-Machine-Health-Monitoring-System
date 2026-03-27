import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
print(f"Testing Key: {api_key[:5]}...{api_key[-5:]}")

genai.configure(api_key=api_key)

try:
    print("Listing models...")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error listing models: {e}")

try:
    print("\nTesting simple generation with gemini-pro-latest...")
    model = genai.GenerativeModel('gemini-pro-latest')
    response = model.generate_content("Hello, respond with 'OK' if you see this.")
    print(f"Pro Latest Response: {response.text}")
except Exception as e:
    print(f"Pro Latest failed: {e}")

try:
    print("\nTesting simple generation with gemini-flash-latest...")
    model = genai.GenerativeModel('gemini-flash-latest')
    response = model.generate_content("Hello, respond with 'OK' if you see this.")
    print(f"Flash Latest Response: {response.text}")
except Exception as e:
    print(f"Flash Latest failed: {e}")
