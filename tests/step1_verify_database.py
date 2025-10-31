"""
Step 1: Verify database table creation and check for missing document names
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.supabase_client import supabase

print("=" * 60)
print("📊 Step 1: Verifying Database Setup")
print("=" * 60)

try:
    # Test if table exists by trying to query it
    result = supabase.table("document_chunks").select("count", count="exact").execute()
    
    print("\n✅ Table 'document_chunks' exists!")
    print(f"   Current row count: {result.count if hasattr(result, 'count') else 0}")
    
    # Check for chunks with missing document names
    print("\n🔍 Checking for data quality issues...")
    
    # Get sample to check document names
    sample = supabase.table("document_chunks").select("document_name").limit(1000).execute()
    unique_docs = set([d.get("document_name") for d in sample.data if d.get("document_name")])
    null_docs = sum(1 for d in sample.data if not d.get("document_name"))
    
    print(f"\n📚 Unique documents in sample: {len(unique_docs)}")
    for doc in sorted(unique_docs):
        count = supabase.table("document_chunks").select("*", count="exact").eq("document_name", doc).limit(0).execute()
        print(f"   - {doc}: {count.count:,} chunks")
    
    if null_docs > 0:
        print(f"\n⚠️  Found {null_docs} chunks with NULL/missing document_name in sample!")
        # Get total NULL count
        null_total = supabase.table("document_chunks").select("*", count="exact").is_("document_name", "null").limit(0).execute()
        print(f"   Total NULL document_name chunks: {null_total.count:,}")
    
    print("\n" + "=" * 60)
    print("✅ Database verification complete!")
    print("=" * 60)
    
except Exception as e:
    print("\n❌ Error: Table 'document_chunks' does not exist!")
    print(f"   Details: {e}")
    print("\n📋 Please run the SQL script in Supabase SQL Editor:")
    print("   https://app.supabase.com/project/rejkqxpktiynlspoyppi/sql/new")
    print("\n" + "=" * 60)

