"""
Clear database in batches to avoid timeout
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.supabase_client import supabase
import time

print("🗑️  Clearing database in batches...")

batch_size = 10000
deleted_total = 0

while True:
    try:
        # Get IDs of next batch
        result = supabase.table("document_chunks").select("id").limit(batch_size).execute()
        
        if not result.data or len(result.data) == 0:
            print("✅ Database cleared!")
            break
        
        ids = [row["id"] for row in result.data]
        
        # Delete this batch
        for id in ids:
            supabase.table("document_chunks").delete().eq("id", id).execute()
        
        deleted_total += len(ids)
        print(f"   Deleted {deleted_total:,} chunks...")
        
        time.sleep(1)  # Small delay between batches
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"Deleted {deleted_total:,} chunks so far")
        break

print(f"\n✅ Total deleted: {deleted_total:,}")

# Verify
result = supabase.table("document_chunks").select("*", count="exact").limit(0).execute()
print(f"Remaining chunks: {result.count:,}")
