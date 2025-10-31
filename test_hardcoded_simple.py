"""
Test hardcoded contexts with FastAPI TestClient
"""
from fastapi.testclient import TestClient
import sys
sys.path.insert(0, '.')

from rag_api import app

def test_hardcoded():
    print("=" * 80)
    print("🧪 TESTING HARDCODED CONTEXTS")
    print("=" * 80)
    
    client = TestClient(app)
    
    # Test 1: Question that's in the CSV with hardcoded context
    print("\n" + "="*80)
    print("TEST 1: Creatine Question (Should have hardcoded context from CSV)")
    print("="*80)
    
    response1 = client.post("/query", json={
        "query": "Creatine is synthesized from:\n\nA. amino acids in the muscles.\nB. amino acids in the liver.\nC. amino acids in the kidneys.\nD. creatinine in the kidneys.",
        "top_k": 5
    })
    
    result1 = response1.json()
    print(f"✅ Status: {response1.status_code}")
    print(f"📊 Contexts: {len(result1.get('contexts', []))}")
    print(f"\n🎯 Answer:\n{'-'*60}\n{result1['answer']}\n{'-'*60}")
    
    if result1.get('contexts'):
        for i, ctx in enumerate(result1['contexts'][:3], 1):
            print(f"\nContext {i}: {ctx}")
    else:
        print("\n❌ NO CONTEXTS!")
    
    # Test 2: Question NOT in CSV (should generate context via Cohere)
    print("\n\n" + "="*80)
    print("TEST 2: Random MCQ (NOT in CSV, should generate context)")
    print("="*80)
    
    response2 = client.post("/query", json={
        "query": "Which vitamin is essential for blood clotting?\n\nA. Vitamin A\nB. Vitamin K\nC. Vitamin C\nD. Vitamin D",
        "top_k": 5
    })
    
    result2 = response2.json()
    print(f"✅ Status: {response2.status_code}")
    print(f"📊 Contexts: {len(result2.get('contexts', []))}")
    print(f"\n🎯 Answer:\n{'-'*60}\n{result2['answer']}\n{'-'*60}")
    
    if result2.get('contexts'):
        for i, ctx in enumerate(result2['contexts'][:3], 1):
            print(f"\nContext {i}: {ctx}")
    else:
        print("\n❌ NO CONTEXTS!")

if __name__ == "__main__":
    test_hardcoded()
