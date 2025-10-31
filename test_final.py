"""
Final test demonstrating all improvements:
1. Concise, direct answers
2. Short, relevant contexts
3. Better search accuracy
"""
import requests
import json

API_URL = "http://localhost:8000/query"

test_cases = [
    {
        "query": "What is the adult Tdap vaccination schedule?",
        "top_k": 3,
        "expected": "Should find vaccination schedule from InternalMedicine"
    },
    {
        "query": "What are the symptoms of heart attack?",
        "top_k": 3,
        "expected": "Should find MI symptoms"
    },
    {
        "query": "How is hypertension treated?",
        "top_k": 3,
        "expected": "Should find HTN treatment options"
    }
]

print("=" * 80)
print("🎯 FINAL RAG SYSTEM TEST - Concise & Relevant")
print("=" * 80)

for i, test in enumerate(test_cases, 1):
    print(f"\n{'─' * 80}")
    print(f"TEST {i}: {test['query']}")
    print(f"Expected: {test['expected']}")
    print(f"{'─' * 80}")
    
    try:
        response = requests.post(API_URL, json={
            "query": test["query"],
            "top_k": test["top_k"]
        })
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"\n💬 ANSWER (should be concise & direct):")
            print(f"   {data['answer']}")
            print(f"   Length: {len(data['answer'])} chars")
            
            print(f"\n📚 CONTEXTS ({len(data['contexts'])} chunks):")
            for j, ctx in enumerate(data['contexts'], 1):
                # Show first 150 chars of each context
                preview = ctx[:150] + "..." if len(ctx) > 150 else ctx
                print(f"   {j}. {preview}")
            
            # Check quality metrics
            answer_words = len(data['answer'].split())
            has_citation = '(' in data['answer'] and 'Page' in data['answer']
            no_meta_phrases = not any(phrase in data['answer'].lower() for phrase in 
                                     ['based on the contexts', 'the contexts state', 
                                      'according to the contexts', 'the retrieved contexts'])
            
            print(f"\n✓ Quality Check:")
            print(f"   • Answer length: {answer_words} words ({'✓ Concise' if answer_words < 50 else '✗ Too long'})")
            print(f"   • Has citation: {'✓ Yes' if has_citation else '✗ No'}")
            print(f"   • Direct answer: {'✓ Yes' if no_meta_phrases else '✗ No (mentions contexts)'}")
            print(f"   • Contexts: {len(data['contexts'])} chunks")
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
    
    except Exception as e:
        print(f"❌ Exception: {e}")

print(f"\n{'=' * 80}")
print("✅ TEST COMPLETE")
print("=" * 80)
