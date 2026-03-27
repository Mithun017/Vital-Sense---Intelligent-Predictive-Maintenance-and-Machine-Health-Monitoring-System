import asyncio
from gemini_service import get_ai_response

async def test():
    print("Testing multi-provider fallback...")
    res = await get_ai_response("Explain why a vibration of 0.8mm/s is risky for a motor.")
    print(f"AI Response: {res}")

if __name__ == "__main__":
    asyncio.run(test())
