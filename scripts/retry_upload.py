"""
Retry uploading the 3 failed PDFs from cache
"""
import asyncio
import json
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.supabase_client import supabase

CACHE_DIR = "parsed_pdfs_cache"

async def upload_from_cache(cache_file):
    """Upload cached parsed PDF to database"""
    try:
        with open(cache_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        document_name = data["document_name"]
        blocks = data["blocks"]
        
        print(f"\n📤 {document_name} ({len(blocks):,} chunks)")
        
        # Check if already uploaded
        result = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: supabase.table("document_chunks").select("id").eq("document_name", document_name).limit(1).execute()
        )
        
        if result.data:
            print(f"   ✅ Already complete")
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
            
            for attempt in range(5):
                try:
                    await asyncio.get_event_loop().run_in_executor(
                        None,
                        lambda b=batch: supabase.table("document_chunks").insert(b).execute()
                    )
                    uploaded += len(batch)
                    if uploaded % 1000 == 0 or uploaded == len(chunks_to_insert):
                        print(f"   📊 {uploaded:,}/{len(chunks_to_insert):,}")
                    break
                except Exception as e:
                    if attempt < 4:
                        await asyncio.sleep(5)  # Longer wait
                        continue
                    else:
                        print(f"   ❌ Failed at {uploaded:,}: {e}")
                        return {"status": "failed", "doc_name": document_name, "uploaded": uploaded}
        
        print(f"   ✅ Complete!")
        return {"status": "success", "doc_name": document_name, "chunks": uploaded}
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return {"status": "failed", "error": str(e)}

async def retry_failed():
    """Retry uploading the 3 failed PDFs"""
    
    failed_docs = ["InfectiousDisease", "InternalMedicine", "Nephrology"]
    
    print("=" * 70)
    print("🔄 RETRY UPLOADING FAILED PDFs")
    print("=" * 70)
    
    for doc_name in failed_docs:
        cache_file = os.path.join(CACHE_DIR, f"{doc_name}.json")
        if os.path.exists(cache_file):
            result = await upload_from_cache(cache_file)
            await asyncio.sleep(2)  # Pause between uploads
        else:
            print(f"\n❌ {doc_name} - cache file not found")
    
    print("\n" + "=" * 70)
    print("✅ DONE")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(retry_failed())
