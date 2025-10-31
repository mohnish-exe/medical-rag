"""
Re-upload the 8 missing PDFs from parsed cache
Only uploads documents that aren't already in the database
"""
import json
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.supabase_client import supabase
from tqdm import tqdm

CACHE_DIR = "parsed_pdfs_cache"

def check_document_exists(doc_name):
    """Check if document already has chunks in database"""
    result = supabase.table("document_chunks").select("*", count="exact").eq("document_name", doc_name).limit(0).execute()
    return result.count > 0

def upload_document(json_file):
    """Upload a parsed PDF from cache"""
    doc_name = os.path.splitext(os.path.basename(json_file))[0]
    
    # Check if already uploaded
    if check_document_exists(doc_name):
        print(f"✅ {doc_name} already in database - skipping")
        return
    
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
    
    # Upload in batches of 100
    batch_size = 100
    failed_batches = []
    
    for i in tqdm(range(0, len(chunks), batch_size), desc=f"Uploading {doc_name}"):
        batch = chunks[i:i + batch_size]
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                supabase.table("document_chunks").insert(batch).execute()
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"\n⚠️  Retry {attempt + 1}/{max_retries} for batch {i//batch_size + 1}")
                    import time
                    time.sleep(2)
                else:
                    print(f"\n❌ Failed batch {i//batch_size + 1}: {e}")
                    failed_batches.append(i//batch_size + 1)
    
    if failed_batches:
        print(f"\n⚠️  {len(failed_batches)} batches failed for {doc_name}")
    else:
        print(f"✅ {doc_name} uploaded successfully!")

if __name__ == "__main__":
    print("=" * 70)
    print("📚 Re-uploading Missing PDFs from Cache")
    print("=" * 70)
    
    # List all JSON files in cache
    json_files = [f for f in os.listdir(CACHE_DIR) if f.endswith('.json')]
    
    print(f"\nFound {len(json_files)} parsed PDFs in cache:")
    for f in sorted(json_files):
        doc_name = os.path.splitext(f)[0]
        exists = check_document_exists(doc_name)
        status = "✅ In DB" if exists else "❌ Missing"
        print(f"  {status} - {doc_name}")
    
    # Upload missing documents
    missing = [f for f in json_files if not check_document_exists(os.path.splitext(f)[0])]
    
    if not missing:
        print("\n✅ All documents already in database!")
    else:
        print(f"\n📤 Uploading {len(missing)} missing documents...")
        for json_file in missing:
            upload_document(os.path.join(CACHE_DIR, json_file))
    
    print("\n" + "=" * 70)
    print("✅ Upload complete!")
    print("=" * 70)
    
    # Final stats
    total = supabase.table("document_chunks").select("*", count="exact").limit(0).execute()
    sample = supabase.table("document_chunks").select("document_name").limit(10000).execute()
    unique_docs = set([d['document_name'] for d in sample.data if d.get('document_name')])
    
    print(f"\n📊 Final Statistics:")
    print(f"   Total chunks: {total.count:,}")
    print(f"   Unique documents: {len(unique_docs)}")
    for doc in sorted(unique_docs):
        count = supabase.table("document_chunks").select("*", count="exact").eq("document_name", doc).limit(0).execute()
        print(f"   - {doc}: {count.count:,} chunks")
