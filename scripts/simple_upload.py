# -*- coding: utf-8 -*-
"""
Simple upload script - no emojis for Windows compatibility
Upload optimized chunks from parsed cache to database
"""
import json
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.supabase_client import supabase
import time
import re

CACHE_DIR = "parsed_pdfs_cache"

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s.,;:!?()\-\[\]{}]', '', text)
    return text.strip()

def extract_keywords(text):
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been', 'being'}
    words = re.findall(r'\b[a-z]{3,}\b', text.lower())
    keywords = [w for w in words if w not in stop_words]
    return list(set(keywords))[:20]

def create_enhanced_chunks(data, doc_name):
    enhanced_chunks = []
    
    for page_num, page_data in data.items():
        page_num = int(page_num)
        headers = page_data.get('headers', [])
        paragraphs = page_data.get('paragraphs', [])
        lists = page_data.get('lists', [])
        current_header = None
        
        # Headers
        for header in headers:
            header_text = header.get('text', '').strip()
            if len(header_text) > 5:
                current_header = header_text
                following_paras = []
                for para in paragraphs[:3]:
                    para_text = para.get('text', '').strip()
                    if len(para_text) > 20:
                        following_paras.append(para_text)
                
                chunk_content = f"[HEADER] {header_text}"
                if following_paras:
                    chunk_content += "\n\n" + " ".join(following_paras[:2])
                
                chunk = {
                    "document_name": doc_name,
                    "page_number": page_num,
                    "chunk_index": len(enhanced_chunks),
                    "text_content": clean_text(chunk_content),
                    "header": current_header,
                    "coverage_flags": [],
                    "metadata": {
                        "block_type": "header_with_content",
                        "section_header": current_header,
                        "keywords": extract_keywords(chunk_content),
                        "has_header": True
                    }
                }
                enhanced_chunks.append(chunk)
        
        # Paragraphs
        for i, para in enumerate(paragraphs):
            para_text = para.get('text', '').strip()
            if len(para_text) < 30:
                continue
            
            context_before = ""
            if i > 0:
                prev_para = paragraphs[i-1].get('text', '').strip()
                if len(prev_para) > 20:
                    context_before = prev_para[-100:]
            
            context_after = ""
            if i < len(paragraphs) - 1:
                next_para = paragraphs[i+1].get('text', '').strip()
                if len(next_para) > 20:
                    context_after = next_para[:100]
            
            full_text = ""
            if current_header:
                full_text += f"[Section: {current_header}] "
            if context_before:
                full_text += f"...{context_before} "
            full_text += para_text
            if context_after:
                full_text += f" {context_after}..."
            
            chunk = {
                "document_name": doc_name,
                "page_number": page_num,
                "chunk_index": len(enhanced_chunks),
                "text_content": clean_text(full_text),
                "header": current_header if current_header else "",
                "coverage_flags": [],
                "metadata": {
                    "block_type": "paragraph_with_context",
                    "section_header": current_header,
                    "keywords": extract_keywords(para_text),
                    "has_context": True,
                    "paragraph_index": i
                }
            }
            enhanced_chunks.append(chunk)
        
        # Lists
        for list_item in lists:
            list_text = list_item.get('text', '').strip()
            if len(list_text) < 20:
                continue
            
            full_text = ""
            if current_header:
                full_text += f"[Section: {current_header}] "
            full_text += f"[LIST ITEM] {list_text}"
            
            chunk = {
                "document_name": doc_name,
                "page_number": page_num,
                "chunk_index": len(enhanced_chunks),
                "text_content": clean_text(full_text),
                "header": current_header if current_header else "",
                "coverage_flags": [],
                "metadata": {
                    "block_type": "list_item",
                    "section_header": current_header,
                    "keywords": extract_keywords(list_text),
                    "is_list": True
                }
            }
            enhanced_chunks.append(chunk)
    
    return enhanced_chunks

def upload_document(json_file):
    doc_name = os.path.splitext(os.path.basename(json_file))[0]
    
    print(f"\n>>> Processing {doc_name}...")
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"    Creating optimized chunks...")
    chunks = create_enhanced_chunks(data, doc_name)
    
    print(f"    Total chunks: {len(chunks):,}")
    
    batch_size = 100
    success_count = 0
    fail_count = 0
    
    total_batches = (len(chunks) + batch_size - 1) // batch_size
    
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        batch_num = i // batch_size + 1
        
        max_retries = 5
        for attempt in range(max_retries):
            try:
                supabase.table("document_chunks").insert(batch).execute()
                success_count += len(batch)
                if batch_num % 10 == 0:
                    print(f"    Batch {batch_num}/{total_batches} uploaded...")
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2)
                else:
                    fail_count += len(batch)
                    print(f"    FAILED batch {batch_num}: {e}")
    
    print(f"    SUCCESS: {doc_name} - {success_count:,} chunks uploaded, {fail_count} failed")
    return success_count, fail_count

if __name__ == "__main__":
    print("=" * 70)
    print("OPTIMIZED RE-INDEXING FOR MAXIMUM RAG ACCURACY")
    print("=" * 70)
    
    print("\nOptimization Features:")
    print("  - Smart chunking (headers + content)")
    print("  - Context preservation (surrounding paragraphs)")
    print("  - Section awareness (maintain hierarchy)")
    print("  - Keyword extraction (pre-computed)")
    print("  - Clean text (normalized formatting)")
    print("  - Rich metadata (enhanced searchability)")
    
    print("\nWARNING: This will upload to the database!")
    response = input("Continue? (yes/no): ")
    
    if response.lower() != 'yes':
        print("Cancelled")
        exit()
    
    json_files = sorted([f for f in os.listdir(CACHE_DIR) if f.endswith('.json')])
    
    print(f"\nProcessing {len(json_files)} documents...")
    
    total_success = 0
    total_fail = 0
    start_time = time.time()
    
    for json_file in json_files:
        success, fail = upload_document(os.path.join(CACHE_DIR, json_file))
        total_success += success
        total_fail += fail
    
    elapsed = time.time() - start_time
    
    print("\n" + "=" * 70)
    print("RE-INDEXING COMPLETE!")
    print("=" * 70)
    
    time.sleep(2)
    total = supabase.table("document_chunks").select("*", count="exact").limit(0).execute()
    sample = supabase.table("document_chunks").select("document_name").limit(10000).execute()
    unique_docs = sorted(set([d['document_name'] for d in sample.data if d.get('document_name')]))
    
    print(f"\nFinal Statistics:")
    print(f"   Time elapsed: {elapsed:.1f}s ({elapsed/60:.1f} min)")
    print(f"   Total chunks in DB: {total.count:,}")
    print(f"   Successfully uploaded: {total_success:,}")
    print(f"   Failed: {total_fail}")
    print(f"   Unique documents: {len(unique_docs)}")
    
    print(f"\nDocuments:")
    for doc in unique_docs:
        count = supabase.table("document_chunks").select("*", count="exact").eq("document_name", doc).limit(0).execute()
        print(f"   - {doc}: {count.count:,} chunks")
    
    print("\nExpected Improvements:")
    print("  + Better context relevance")
    print("  + Higher answer accuracy")
    print("  + Improved faithfulness")
    print("  + Faster search with keywords")
