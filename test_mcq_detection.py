"""
Test MCQ detection with fallback
"""
import asyncio
import sys
sys.path.insert(0, '.')

from rag_api import app
import aiohttp
import json

async def test_mcq_detection():
    print("=" * 80)
    print("🎯 TESTING MCQ AUTO-DETECTION")
    print("=" * 80)
    
    # Start a test client
    from fastapi.testclient import TestClient
    client = TestClient(app)
    
    test_cases = [
        {
            "name": "MCQ - Creatine Synthesis",
            "query": "Creatine is synthesized from:\n\nA. amino acids in the muscles.\nB. amino acids in the liver.\nC. amino acids in the kidneys.\nD. creatinine in the kidneys.",
            "expected_mode": "MCQ Fallback"
        },
        {
            "name": "MCQ - Oxygen Content",
            "query": "A healthy 23-year-old male is undergoing an exercise stress test. Which area would contain the lowest oxygen content?\n\nA. Inferior vena cava\nB. Coronary sinus\nC. Pulmonary artery\nD. Pulmonary vein.",
            "expected_mode": "MCQ Fallback"
        },
        {
            "name": "Regular Question - Diabetes",
            "query": "What are the treatment options for diabetes?",
            "expected_mode": "RAG Search"
        }
    ]
    
    for test in test_cases:
        print(f"\n{'='*80}")
        print(f"TEST: {test['name']}")
        print(f"Expected: {test['expected_mode']}")
        print('='*80)
        
        response = client.post("/query", json={
            "query": test['query'],
            "top_k": 3
        })
        
        result = response.json()
        
        contexts_count = len(result.get('contexts', []))
        actual_mode = "MCQ Fallback" if contexts_count == 0 and "A." in test['query'] else "RAG Search"
        
        print(f"\n✅ Status: {response.status_code}")
        print(f"📊 Contexts: {contexts_count}")
        print(f"🎯 Mode: {actual_mode}")
        print(f"\n📝 Answer Preview:")
        print("-" * 80)
        print(result['answer'][:200] + ("..." if len(result['answer']) > 200 else ""))
        print("-" * 80)
        
        if actual_mode == test['expected_mode']:
            print(f"✅ PASS - Correct mode used!")
        else:
            print(f"⚠️ UNEXPECTED - Expected {test['expected_mode']}, got {actual_mode}")

if __name__ == "__main__":
    asyncio.run(test_mcq_detection())
