"""
Test script to verify Supabase connection and configuration
"""
from supabase import create_client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

def test_supabase_connection():
    """Test Supabase connection and display basic info"""
    
    print("=" * 60)
    print("🔍 Testing Supabase Connection")
    print("=" * 60)
    
    # Check if credentials are loaded
    print("\n1️⃣ Checking Environment Variables...")
    if not SUPABASE_URL:
        print("❌ SUPABASE_URL is not set!")
        return False
    if not SUPABASE_KEY:
        print("❌ SUPABASE_SERVICE_ROLE_KEY is not set!")
        return False
    
    print(f"✅ SUPABASE_URL: {SUPABASE_URL}")
    print(f"✅ SUPABASE_KEY: {SUPABASE_KEY[:20]}...{SUPABASE_KEY[-10:]}")
    
    # Try to create client
    print("\n2️⃣ Creating Supabase Client...")
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Supabase client created successfully!")
    except Exception as e:
        print(f"❌ Failed to create Supabase client: {e}")
        return False
    
    # Test storage access
    print("\n3️⃣ Testing Storage Access...")
    try:
        # List all buckets
        buckets_response = supabase.storage.list_buckets()
        print(f"✅ Storage access successful!")
        print(f"📦 Available buckets: {len(buckets_response)}")
        
        if buckets_response:
            print("\n   Bucket Details:")
            for bucket in buckets_response:
                print(f"   - Name: {bucket.name}")
                print(f"     ID: {bucket.id}")
                print(f"     Public: {bucket.public}")
                print()
        else:
            print("   ℹ️  No buckets found. You may need to create one in Supabase dashboard.")
            
    except Exception as e:
        print(f"❌ Storage access failed: {e}")
        print(f"   Error details: {type(e).__name__}")
    
    # Test database access (optional)
    print("\n4️⃣ Testing Database Access...")
    try:
        # Try to get tables (this will work with service role key)
        # We'll try to query a common system table
        result = supabase.table('_prisma_migrations').select("*").limit(1).execute()
        print("✅ Database access successful!")
        print(f"   Can query database tables")
    except Exception as e:
        # It's okay if this specific table doesn't exist
        error_msg = str(e)
        if "relation" in error_msg.lower() and "does not exist" in error_msg.lower():
            print("✅ Database access successful! (test table not found, but connection works)")
        else:
            print(f"⚠️  Database query note: {e}")
            print("   (This might be normal if you haven't created any tables yet)")
    
    # Test REST API endpoint
    print("\n5️⃣ Testing REST API Endpoint...")
    try:
        import requests
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}"
        }
        response = requests.get(f"{SUPABASE_URL}/rest/v1/", headers=headers)
        
        if response.status_code == 200:
            print("✅ REST API is accessible!")
        else:
            print(f"⚠️  REST API responded with status: {response.status_code}")
            
    except Exception as e:
        print(f"⚠️  REST API test: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Supabase Connection Test Complete!")
    print("=" * 60)
    print("\n💡 Next Steps:")
    print("   - If you don't have storage buckets, create them in Supabase Dashboard")
    print("   - Go to: Storage → Create a new bucket")
    print("   - Make it public if you need public file access")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    test_supabase_connection()
