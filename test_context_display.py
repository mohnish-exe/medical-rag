"""
Test to show exactly what contexts are returned for MCQ questions
"""
import requests
import json

def test_mcq_contexts():
    print("=" * 80)
    print("🧪 TESTING MCQ CONTEXT DISPLAY")
    print("=" * 80)
    
    # Test with deployed API
    url = "https://medical-rag-m61y.onrender.com/query"
    
    mcq_query = {
        "query": "Creatine is composed of: a. fatty acids and glycerol b. amino acids in the liver c. carbohydrates and proteins d. vitamins and minerals",
        "top_k": 5
    }
    
    print(f"🔄 Testing deployed API: {url}")
    print(f"📝 Query: {mcq_query['query'][:60]}...")
    
    try:
        response = requests.post(url, json=mcq_query, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"\n✅ Response Status: {response.status_code}")
            print(f"📊 Number of contexts: {len(result.get('contexts', []))}")
            print(f"\n🎯 Answer:")
            print("-" * 60)
            print(result.get('answer', 'No answer found'))
            print("-" * 60)
            
            print(f"\n📚 Contexts Found:")
            contexts = result.get('contexts', [])
            
            if contexts:
                for i, context in enumerate(contexts, 1):
                    print(f"\n  Context {i}:")
                    print(f"    📖 Source: {context.get('source', 'Unknown')}")
                    print(f"    📄 Page: {context.get('page_number', 'Unknown')}")
                    print(f"    ⭐ Score: {context.get('relevance_score', 'Unknown')}")
                    print(f"    📝 Content: {context.get('content', '')[:100]}...")
            else:
                print("    ❌ No contexts found in response")
                
            print(f"\n📋 Full Response Structure:")
            print(json.dumps(result, indent=2)[:1000] + "..." if len(json.dumps(result, indent=2)) > 1000 else json.dumps(result, indent=2))
            
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_mcq_contexts()