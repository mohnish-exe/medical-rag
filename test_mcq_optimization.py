"""
Test script for MCQ query extraction optimization
"""
import requests
import json
import time

# Test cases
test_cases = [
    {
        "name": "MCQ with hardcoded context (Creatine)",
        "query": """Creatine is synthesized from:

A. amino acids in the muscles.
B. amino acids in the liver.
C. amino acids in the kidneys.
D. creatinine in the kidneys.""",
        "expected_behavior": "Should use hardcoded context from CSV"
    },
    {
        "name": "MCQ without hardcoded context (Hypertension)",
        "query": """What is the primary cause of essential hypertension?

A. Kidney disease
B. Hormonal imbalance
C. Unknown (multifactorial)
D. Genetic factors only""",
        "expected_behavior": "Should extract question part and search database"
    },
    {
        "name": "Regular question (non-MCQ)",
        "query": "What causes hypertension?",
        "expected_behavior": "Should search with full query"
    }
]

def test_query(query, test_name, expected_behavior):
    """Test a single query"""
    print(f"\n{'='*80}")
    print(f"🧪 TEST: {test_name}")
    print(f"📋 Expected: {expected_behavior}")
    print(f"{'='*80}")
    
    try:
        # Make request
        url = "http://127.0.0.1:8000/query"
        payload = {
            "query": query,
            "top_k": 5
        }
        
        print(f"\n📤 Sending query...")
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        
        # Display results
        print(f"\n✅ Response received!")
        print(f"\n📊 METRICS:")
        print(f"   - Contexts returned: {len(result.get('contexts', []))}")
        print(f"   - Answer length: {len(result.get('answer', ''))} chars")
        
        print(f"\n💬 ANSWER:")
        print(f"   {result.get('answer', 'No answer')}")
        
        if result.get('contexts'):
            print(f"\n📄 CONTEXTS (showing first 2):")
            for i, ctx in enumerate(result['contexts'][:2], 1):
                preview = ctx[:150] + "..." if len(ctx) > 150 else ctx
                print(f"\n   {i}. {preview}")
        else:
            print(f"\n⚠️  NO CONTEXTS RETURNED")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ ERROR: {e}")
        return False
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("🚀 MCQ OPTIMIZATION TEST SUITE")
    print("="*80)
    
    # Check if server is running
    print("\n🔍 Checking if server is running...")
    try:
        response = requests.get("http://127.0.0.1:8000/", timeout=5)
        print("✅ Server is running!")
    except:
        print("❌ Server is not running. Please start it with:")
        print("   python -m uvicorn rag_api:app --reload --port 8000")
        return
    
    # Run tests
    results = []
    for test in test_cases:
        time.sleep(1)  # Brief pause between tests
        success = test_query(
            test["query"],
            test["name"],
            test["expected_behavior"]
        )
        results.append((test["name"], success))
    
    # Summary
    print(f"\n\n{'='*80}")
    print("📋 TEST SUMMARY")
    print("="*80)
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    print("="*80)

if __name__ == "__main__":
    main()
