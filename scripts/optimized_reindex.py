"""
OPTIMIZED RE-INDEXING STRATEGY
================================

Goal: Maximize RAG accuracy, relevancy, context quality, and faithfulness

Key Optimizations:
1. **Smart Chunking**: Combine related content (headers + paragraphs)
2. **Rich Metadata**: Store page numbers, section headers, document type
3. **Semantic Context**: Include surrounding context for better retrieval
4. **Clean Text**: Remove noise, normalize formatting
5. **Hierarchical Structure**: Maintain document structure (sections, subsections)
6. **Keyword Extraction**: Pre-compute keywords for faster search
7. **Citation-Ready**: Format for easy source attribution

Improvements over previous indexing:
- Better context boundaries (complete thoughts)
- Section headers included with content
- Reduced fragmentation
- Enhanced searchability
"""

import json
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.supabase_client import supabase
from tqdm import tqdm
import time
import re

CACHE_DIR = "parsed_pdfs_cache"

def clean_text(text):
    """Clean and normalize text"""
    if not text:
        return ""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters that don't add meaning
    text = re.sub(r'[^\w\s.,;:!?()\-\[\]{}]', '', text)
    return text.strip()

def extract_keywords(text):
    """Extract important keywords from text"""
    # Remove common medical stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been', 'being'}
    
    # Extract words
    words = re.findall(r'\b[a-z]{3,}\b', text.lower())
    
    # Filter and get unique keywords
    keywords = [w for w in words if w not in stop_words]
    return list(set(keywords))[:20]  # Top 20 unique keywords

def create_enhanced_chunks(data, doc_name):
    """
    Create optimized chunks with better context and metadata
    
    Strategy:
    1. Group headers with their content
    2. Keep paragraphs together (don't split mid-sentence)
    3. Add surrounding context
    4. Enrich with metadata
    """
    enhanced_chunks = []
    
    for page_num, page_data in data.items():
        page_num = int(page_num)
        
        # Extract all content from this page
        headers = page_data.get('headers', [])
        paragraphs = page_data.get('paragraphs', [])
        lists = page_data.get('lists', [])
        
        # Build section-aware chunks
        current_header = None
        
        # Process headers first
        for header in headers:
            header_text = header.get('text', '').strip()
            if len(header_text) > 5:  # Valid header
                current_header = header_text
                
                # Create header chunk with following content
                chunk_content = f"[HEADER] {header_text}"
                
                # Add immediate following paragraphs (up to 3)
                following_paras = []
                for para in paragraphs[:3]:
                    para_text = para.get('text', '').strip()
                    if len(para_text) > 20:
                        following_paras.append(para_text)
                
                if following_paras:
                    chunk_content += "\n\n" + " ".join(following_paras[:2])
                
                chunk = {
                    "document_name": doc_name,
                    "page_number": page_num,
                    "block_type": "header_with_content",
                    "section_header": current_header,
                    "text_content": clean_text(chunk_content),
                    "keywords": extract_keywords(chunk_content),
                    "metadata": {
                        "has_header": True,
                        "header": current_header,
                        "content_length": len(chunk_content)
                    }
                }
                enhanced_chunks.append(chunk)
        
        # Process paragraphs (group related ones)
        for i, para in enumerate(paragraphs):
            para_text = para.get('text', '').strip()
            
            # Skip very short paragraphs
            if len(para_text) < 30:
                continue
            
            # Create context-aware chunk
            # Include previous paragraph for context (if available)
            context_before = ""
            if i > 0:
                prev_para = paragraphs[i-1].get('text', '').strip()
                if len(prev_para) > 20:
                    context_before = prev_para[-100:]  # Last 100 chars of previous
            
            # Include next paragraph for context (if available)
            context_after = ""
            if i < len(paragraphs) - 1:
                next_para = paragraphs[i+1].get('text', '').strip()
                if len(next_para) > 20:
                    context_after = next_para[:100]  # First 100 chars of next
            
            # Build full chunk
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
                "block_type": "paragraph_with_context",
                "section_header": current_header,
                "text_content": clean_text(full_text),
                "keywords": extract_keywords(para_text),
                "metadata": {
                    "has_context": True,
                    "paragraph_index": i,
                    "content_length": len(para_text)
                }
            }
            enhanced_chunks.append(chunk)
        
        # Process lists (keep together)
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
                "block_type": "list_item",
                "section_header": current_header,
                "text_content": clean_text(full_text),
                "keywords": extract_keywords(list_text),
                "metadata": {
                    "is_list": True,
                    "content_length": len(list_text)
                }
            }
            enhanced_chunks.append(chunk)
    
    return enhanced_chunks

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

