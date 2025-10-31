"""
Check which buckets exist in Supabase
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.supabase_client import supabase

print("=" * 60)
print("🔍 Checking Supabase Buckets")
print("=" * 60)

try:
    buckets = supabase.storage.list_buckets()
    print(f"\n✅ Found {len(buckets)} bucket(s):\n")
    
    if buckets:
        for bucket in buckets:
            print(f"   📦 Name: {bucket.name}")
            print(f"      ID: {bucket.id}")
            print(f"      Public: {bucket.public}")
            print(f"      Created: {bucket.created_at}")
            print()
    else:
        print("   ⚠️  No buckets found!")
        print("\n   Create a bucket:")
        print("   1. Go to https://app.supabase.com/project/rejkqxpktiynlspoyppi/storage/buckets")
        print("   2. Click 'New bucket'")
        print("   3. Name: pdf-documents")
        print("   4. Make it Public")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("=" * 60)
