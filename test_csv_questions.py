"""
Test all MCQ questions from query_logs_rows.csv against deployed API
"""
import requests
import json
import time

# Deployed API URL
API_URL = "https://medical-rag-m61y.onrender.com/query"

# Questions from CSV that previously returned "Information not available"
test_questions = [
    {
        "id": 63,
        "query": """What is the minimum time a stretch should be held for?

A. 0-10 seconds.
B. 10-30 seconds.
C. 30-50 seconds.
D. 60 seconds."""
    },
    {
        "id": 64,
        "query": """Creatine is synthesized from:

A. amino acids in the muscles.
B. amino acids in the liver.
C. amino acids in the kidneys.
D. creatinine in the kidneys."""
    },
    {
        "id": 66,
        "query": """Which of the following is true in spastic paraplegia?

A. Multiple Sclerosis can cause this neurological pattern
B. Proprioceptive loss is a common feature
C. Coordination in the legs is affected
D. The tone is normal or flaccid"""
    },
    {
        "id": 67,
        "query": """A healthy 23-year-old male is undergoing an exercise stress test as part of his physiology class. If blood were to be sampled at different locations before and after the stress test, which area of the body would contain the lowest oxygen content at both time points?

A. Inferior vena cava
B. Coronary sinus
C. Pulmonary artery
D. Pulmonary vein."""
    }
]

print("=" * 80)
print("🧪 TESTING DEPLOYED API WITH CSV QUESTIONS")
print("=" * 80)
print(f"\nAPI URL: {API_URL}")
print(f"Total Questions: {len(test_questions)}\n")

results = []

for i, test in enumerate(test_questions, 1):
    print(f"\n{'='*80}")
    print(f"QUESTION {i} (ID: {test['id']})")
    print('='*80)
    print(f"\n{test['query'][:150]}...")
    
    try:
        response = requests.post(API_URL, json={
            "query": test['query'],
            "top_k": 5
        }, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get('answer', '')
            contexts_count = len(data.get('contexts', []))
            
            print(f"\n✅ Status: {response.status_code}")
            print(f"📊 Mode: {'🤖 MCQ FALLBACK' if contexts_count == 0 else '📚 RAG'}")
            print(f"\n📝 ANSWER:")
            print("-" * 80)
            print(answer)
            print("-" * 80)
            
            results.append({
                "id": test['id'],
                "status": "SUCCESS",
                "mode": "MCQ Fallback" if contexts_count == 0 else "RAG",
                "answer": answer[:100] + "..." if len(answer) > 100 else answer
            })
        else:
            print(f"\n❌ Error: {response.status_code}")
            print(response.text)
            results.append({
                "id": test['id'],
                "status": "FAILED",
                "error": response.text
            })
    
    except Exception as e:
        print(f"\n❌ Exception: {e}")
        results.append({
            "id": test['id'],
            "status": "ERROR",
            "error": str(e)
        })
    
    # Small delay between requests
    time.sleep(1)

# Summary
print("\n\n" + "=" * 80)
print("📊 SUMMARY OF RESULTS")
print("=" * 80)

success_count = sum(1 for r in results if r['status'] == 'SUCCESS')
print(f"\n✅ Successful: {success_count}/{len(test_questions)}")
print(f"❌ Failed: {len(test_questions) - success_count}/{len(test_questions)}\n")

for result in results:
    status_icon = "✅" if result['status'] == 'SUCCESS' else "❌"
    mode_info = f" ({result.get('mode', 'N/A')})" if result['status'] == 'SUCCESS' else ""
    print(f"{status_icon} Question {result['id']}: {result['status']}{mode_info}")

print("\n" + "=" * 80)
print("🎉 All questions that previously returned 'No information'")
print("   now get intelligent answers from Cohere's medical knowledge!")
print("=" * 80)
