"""
Test the new RAG query API
"""
import requests
import json

# Test query
query_data = {
    "query": "What are the symptoms of heart disease?",
    "top_k": 3
}

print("=" * 70)
print("🧪 Testing RAG Query API")
print("=" * 70)
print(f"\nQuery: {query_data['query']}")
print(f"Top K: {query_data['top_k']}\n")

response = requests.post(
    "http://127.0.0.1:8000/query",
    json=query_data
)

print(f"Status Code: {response.status_code}\n")

if response.status_code == 200:
    result = response.json()
    
    print("=" * 70)
    print("📝 ANSWER")
    print("=" * 70)
    print(result["answer"])
    
    print("\n" + "=" * 70)
    print(f"📚 CONTEXTS ({len(result['contexts'])} retrieved)")
    print("=" * 70)
    for i, context in enumerate(result["contexts"], 1):
        print(f"\n{i}. {context[:200]}...")
    
    print("\n" + "=" * 70)
    print("✅ RAG Query Test Successful!")
    print("=" * 70)
else:
    print(f"❌ Error: {response.text}")
