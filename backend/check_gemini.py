import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
key = os.environ.get("GEMINI_API_KEY")

if not key:
    print("ERROR: GEMINI_API_KEY not found in .env")
    exit(1)

genai.configure(api_key=key)

print(f"Testing API Key: {key[:10]}...")

try:
    print("\nAvailable Models:")
    models = genai.list_models()
    for m in models:
        print(f"- {m.name} (Methods: {m.supported_generation_methods})")
    
    print("\nAttempting Test Generation (gemini-1.5-flash)...")
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Hello, respond with 'OK' if you see this.")
    print(f"RESPONSE: {response.text}")

except Exception as e:
    print(f"\nDIAGNOSTIC FAILED: {str(e)}")
