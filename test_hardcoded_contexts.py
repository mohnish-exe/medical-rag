"""
Test hardcoded contexts from CSV
"""
import requests
import json

def test_hardcoded_contexts():
    print("=" * 80)
    print("🧪 TESTING HARDCODED CONTEXTS FROM CSV")
    print("=" * 80)
    
    # Test cases: questions that are in the CSV
    test_queries = [
        {
            "name": "Creatine Synthesis (in CSV)",
            "query": "Creatine is synthesized from:\n\nA. amino acids in the muscles.\nB. amino acids in the liver.\nC. amino acids in the kidneys.\nD. creatinine in the kidneys."
        },
        {
            "name": "Stretch Duration (in CSV)",
            "query": "What is the minimum time a stretch should be held for?\n\nA. 0-10 seconds.\nB. 10-30 seconds.\nC. 30-50 seconds.\nD. 60 seconds."
        },
        {
            "name": "Morphodifferentiation (NOT in CSV)",
            "query": "Which stage of tooth development establishes crown shape?\n\nA. Initiation\nB. Proliferation\nC. Morphodifferentiation\nD. Apposition"
        }
    ]
    
    for test in test_queries:
        print(f"\n{'='*80}")
        print(f"TEST: {test['name']}")
        print('='*80)
        
        try:
            response = requests.post(
                "http://127.0.0.1:8000/query",
                json={"query": test['query'], "top_k": 5},
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                contexts = result.get('contexts', [])
                
                print(f"✅ Status: {response.status_code}")
                print(f"📊 Contexts Found: {len(contexts)}")
                
                print(f"\n🎯 Answer:")
                print("-" * 60)
                print(result['answer'][:300])
                print("-" * 60)
                
                if contexts:
                    print(f"\n📚 Contexts:")
                    for i, ctx in enumerate(contexts[:3], 1):
                        source = ctx.get('source', 'Unknown')
                        score = ctx.get('relevance_score', 'N/A')
                        content = ctx.get('content', '')[:150]
                        print(f"\n  {i}. [{source}] (Score: {score})")
                        print(f"     {content}...")
                else:
                    print(f"\n❌ NO CONTEXTS RETURNED!")
                    
            else:
                print(f"❌ Error {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"❌ Request failed: {e}")
        
        print()

if __name__ == "__main__":
    test_hardcoded_contexts()
