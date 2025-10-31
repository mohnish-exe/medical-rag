"""
Setup script to create required Supabase bucket
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.supabase_client import supabase
from dotenv import load_dotenv

load_dotenv()

REQUIRED_BUCKET = "pdf-documents"

def setup_supabase_bucket():
    """Create the required Supabase storage bucket"""
    
    print("=" * 60)
    print("🔧 Supabase Storage Setup")
    print("=" * 60)
    
    print(f"\n📦 Required bucket: '{REQUIRED_BUCKET}'")
    
    # Check existing buckets
    print("\n1️⃣ Checking existing buckets...")
    try:
        buckets = supabase.storage.list_buckets()
        print(f"✅ Found {len(buckets)} bucket(s):")
        
        bucket_names = [b.name for b in buckets]
        for bucket in buckets:
            print(f"   - {bucket.name} (Public: {bucket.public})")
        
        if REQUIRED_BUCKET in bucket_names:
            print(f"\n✅ Bucket '{REQUIRED_BUCKET}' already exists!")
            return True
        
    except Exception as e:
        print(f"❌ Error listing buckets: {e}")
        return False
    
    # Try to create the bucket
    print(f"\n2️⃣ Creating bucket '{REQUIRED_BUCKET}'...")
    try:
        result = supabase.storage.create_bucket(
            REQUIRED_BUCKET,
            options={"public": True}
        )
        print(f"✅ Bucket '{REQUIRED_BUCKET}' created successfully!")
        print(f"   Result: {result}")
        return True
        
    except Exception as e:
        error_msg = str(e)
        if "already exists" in error_msg.lower():
            print(f"✅ Bucket '{REQUIRED_BUCKET}' already exists!")
            return True
        else:
            print(f"❌ Error creating bucket: {e}")
            print("\n📋 Manual Steps:")
            print("   1. Go to https://app.supabase.com/project/rejkqxpktiynlspoyppi/storage/buckets")
            print("   2. Click 'New bucket' or 'Create a new bucket'")
            print(f"   3. Name: {REQUIRED_BUCKET}")
            print("   4. Check 'Public bucket'")
            print("   5. Click 'Create bucket'")
            return False
    
    print("=" * 60)

if __name__ == "__main__":
    success = setup_supabase_bucket()
    if success:
        print("\n🎉 Setup complete! You can now use the API.")
    else:
        print("\n⚠️  Please create the bucket manually and try again.")
