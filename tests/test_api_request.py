"""
Test script to send a request to the /hackrx/run endpoint
"""
import requests
import json

# API endpoint
url = "http://127.0.0.1:8000/hackrx/run"

# Request payload
payload = {
    "documents": "https://drive.google.com/uc?export=download&id=12nq14ovXolaVKLppDNho_pPo01m3KEj5",
    "questions": [
        "What does the report say about the patient's troponin level and what does it indicate?"
    ]
}

print("=" * 60)
print("🚀 Testing API Request")
print("=" * 60)
print(f"\n📍 URL: {url}")
print(f"\n📤 Sending request...")
print(f"\nPayload:\n{json.dumps(payload, indent=2)}")

try:
    # Send POST request
    response = requests.post(url, json=payload)
    
    print(f"\n📥 Response Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ Success! Response:")
        print(json.dumps(data, indent=2))
    else:
        print("\n❌ Error Response:")
        print(response.text)
        
except Exception as e:
    print(f"\n❌ Error: {e}")

print("\n" + "=" * 60)
