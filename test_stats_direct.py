"""
Direct database test to check what's actually in the database
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from core.supabase_client import supabase

print("=" * 70)
print("DIRECT DATABASE STATS TEST")
print("=" * 70)

# Test 1: Total chunks
print("\n1. Testing total chunks count...")
try:
    total_result = supabase.table("document_chunks").select("id", count="exact").limit(1).execute()
    print(f"   ✓ Total chunks: {total_result.count:,}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 2: Check each document individually
print("\n2. Checking each document individually...")
documents = ['Anatomy&Physiology', 'Cardiology', 'Dentistry', 'EmergencyMedicine', 
             'Gastrology', 'General', 'InfectiousDisease', 'InternalMedicine', 'Nephrology']

found_docs = []
chunks_per_doc = {}

for doc in documents:
    try:
        count_result = supabase.table("document_chunks")\
            .select("id", count="exact")\
            .eq("document_name", doc)\
            .limit(1)\
            .execute()
        
        if count_result.count > 0:
            found_docs.append(doc)
            chunks_per_doc[doc] = count_result.count
            print(f"   ✓ {doc}: {count_result.count:,} chunks")
        else:
            print(f"   ✗ {doc}: 0 chunks (not found)")
    except Exception as e:
        print(f"   ✗ {doc}: Error - {e}")

# Test 3: Get unique document names from actual data (sample)
print("\n3. Sampling actual document_name values in database...")
try:
    sample_result = supabase.table("document_chunks")\
        .select("document_name")\
        .limit(100)\
        .execute()
    
    unique_names = set([d["document_name"] for d in sample_result.data if d.get("document_name")])
    print(f"   Found {len(unique_names)} unique names in sample:")
    for name in sorted(unique_names):
        print(f"   - '{name}'")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 4: Check for NULL document names
print("\n4. Checking for NULL or empty document_name values...")
try:
    null_result = supabase.table("document_chunks")\
        .select("id", count="exact")\
        .is_("document_name", "null")\
        .limit(1)\
        .execute()
    print(f"   NULL document_name: {null_result.count:,} chunks")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 5: Get distinct document names using RPC or direct query
print("\n5. Getting all distinct document names...")
try:
    # Try to get a larger sample to find all unique names
    all_docs_result = supabase.table("document_chunks")\
        .select("document_name")\
        .limit(10000)\
        .execute()
    
    all_unique_names = set([d["document_name"] for d in all_docs_result.data if d.get("document_name")])
    print(f"   Found {len(all_unique_names)} unique document names in 10K sample:")
    for name in sorted(all_unique_names):
        # Count this document
        count = supabase.table("document_chunks")\
            .select("id", count="exact")\
            .eq("document_name", name)\
            .limit(1)\
            .execute()
        print(f"   - '{name}': {count.count:,} chunks")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Final Summary
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"Documents found: {len(found_docs)}")
print(f"Expected: 9 documents")
print(f"Status: {'✓ PASS' if len(found_docs) == 9 else '✗ FAIL'}")
print("\nDocuments breakdown:")
for doc, count in sorted(chunks_per_doc.items()):
    print(f"  {doc}: {count:,} chunks")
print("=" * 70)
