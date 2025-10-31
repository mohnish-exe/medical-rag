"""
Quick test to verify Cohere API key is working
"""
import aiohttp
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
COHERE_MODEL = "command-r-plus-08-2024"

async def test_cohere():
    """Test Cohere API with a simple prompt"""
    
    print("=" * 60)
    print("🔍 Testing Cohere API Integration")
    print("=" * 60)
    
    if not COHERE_API_KEY:
        print("❌ COHERE_API_KEY not set in .env file!")
        return
    
    print(f"\n✅ API Key loaded: {COHERE_API_KEY[:20]}...{COHERE_API_KEY[-10:]}")
    print(f"✅ Model: {COHERE_MODEL}")
    
    # Test prompt
    test_prompt = "What is diabetes? Answer in 2-3 sentences."
    print(f"\n📝 Test Prompt: {test_prompt}")
    
    # API endpoint
    url = "https://api.cohere.ai/v1/chat"
    
    headers = {
        "Authorization": f"Bearer {COHERE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": COHERE_MODEL,
        "message": test_prompt,
        "temperature": 0.3,
        "max_tokens": 100,
        "k": 0,
        "p": 0.75
    }
    
    print(f"\n🚀 Sending request to Cohere API...")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as resp:
                print(f"\n📊 Response Status: {resp.status}")
                
                if resp.status == 200:
                    data = await resp.json()
                    
                    # Extract text from Cohere Chat API response
                    if "text" in data:
                        text = data["text"].strip()
                        if text:
                            print(f"\n✅ Cohere Response:")
                            print("-" * 60)
                            print(text)
                            print("-" * 60)
                            print("\n🎉 Cohere API is working correctly!")
                            return
                    
                    print(f"⚠️ Unexpected response structure: {data}")
                
                else:
                    error_text = await resp.text()
                    print(f"\n❌ API Error:")
                    print(error_text)
                    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_cohere())
