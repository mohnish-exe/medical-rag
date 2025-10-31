"""
Test API endpoint with stretch question
"""
import requests
import json

url = "http://localhost:8000/query"

data = {
    "query": "What is the minimum time a stretch should be held for?\n\nA. 0-10 seconds.\nB. 10-30 seconds.\nC. 30-50 seconds.\nD. 60 seconds.",
    "top_k": 5
}

print("=" * 80)
print("🎯 TESTING STRETCH MCQ VIA API")
print("=" * 80)
print(f"\nSending request to: {url}")
print(f"Query: {data['query'][:60]}...")

try:
    response = requests.post(url, json=data, timeout=60)
    
    print(f"\nStatus: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        
        print("\n" + "=" * 80)
        print("📝 ANSWER:")
        print("=" * 80)
        print(result['answer'])
        print("=" * 80)
        
        contexts_count = len(result.get('contexts', []))
        mode = "🤖 FALLBACK (Cohere Knowledge)" if contexts_count == 0 else "📚 RAG (Database)"
        
        print(f"\n📊 Contexts: {contexts_count}")
        print(f"Mode: {mode}")
        
        if contexts_count > 0:
            print(f"\nSample context:")
            print("-" * 80)
            print(result['contexts'][0][:150] + "...")
    else:
        print(f"Error: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("\n❌ Could not connect to server")
    print("💡 Start server with: python -m uvicorn rag_api:app --reload --port 8000")
except Exception as e:
    print(f"\n❌ Error: {e}")