def upload_document_optimized(json_file):
    """Upload document with optimized chunking"""
    doc_name = os.path.splitext(os.path.basename(json_file))[0]
    
    print(f"\n📤 Processing {doc_name}...")
    
    # Load parsed JSON
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create enhanced chunks
    print(f"   Creating optimized chunks...")
    chunks = create_enhanced_chunks(data, doc_name)
    
    print(f"   Total optimized chunks: {len(chunks):,}")
    
    # Upload in batches
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
                    time.sleep(3)
                else:
                    fail_count += len(batch)
                    print(f"\n❌ Failed batch: {e}")
    
    print(f"✅ {doc_name}: {success_count:,} chunks uploaded")
    return success_count, fail_count

if __name__ == "__main__":
    print("=" * 70)
    print("🚀 OPTIMIZED RE-INDEXING FOR MAXIMUM RAG ACCURACY")
    print("=" * 70)
    
    print("\n📋 Optimization Features:")
    print("  ✅ Smart chunking (headers + content)")
    print("  ✅ Context preservation (surrounding paragraphs)")
    print("  ✅ Section awareness (maintain hierarchy)")
    print("  ✅ Keyword extraction (pre-computed)")
    print("  ✅ Clean text (normalized formatting)")
    print("  ✅ Rich metadata (enhanced searchability)")
    
    # Confirm
    print("\n⚠️  This will DELETE all existing chunks and re-upload with optimization!")
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
    
    print(f"\n📚 Processing {len(json_files)} PDFs with optimization...")
    
    total_success = 0
    total_fail = 0
    
    start_time = time.time()
    
    for json_file in json_files:
        success, fail = upload_document_optimized(os.path.join(CACHE_DIR, json_file))
        total_success += success
        total_fail += fail
    
    elapsed = time.time() - start_time
    
    print("\n" + "=" * 70)
    print("✅ OPTIMIZED RE-INDEXING COMPLETE!")
    print("=" * 70)
    
    # Final stats
    time.sleep(2)
    total = supabase.table("document_chunks").select("*", count="exact").limit(0).execute()
    sample = supabase.table("document_chunks").select("document_name").limit(10000).execute()
    unique_docs = sorted(set([d['document_name'] for d in sample.data if d.get('document_name')]))
    
    print(f"\n📊 Final Statistics:")
    print(f"   Total chunks in DB: {total.count:,}")
    print(f"   Successfully uploaded: {total_success:,}")
    print(f"   Failed: {total_fail}")
    print(f"   Unique documents: {len(unique_docs)}")
    print(f"   Time elapsed: {elapsed:.1f}s")
    
    print(f"\n📚 Documents:")
    for doc in unique_docs:
        count = supabase.table("document_chunks").select("*", count="exact").eq("document_name", doc).limit(0).execute()
        print(f"   - {doc}: {count.count:,} chunks")
    
    print("\n🎯 Expected Improvements:")
    print("  📈 Better context relevance (complete sections)")
    print("  📈 Higher answer accuracy (preserved structure)")
    print("  📈 Improved faithfulness (proper citations)")
    print("  📈 Faster search (pre-computed keywords)")
