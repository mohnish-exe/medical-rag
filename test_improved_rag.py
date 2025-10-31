"""
Test script to demonstrate improved RAG accuracy and relevance
"""
import requests
import json

API_URL = "http://localhost:8000/query"

# Test queries with different complexities
test_queries = [
    {
        "query": "What is the recommended adult immunization schedule for Tdap?",
        "top_k": 5,
        "description": "Test: Medical abbreviation expansion (Tdap → tetanus, diphtheria, pertussis)"
    },
    {
        "query": "What are the diagnostic criteria for MI?",
        "top_k": 5,
        "description": "Test: Abbreviation expansion (MI → myocardial infarction, heart attack)"
    },
    {
        "query": "How is chronic kidney disease managed?",
        "top_k": 5,
        "description": "Test: General medical query without abbreviations"
    }
]

print("=" * 80)
print("🧪 TESTING IMPROVED RAG SYSTEM")
print("=" * 80)
print("\nImprovements implemented:")
print("✓ Query enhancement with medical abbreviation expansion")
print("✓ Advanced relevance scoring (position, density, header weight)")
print("✓ Smart text extraction (complete sentences)")
print("✓ Context diversity (avoid duplicate pages)")
print("✓ Enhanced prompt with few-shot examples")
print("✓ Increased token limit (600) for comprehensive answers")
print("=" * 80)

for i, test in enumerate(test_queries, 1):
    print(f"\n{'=' * 80}")
    print(f"TEST {i}: {test['description']}")
    print(f"{'=' * 80}")
    print(f"Query: {test['query']}")
    print(f"Top K: {test['top_k']}")
    
    try:
        response = requests.post(API_URL, json={
            "query": test["query"],
            "top_k": test["top_k"]
        })
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"\n{'─' * 80}")
            print("📝 ANSWER:")
            print(f"{'─' * 80}")
            print(data["answer"])
            
            print(f"\n{'─' * 80}")
            print(f"📚 RETRIEVED CONTEXTS ({len(data['contexts'])} chunks):")
            print(f"{'─' * 80}")
            
            # Analyze context diversity
            doc_sources = {}
            for ctx in data["contexts"]:
                # Extract document name from context
                if '[' in ctx and '|' in ctx:
                    doc_part = ctx.split('|')[0].strip('[').strip()
                    doc_sources[doc_part] = doc_sources.get(doc_part, 0) + 1
            
            print(f"\n📊 Source Documents:")
            for doc, count in doc_sources.items():
                print(f"  • {doc}: {count} chunk(s)")
            
            print(f"\n📄 Context Previews:")
            for j, ctx in enumerate(data["contexts"], 1):
                lines = ctx.split('\n')
                header = lines[0] if lines else "Unknown"
                preview = lines[1][:100] + "..." if len(lines) > 1 else ""
                print(f"  {j}. {header}")
                print(f"     {preview}")
            
            print(f"\n✅ Query completed successfully")
            
        else:
            print(f"\n❌ Error: {response.status_code}")
            print(response.text)
    
    except Exception as e:
        print(f"\n❌ Exception: {e}")

print(f"\n{'=' * 80}")
print("🎯 TEST SUMMARY")
print(f"{'=' * 80}")
print("Check the answers above to verify:")
print("1. ✓ Abbreviations were expanded (Tdap, MI)")
print("2. ✓ Answers are comprehensive with citations")
print("3. ✓ Contexts are from relevant documents")
print("4. ✓ Complete sentences (not truncated mid-sentence)")
print("5. ✓ Diverse sources (multiple documents when relevant)")
print(f"{'=' * 80}")
