"""
Smart indexing: Parse PDFs locally, then upload when connection stable
"""
import asyncio
import os
import json
import time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
from .parser import extract_formatted_blocks
from .supabase_client import supabase

CACHE_DIR = "parsed_pdfs_cache"

def parse_and_cache_pdf(pdf_path_str):
    """Parse PDF and save to cache file"""
    try:
        blocks = extract_formatted_blocks(pdf_path_str)
        
        # Save to cache
        os.makedirs(CACHE_DIR, exist_ok=True)
        doc_name = Path(pdf_path_str).stem
        cache_file = os.path.join(CACHE_DIR, f"{doc_name}.json")
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump({"document_name": doc_name, "blocks": blocks}, f)
        
        return {"success": True, "blocks": len(blocks), "doc_name": doc_name, "cache_file": cache_file}
    except Exception as e:
        return {"success": False, "error": str(e), "path": pdf_path_str}

async def upload_from_cache(cache_file):
    """Upload cached parsed PDF to database"""
    try:
        with open(cache_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        document_name = data["document_name"]
        blocks = data["blocks"]
        
        print(f"\n   📤 Uploading: {document_name} ({len(blocks)} chunks)")
        
        # Check if already uploaded
        result = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: supabase.table("document_chunks").select("id").eq("document_name", document_name).limit(1).execute()
        )
        
        if result.data:
            print(f"      ⏭️  Already in database, skipping...")
            return {"status": "skipped", "doc_name": document_name}
        
        # Prepare chunks
        chunks_to_insert = []
        for idx, block in enumerate(blocks):
            chunk_data = {
                "document_name": document_name,
                "page_number": block.get("page", 0),
                "chunk_index": idx,
                "text_content": block.get("text", ""),
                "header": block.get("header", ""),
                "coverage_flags": block.get("coverage_flags", []),
                "metadata": {
                    "font_size": block.get("font_size"),
                    "color": block.get("color"),
                    "flagged": block.get("flagged", False)
                }
            }
            chunks_to_insert.append(chunk_data)
        
        # Upload in small batches with retry
        batch_size = 50
        uploaded = 0
        
        for i in range(0, len(chunks_to_insert), batch_size):
            batch = chunks_to_insert[i:i+batch_size]
            
            for attempt in range(5):  # More retries
                try:
                    await asyncio.get_event_loop().run_in_executor(
                        None,
                        lambda b=batch: supabase.table("document_chunks").insert(b).execute()
                    )
                    uploaded += len(batch)
                    if uploaded % 500 == 0 or uploaded == len(chunks_to_insert):
                        print(f"      📊 {uploaded}/{len(chunks_to_insert)} chunks uploaded...")
                    break
                except Exception as e:
                    if attempt < 4:
                        await asyncio.sleep(3)  # Wait longer between retries
                        continue
                    else:
                        print(f"      ❌ Failed after 5 attempts: {e}")
                        return {"status": "failed", "doc_name": document_name, "error": str(e)}
        
        print(f"      ✅ Successfully uploaded {uploaded} chunks!")
        return {"status": "success", "doc_name": document_name, "chunks": uploaded}
        
    except Exception as e:
        print(f"      ❌ Error: {e}")
        return {"status": "failed", "error": str(e)}

async def smart_batch_index():
    """Two-phase indexing: Parse first, upload later"""
    
    folder_path = r"D:\Documents\HackACure-Dataset\Dataset"
    
    print("=" * 70)
    print("🧠 SMART BATCH INDEXING - Parse + Upload Separately")
    print("=" * 70)
    print(f"\n📁 Folder: {folder_path}\n")
    
    if not os.path.exists(folder_path):
        print(f"❌ Folder not found: {folder_path}")
        return
    
    pdf_files = list(Path(folder_path).glob("*.pdf"))
    
    if not pdf_files:
        print(f"❌ No PDF files found")
        return
    
    print(f"✅ Found {len(pdf_files)} PDF files\n")
    
    # PHASE 1: Parse and cache all PDFs
    print("=" * 70)
    print("📖 PHASE 1: Parsing PDFs (local, fast)")
    print("=" * 70)
    
    cache_files = []
    os.makedirs(CACHE_DIR, exist_ok=True)
    
    # Check which are already parsed
    for pdf_path in pdf_files:
        doc_name = pdf_path.stem
        cache_file = os.path.join(CACHE_DIR, f"{doc_name}.json")
        
        if os.path.exists(cache_file):
            print(f"   ✅ {doc_name} - already parsed (cached)")
            cache_files.append(cache_file)
        else:
            print(f"   ⏳ {doc_name} - parsing...")
            start = time.time()
            
            # Parse in current process (simpler, more reliable)
            result = parse_and_cache_pdf(str(pdf_path))
            
            if result["success"]:
                elapsed = time.time() - start
                print(f"      ✅ Parsed {result['blocks']} blocks ({elapsed:.1f}s)")
                cache_files.append(result["cache_file"])
            else:
                print(f"      ❌ Error: {result['error']}")
    
    print(f"\n✅ All PDFs parsed! {len(cache_files)} files ready to upload.\n")
    
    # PHASE 2: Upload to database
    print("=" * 70)
    print("☁️  PHASE 2: Uploading to Database")
    print("=" * 70)
    
    results = []
    for cache_file in cache_files:
        result = await upload_from_cache(cache_file)
        results.append(result)
    
    # Summary
    successful = sum(1 for r in results if r.get("status") == "success")
    skipped = sum(1 for r in results if r.get("status") == "skipped")
    failed = sum(1 for r in results if r.get("status") == "failed")
    total_chunks = sum(r.get("chunks", 0) for r in results)
    
    print(f"\n{'=' * 70}")
    print("📊 INDEXING COMPLETE")
    print("=" * 70)
    print(f"✅ Successfully uploaded: {successful}")
    print(f"⏭️  Skipped (already in DB): {skipped}")
    print(f"❌ Failed: {failed}")
    print(f"📦 Total chunks uploaded: {total_chunks}")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(smart_batch_index())
