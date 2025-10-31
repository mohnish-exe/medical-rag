"""
Test RAG query to verify it searches across all documents
"""
import requests
import json

# Server URL
BASE_URL = "http://localhost:8000"

# Test query
test_query = {
    "query": "What is the recommended adult immunization schedule for Tdap?",
    "top_k": 3
}

print("=" * 70)
print("RAG QUERY TEST")
print("=" * 70)
print(f"\nQuery: {test_query['query']}")
print(f"Top K: {test_query['top_k']}")
print("\n" + "=" * 70)

try:
    # Send POST request to /query endpoint
    response = requests.post(
        f"{BASE_URL}/query",
        json=test_query,
        headers={"Content-Type": "application/json"}
    )
    
    # Check response status
    if response.status_code == 200:
        result = response.json()
        
        print("\n✓ Query successful!")
        print("\n" + "=" * 70)
        print("ANSWER:")
        print("=" * 70)
        print(result.get("answer", "No answer provided"))
        
        print("\n" + "=" * 70)
        print("CONTEXTS (Sources):")
        print("=" * 70)
        
        contexts = result.get("contexts", [])
        print(f"\nFound {len(contexts)} context(s):\n")
        
        # Track which documents are referenced
        documents_found = set()
        
        for i, context in enumerate(contexts, 1):
            print(f"\n--- Context {i} ---")
            # Extract document name from context (format: [DocumentName | Page X])
            if context.startswith("["):
                doc_info = context.split("]")[0][1:]
                doc_name = doc_info.split("|")[0].strip()
                documents_found.add(doc_name)
                print(f"Document: {doc_name}")
            print(context[:500] + "..." if len(context) > 500 else context)
        
        print("\n" + "=" * 70)
        print("DOCUMENT COVERAGE:")
        print("=" * 70)
        print(f"Documents referenced: {len(documents_found)}")
        for doc in sorted(documents_found):
            print(f"  - {doc}")
        
        print("\n" + "=" * 70)
        print("VERDICT:")
        print("=" * 70)
        if len(documents_found) > 1:
            print("✓ SUCCESS: Query searched across MULTIPLE documents!")
            print("  RAG is working correctly across all indexed data.")
        elif len(documents_found) == 1:
            print("⚠ WARNING: Only 1 document referenced")
            print("  This might be expected if the query topic is specific,")
            print("  or could indicate a search issue.")
        else:
            print("✗ FAIL: No documents found")
        
    else:
        print(f"\n✗ Query failed with status code: {response.status_code}")
        print(f"Error: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("\n✗ ERROR: Could not connect to server")
    print("Make sure the server is running: python rag_api.py")
except Exception as e:
    print(f"\n✗ ERROR: {e}")

print("\n" + "=" * 70)
