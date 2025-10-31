"""
Quick Manual Test - API Format Verification
Run this while the server is running in another terminal
"""

import requests
import json

BASE_URL = "http://localhost:8000"

print("="*70)
print("API FORMAT COMPLIANCE VERIFICATION")
print("="*70)

# Test 1: Valid request
print("\n✅ TEST 1: Valid Request (both required fields)")
print("-"*70)
payload = {"query": "What is diabetes?", "top_k": 3}
print(f"Request: {json.dumps(payload, indent=2)}")

try:
    response = requests.post(f"{BASE_URL}/query", json=payload, timeout=30)
    print(f"\nStatus: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"✅ SUCCESS")
        print(f"\nResponse keys: {list(result.keys())}")
        print(f"Answer type: {type(result['answer'])}")
        print(f"Contexts type: {type(result['contexts'])}")
        print(f"Number of contexts: {len(result['contexts'])}")
        print(f"\nAnswer preview: {result['answer'][:150]}...")
except requests.exceptions.ConnectionError:
    print("❌ Server not running. Start with: python rag_api.py")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Missing top_k
print("\n\n❌ TEST 2: Missing top_k (should fail with 422)")
print("-"*70)
payload = {"query": "What is diabetes?"}
print(f"Request: {json.dumps(payload, indent=2)}")

try:
    response = requests.post(f"{BASE_URL}/query", json=payload, timeout=30)
    print(f"\nStatus: {response.status_code}")
    if response.status_code == 422:
        print("✅ CORRECTLY REJECTED - top_k is required")
        error = response.json()
        print(f"Error: {error['detail'][0]['msg']}")
    else:
        print("❌ FAILED - Should have been rejected")
except requests.exceptions.ConnectionError:
    print("❌ Server not running")
except Exception as e:
    print(f"Error: {e}")

# Test 3: Invalid type
print("\n\n❌ TEST 3: Invalid top_k type (should fail with 422)")
print("-"*70)
payload = {"query": "What is diabetes?", "top_k": "three"}
print(f"Request: {json.dumps(payload, indent=2)}")

try:
    response = requests.post(f"{BASE_URL}/query", json=payload, timeout=30)
    print(f"\nStatus: {response.status_code}")
    if response.status_code == 422:
        print("✅ CORRECTLY REJECTED - top_k must be integer")
        error = response.json()
        print(f"Error: {error['detail'][0]['msg']}")
    else:
        print("❌ FAILED - Should have been rejected")
except requests.exceptions.ConnectionError:
    print("❌ Server not running")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print("API Format: Request {\"query\": str, \"top_k\": int}")
print("            Response {\"answer\": str, \"contexts\": [str]}")
print("\n✅ Both query and top_k are REQUIRED (no defaults)")
print("✅ FastAPI/Pydantic validates all requests automatically")
print("✅ Invalid requests return HTTP 422 with error details")
print("="*70)
