"""
Clean database and re-index all 9 PDFs properly
"""
import json
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.supabase_client import supabase
from tqdm import tqdm
import time

CACHE_DIR = "parsed_pdfs_cache"

def clear_database():
    """Delete all chunks from database"""
    print("\n🗑️  Clearing database...")
    try:
        # Delete all records
        supabase.table("document_chunks").delete().neq("id", 0).execute()
        print("✅ Database cleared!")
        return True
    except Exception as e:
        print(f"❌ Error clearing database: {e}")
        return False

def upload_document(json_file):
    """Upload a parsed PDF"""
    doc_name = os.path.splitext(os.path.basename(json_file))[0]
    
    print(f"\n📤 Uploading {doc_name}...")
    
    # Load parsed JSON
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    chunks = []
    for page_num, page_data in data.items():
        for block_type, blocks in page_data.items():
            for block in blocks:
                chunk = {
                    "document_name": doc_name,
                    "page_number": int(page_num),
                    "block_type": block_type,
                    "text_content": block.get("text", ""),
                    "metadata": block
                }
                chunks.append(chunk)
    
    print(f"   Total chunks: {len(chunks):,}")
    
    # Upload in batches of 50 (smaller for stability)
    batch_size = 50
    success_count = 0
    fail_count = 0
    
    for i in tqdm(range(0, len(chunks), batch_size), desc=f"Uploading"):
        batch = chunks[i:i + batch_size]
        
        max_retries = 5
        for attempt in range(max_retries):
            try:
                supabase.table("document_chunks").insert(batch).execute()
                success_count += len(batch)
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(3)  # Wait before retry
                else:
                    fail_count += len(batch)
                    print(f"\n❌ Failed batch after {max_retries} attempts")
    
    print(f"✅ {doc_name}: {success_count:,} chunks uploaded, {fail_count} failed")
    return success_count, fail_count

if __name__ == "__main__":
    print("=" * 70)
    print("🔄 Clean Re-Index All PDFs")
    print("=" * 70)
    
    # Confirm action
    print("\n⚠️  WARNING: This will DELETE all existing chunks and re-upload!")
    response = input("Continue? (yes/no): ")
    
    if response.lower() != 'yes':
        print("❌ Cancelled")
        exit()
    
    # Clear database
    if not clear_database():
        print("❌ Failed to clear database. Exiting.")
        exit()
    
    # Get all JSON files
    json_files = sorted([f for f in os.listdir(CACHE_DIR) if f.endswith('.json')])
    
    print(f"\n📚 Found {len(json_files)} PDFs to upload")
    
    total_success = 0
    total_fail = 0
    
    for json_file in json_files:
        success, fail = upload_document(os.path.join(CACHE_DIR, json_file))
        total_success += success
        total_fail += fail
    
    print("\n" + "=" * 70)
    print("✅ Re-indexing Complete!")
    print("=" * 70)
    
    # Final stats
    time.sleep(2)  # Wait for database to update
    total = supabase.table("document_chunks").select("*", count="exact").limit(0).execute()
    sample = supabase.table("document_chunks").select("document_name").limit(10000).execute()
    unique_docs = sorted(set([d['document_name'] for d in sample.data if d.get('document_name')]))
    
    print(f"\n📊 Final Statistics:")
    print(f"   Total chunks in DB: {total.count:,}")
    print(f"   Successfully uploaded: {total_success:,}")
    print(f"   Failed: {total_fail}")
    print(f"   Unique documents: {len(unique_docs)}")
    
    print(f"\n📚 Documents:")
    for doc in unique_docs:
        count = supabase.table("document_chunks").select("*", count="exact").eq("document_name", doc).limit(0).execute()
        print(f"   - {doc}: {count.count:,} chunks")
