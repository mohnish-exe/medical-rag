"""
Test script to upload a sample file to Supabase storage
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.supabase_client import upload_to_supabase, get_public_url

def test_file_upload():
    """Test uploading a file to Supabase storage"""
    
    # Create a test file
    test_file_path = "test_upload.txt"
    with open(test_file_path, "w") as f:
        f.write("This is a test file for Supabase upload verification!")
    
    print("=" * 60)
    print("📤 Testing File Upload to Supabase")
    print("=" * 60)
    
    # Change this to match your bucket name
    bucket_name = "pdf-documents"  # 👈 CHANGE THIS to your bucket name
    file_name = "test_upload.txt"
    
    print(f"\n📦 Bucket: {bucket_name}")
    print(f"📄 File: {file_name}")
    
    try:
        print("\n⏳ Uploading file...")
        result = upload_to_supabase(bucket_name, test_file_path, file_name)
        print("✅ Upload successful!")
        print(f"   Response: {result}")
        
        # Get public URL
        public_url = get_public_url(bucket_name, file_name)
        print(f"\n🔗 Public URL: {public_url}")
        print("\n✅ You can access this file at the URL above!")
        
    except Exception as e:
        print(f"\n❌ Upload failed: {e}")
        print(f"\n💡 Make sure:")
        print(f"   1. You've created a bucket named '{bucket_name}' in Supabase")
        print(f"   2. The bucket is set to 'Public' if you want public URLs")
        print(f"   3. Your service role key has the correct permissions")
    
    finally:
        # Clean up test file
        if os.path.exists(test_file_path):
            os.remove(test_file_path)
            print(f"\n🗑️  Cleaned up local test file")
    
    print("=" * 60)

if __name__ == "__main__":
    test_file_upload()
