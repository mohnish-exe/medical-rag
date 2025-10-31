"""
Quick test to verify Gemini API integration
"""
import asyncio
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.5-flash"

async def test_gemini():
    """Test Gemini API with a simple prompt"""
    
    print("=" * 60)
    print("🔍 Testing Gemini API Integration")
    print("=" * 60)
    
    if not GEMINI_API_KEY:
        print("❌ GEMINI_API_KEY not set in .env file!")
        return
    
    print(f"\n✅ API Key loaded: {GEMINI_API_KEY[:20]}...{GEMINI_API_KEY[-10:]}")
    print(f"✅ Model: {GEMINI_MODEL}")
    
    # Test prompt
    test_prompt = "What is 2 + 2? Provide a brief answer."
    
    print(f"\n📤 Sending test prompt: '{test_prompt}'")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "contents": [{
            "parts": [{
                "text": test_prompt
            }]
        }],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 100,
            "topP": 0.8,
            "topK": 10
        }
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as resp:
                print(f"\n📥 Response status: {resp.status}")
                
                if resp.status == 200:
                    data = await resp.json()
                    
                    # Extract text from Gemini response
                    if "candidates" in data and len(data["candidates"]) > 0:
                        candidate = data["candidates"][0]
                        if "content" in candidate and "parts" in candidate["content"]:
                            text = candidate["content"]["parts"][0].get("text", "")
                            print(f"\n✅ Gemini Response: {text}")
                            print("\n" + "=" * 60)
                            print("🎉 Gemini API is working correctly!")
                            print("=" * 60)
                            return True
                    
                    print("⚠️ Unexpected response structure")
                    print(f"Response: {data}")
                else:
                    error_text = await resp.text()
                    print(f"❌ API Error: {error_text}")
                    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return False

if __name__ == "__main__":
    asyncio.run(test_gemini())
