"""
Test the query logging functionality
Run this AFTER creating the query_logs table in Supabase
"""
import requests
import time
import json

API_URL = "http://localhost:8000"

print("=" * 80)
print("🧪 TESTING QUERY LOGGING SYSTEM")
print("=" * 80)

# Test queries
test_queries = [
    "What are the symptoms of diabetes?",
    "What is the Tdap vaccination schedule?",
    "How is hypertension treated?"
]

print("\n1️⃣ Sending test queries...\n")

for i, query in enumerate(test_queries, 1):
    print(f"   Query {i}: \"{query}\"")
    
    try:
        response = requests.post(f"{API_URL}/query", json={
            "query": query,
            "top_k": 3
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success - {len(data['contexts'])} contexts found")
        else:
            print(f"   ❌ Failed - Status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    time.sleep(0.5)  # Small delay between requests

print("\n2️⃣ Fetching query logs...\n")

try:
    response = requests.get(f"{API_URL}/query-logs", params={"limit": 10})
    
    if response.status_code == 200:
        data = response.json()
        
        if "error" in data:
            print(f"❌ {data['error']}")
            print(f"💡 {data['message']}")
            print("\n⚠️ You need to create the query_logs table first!")
            print("Run: python scripts/create_query_logs_table.py")
        else:
            print(f"✅ Query logs retrieved successfully!")
            print(f"\n📊 Summary:")
            print(f"   Total Queries: {data['total_queries']}")
            print(f"   Successful: {data['successful']}")
            print(f"   Failed: {data['failed']}")
            print(f"   Avg Contexts: {data['average_contexts_found']}")
            
            print(f"\n📋 Recent logs:")
            for log in data['logs'][:5]:
                query = log['query'][:60] + "..." if len(log['query']) > 60 else log['query']
                contexts = log.get('contexts_found', 0)
                success = "✅" if log.get('success') else "❌"
                print(f"   {success} \"{query}\" - {contexts} contexts")
            
            print(f"\n✅ QUERY LOGGING IS WORKING! ✅")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)

except requests.exceptions.ConnectionError:
    print("❌ Cannot connect to API server")
    print("💡 Make sure the server is running: python rag_api.py")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 80)
print("For more options, run: python view_query_logs.py")
print("=" * 80)
