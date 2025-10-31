"""
Ultra-fast batch PDF indexing with parallel processing
"""
import asyncio
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from core.parser import extract_formatted_blocks
from core.supabase_client import supabase

def parse_pdf_worker(pdf_path_str):
    """Worker function to parse PDF in separate process (CPU-bound)"""
    try:
        blocks = extract_formatted_blocks(pdf_path_str)
        return {"success": True, "blocks": blocks, "path": pdf_path_str}
    except Exception as e:
        return {"success": False, "error": str(e), "path": pdf_path_str}

async def insert_chunks_async(document_name, blocks):
    """Insert chunks into database asynchronously with retry logic"""
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
    
    # Insert in batches of 50 (smaller batches for reliability)
    batch_size = 50
    total_inserted = 0
    
    for i in range(0, len(chunks_to_insert), batch_size):
        batch = chunks_to_insert[i:i+batch_size]
        
        # Retry logic for each batch
        for attempt in range(3):
            try:
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(
                    None, 
                    lambda b=batch: supabase.table("document_chunks").insert(b).execute()
                )
                total_inserted += len(batch)
                break  # Success, exit retry loop
            except Exception as e:
                if attempt < 2:
                    await asyncio.sleep(2)  # Wait 2 seconds before retry
                    continue
                else:
                    print(f"      ❌ Error inserting batch after 3 attempts: {e}")
                    return False
    
    return True

async def check_document_exists(document_name):
    """Check if document already indexed with retry logic"""
    loop = asyncio.get_event_loop()
    
    for attempt in range(3):
        try:
            result = await loop.run_in_executor(
                None,
                lambda: supabase.table("document_chunks").select("id").eq("document_name", document_name).limit(1).execute()
            )
            return bool(result.data)
        except Exception as e:
            if attempt < 2:
                await asyncio.sleep(1)  # Wait 1 second before retry
                continue
            else:
                print(f"      ⚠️  Could not check if exists (will assume not indexed): {e}")
                return False  # Assume not indexed if check fails

async def process_single_pdf(pdf_path, executor):
    """Process a single PDF file"""
    doc_name = pdf_path.stem
    
    print(f"\n   📄 {doc_name}")
    
    # Check if already indexed
    exists = await check_document_exists(doc_name)
    if exists:
        print(f"      ⏭️  Already indexed, skipping...")
        return {"status": "skipped", "doc_name": doc_name}
    
    # Parse PDF in separate process (CPU-bound work)
    start_time = time.time()
    loop = asyncio.get_event_loop()
    
    try:
        result = await loop.run_in_executor(executor, parse_pdf_worker, str(pdf_path))
        
        if not result["success"]:
            print(f"      ❌ Parse error: {result['error']}")
            return {"status": "failed", "doc_name": doc_name, "error": result["error"]}
        
        blocks = result["blocks"]
        parse_time = time.time() - start_time
        print(f"      ✅ Parsed {len(blocks)} blocks ({parse_time:.1f}s)")
        
        # Insert into database
        insert_start = time.time()
        success = await insert_chunks_async(doc_name, blocks)
        insert_time = time.time() - insert_start
        
        if success:
            total_time = time.time() - start_time
            print(f"      ✅ Indexed {len(blocks)} chunks ({insert_time:.1f}s) - Total: {total_time:.1f}s")
            return {
                "status": "success", 
                "doc_name": doc_name, 
                "chunks": len(blocks),
                "time": total_time
            }
        else:
            return {"status": "failed", "doc_name": doc_name, "error": "Database insert failed"}
            
    except Exception as e:
        print(f"      ❌ Error: {e}")
        return {"status": "failed", "doc_name": doc_name, "error": str(e)}

async def batch_index_parallel():
    """Index all PDFs with parallel processing"""
    
    folder_path = r"D:\Documents\HackACure-Dataset\Dataset"
    
    print("=" * 70)
    print("🚀 FAST BATCH INDEXING - Parallel Processing")
    print("=" * 70)
    print(f"\n📁 Folder: {folder_path}\n")
    
    # Check folder exists
    if not os.path.exists(folder_path):
        print(f"❌ Folder not found: {folder_path}")
        return
    
    # Get all PDF files
    pdf_files = list(Path(folder_path).glob("*.pdf"))
    
    if not pdf_files:
        print(f"❌ No PDF files found in {folder_path}")
        return
    
    print(f"✅ Found {len(pdf_files)} PDF files\n")
    print("Files to process:")
    for i, pdf in enumerate(pdf_files, 1):
        print(f"   {i}. {pdf.name}")
    
    print(f"\n{'=' * 70}")
    print("⏳ Processing PDFs...")
    print(f"{'=' * 70}")
    
    start_time = time.time()
    
    # Create process pool for CPU-bound PDF parsing
    # Use max 4 workers to avoid overwhelming the system
    max_workers = min(4, os.cpu_count() or 2)
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Process PDFs with controlled concurrency
        results = []
        for pdf_path in pdf_files:
            result = await process_single_pdf(pdf_path, executor)
            results.append(result)
    
    # Summary
    total_time = time.time() - start_time
    successful = sum(1 for r in results if r["status"] == "success")
    failed = sum(1 for r in results if r["status"] == "failed")
    skipped = sum(1 for r in results if r["status"] == "skipped")
    total_chunks = sum(r.get("chunks", 0) for r in results)
    
    print(f"\n{'=' * 70}")
    print("📊 BATCH INDEXING COMPLETE")
    print(f"{'=' * 70}")
    print(f"✅ Successful: {successful}")
    print(f"⏭️  Skipped (already indexed): {skipped}")
    print(f"❌ Failed: {failed}")
    print(f"📄 Total PDFs: {len(pdf_files)}")
    print(f"📦 Total chunks indexed: {total_chunks}")
    print(f"⏱️  Total time: {total_time:.1f}s")
    
    if successful > 0:
        avg_time = sum(r.get("time", 0) for r in results if r["status"] == "success") / successful
        print(f"⚡ Average time per PDF: {avg_time:.1f}s")
    
    print(f"{'=' * 70}\n")
    
    # Show database stats
    print("📊 Database Statistics:")
    try:
        loop = asyncio.get_event_loop()
        stats = await loop.run_in_executor(
            None,
            lambda: supabase.table("document_chunks") \
                .select("document_name", count="exact") \
                .execute()
        )
        
        if stats.count:
            print(f"   Total chunks in database: {stats.count}")
            
            # Count unique documents
            docs = await loop.run_in_executor(
                None,
                lambda: supabase.rpc("count_distinct_documents").execute()
            )
            
    except Exception as e:
        print(f"   Could not fetch stats: {e}")

if __name__ == "__main__":
    asyncio.run(batch_index_parallel())
