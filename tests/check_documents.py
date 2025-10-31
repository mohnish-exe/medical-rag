"""Check what documents are in the database"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.supabase_client import supabase

# Get all unique document names
result = supabase.table('document_chunks').select('document_name').execute()

if result.data:
    docs = set([d['document_name'] for d in result.data])
    print(f"\n📊 Total chunks: {len(result.data)}")
    print(f"📚 Unique documents: {len(docs)}")
    print("\n📄 Document list:")
    for doc in sorted(docs):
        # Count chunks per document
        count = sum(1 for d in result.data if d['document_name'] == doc)
        print(f"  - {doc}: {count:,} chunks")
else:
    print("No data found")
