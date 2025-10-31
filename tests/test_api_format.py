"""
Test API Format Compliance
Verifies exact JSON structure matches specification:
- Request: {"query": str (required), "top_k": int (required)}
- Response: {"answer": str, "contexts": [str, ...]}
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_valid_request():
    """Test 1: Valid request with both required fields"""
    print("\n" + "="*60)
    print("TEST 1: Valid Request (both fields provided)")
    print("="*60)
    
    payload = {
        "query": "What are the symptoms of heart failure?",
        "top_k": 3
    }
    
    print(f"\n📤 Sending: {json.dumps(payload, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/query", json=payload)
    
    print(f"\n📥 Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ SUCCESS - Response received")
        print(f"\n📄 Response structure:")
        print(f"  - 'answer' field: {type(result.get('answer'))} ({len(result.get('answer', ''))} chars)")
        print(f"  - 'contexts' field: {type(result.get('contexts'))} ({len(result.get('contexts', []))} items)")
        print(f"\n📝 Answer preview: {result['answer'][:200]}...")
        print(f"\n📚 Contexts preview:")
        for i, ctx in enumerate(result['contexts'][:2], 1):
            print(f"  {i}. {ctx[:100]}...")
        return True
    else:
        print(f"❌ FAILED - {response.text}")
        return False

def test_missing_top_k():
    """Test 2: Request missing top_k (should fail)"""
    print("\n" + "="*60)
    print("TEST 2: Missing top_k (should be rejected)")
    print("="*60)
    
    payload = {
        "query": "What are the symptoms of heart failure?"
        # top_k intentionally omitted
    }
    
    print(f"\n📤 Sending: {json.dumps(payload, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/query", json=payload)
    
    print(f"\n📥 Status Code: {response.status_code}")
    
    if response.status_code == 422:  # Validation error
        print("✅ SUCCESS - Request correctly rejected (validation error)")
        print(f"\n📄 Error details: {response.json()}")
        return True
    elif response.status_code == 200:
        print("❌ FAILED - Request should have been rejected but was accepted")
        return False
    else:
        print(f"⚠️  Unexpected status code: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def test_missing_query():
    """Test 3: Request missing query (should fail)"""
    print("\n" + "="*60)
    print("TEST 3: Missing query (should be rejected)")
    print("="*60)
    
    payload = {
        "top_k": 3
        # query intentionally omitted
    }
    
    print(f"\n📤 Sending: {json.dumps(payload, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/query", json=payload)
    
    print(f"\n📥 Status Code: {response.status_code}")
    
    if response.status_code == 422:  # Validation error
        print("✅ SUCCESS - Request correctly rejected (validation error)")
        print(f"\n📄 Error details: {response.json()}")
        return True
    elif response.status_code == 200:
        print("❌ FAILED - Request should have been rejected but was accepted")
        return False
    else:
        print(f"⚠️  Unexpected status code: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def test_invalid_top_k_type():
    """Test 4: top_k with wrong type (should fail)"""
    print("\n" + "="*60)
    print("TEST 4: Invalid top_k type (string instead of int)")
    print("="*60)
    
    payload = {
        "query": "What are the symptoms of heart failure?",
        "top_k": "three"  # String instead of int
    }
    
    print(f"\n📤 Sending: {json.dumps(payload, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/query", json=payload)
    
    print(f"\n📥 Status Code: {response.status_code}")
    
    if response.status_code == 422:  # Validation error
        print("✅ SUCCESS - Request correctly rejected (type validation error)")
        print(f"\n📄 Error details: {response.json()}")
        return True
    elif response.status_code == 200:
        print("❌ FAILED - Request should have been rejected but was accepted")
        return False
    else:
        print(f"⚠️  Unexpected status code: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def test_response_format():
    """Test 5: Validate response format exactly matches specification"""
    print("\n" + "="*60)
    print("TEST 5: Response Format Validation")
    print("="*60)
    
    payload = {
        "query": "What is diabetes?",
        "top_k": 2
    }
    
    print(f"\n📤 Sending: {json.dumps(payload, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/query", json=payload)
    
    if response.status_code == 200:
        result = response.json()
        
        # Check exact structure
        checks = []
        
        # Must have exactly 2 fields
        if len(result.keys()) == 2:
            checks.append(("✅", "Exactly 2 fields in response"))
        else:
            checks.append(("❌", f"Expected 2 fields, got {len(result.keys())}: {list(result.keys())}"))
        
        # Must have 'answer' field (string)
        if 'answer' in result and isinstance(result['answer'], str):
            checks.append(("✅", "'answer' field is string"))
        else:
            checks.append(("❌", f"'answer' field issue: {type(result.get('answer'))}"))
        
        # Must have 'contexts' field (list of strings)
        if 'contexts' in result and isinstance(result['contexts'], list):
            if all(isinstance(ctx, str) for ctx in result['contexts']):
                checks.append(("✅", "'contexts' field is list of strings"))
            else:
                checks.append(("❌", "'contexts' contains non-string items"))
        else:
            checks.append(("❌", f"'contexts' field issue: {type(result.get('contexts'))}"))
        
        # Print results
        print("\n📋 Format Validation:")
        for status, message in checks:
            print(f"  {status} {message}")
        
        all_passed = all(status == "✅" for status, _ in checks)
        
        if all_passed:
            print("\n🎉 PERFECT - Response format exactly matches specification!")
            return True
        else:
            print("\n❌ FAILED - Response format does not match specification")
            return False
    else:
        print(f"❌ FAILED - Could not get response: {response.status_code}")
        return False

if __name__ == "__main__":
    print("\n" + "="*60)
    print("API FORMAT COMPLIANCE TEST SUITE")
    print("="*60)
    print("\nSpecification:")
    print("  Request: {\"query\": str (required), \"top_k\": int (required)}")
    print("  Response: {\"answer\": str, \"contexts\": [str, ...]}")
    print("\nEnsure server is running: python rag_api.py")
    print("="*60)
    
    results = []
    
    try:
        # Run all tests
        results.append(("Valid Request", test_valid_request()))
        results.append(("Missing top_k", test_missing_top_k()))
        results.append(("Missing query", test_missing_query()))
        results.append(("Invalid top_k type", test_invalid_top_k_type()))
        results.append(("Response Format", test_response_format()))
        
        # Summary
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for test_name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} - {test_name}")
        
        print(f"\n📊 Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if passed == total:
            print("\n🎉 ALL TESTS PASSED - API format is fully compliant!")
        else:
            print(f"\n⚠️  {total - passed} test(s) failed - review issues above")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to server")
        print("Make sure the API server is running: python rag_api.py")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
