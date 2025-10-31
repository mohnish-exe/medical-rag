"""Quick check of database contents"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.supabase_client import supabase

# Get total
total = supabase.table("document_chunks").select("*", count="exact").limit(0).execute()
print(f"Total chunks: {total.count:,}")

# Check first 100 for document names
sample = supabase.table("document_chunks").select("document_name, page_number").limit(100).execute()
docs_in_sample = {}
for chunk in sample.data:
    doc = chunk.get('document_name', 'NULL')
    docs_in_sample[doc] = docs_in_sample.get(doc, 0) + 1

print(f"\nDocument names in first 100 chunks:")
for doc, count in sorted(docs_in_sample.items()):
    print(f"  {doc}: {count}")

# Get full count for Anatomy&Physiology
anatomy_count = supabase.table("document_chunks").select("*", count="exact").eq("document_name", "Anatomy&Physiology").limit(0).execute()
print(f"\nAnatomy&Physiology total: {anatomy_count.count:,}")

# Check if there are chunks with no document_name at all
print(f"\nChecking for NULL document names...")
try:
    null_count = supabase.table("document_chunks").select("*", count="exact").is_("document_name", "null").limit(0).execute()
    print(f"NULL document_name chunks: {null_count.count:,}")
except Exception as e:
    print(f"Error checking NULL: {e}")
    
# Try getting a chunk with high ID to see if it's a different document
high_id_sample = supabase.table("document_chunks").select("document_name, page_number, text_content").range(100000, 100010).execute()
print(f"\nSample from chunk IDs 100,000-100,010:")
for chunk in high_id_sample.data:
    print(f"  Doc: {chunk.get('document_name', 'NULL')}, Page: {chunk.get('page_number')}, Text: {chunk.get('text_content', '')[:50]}...")
