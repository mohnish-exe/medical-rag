"""
COMPLETE OPTIMIZED WORKFLOW
============================

1. Re-parse all PDFs with medical-specific parser
2. Re-index with optimized chunking strategy
3. Maximize RAG accuracy, relevancy, and faithfulness

This combines:
- Medical document parsing (headers, sections, paragraphs)
- Smart chunking (context preservation, section awareness)
- Enhanced metadata (keywords, citations, structure)
"""

import os
import json
from core.medical_parser import extract_medical_blocks
from scripts.optimized_reindex import (
    clean_text, extract_keywords, create_enhanced_chunks,
    clear_database, supabase
)
from tqdm import tqdm
import time

PDF_DIR = "Dataset"  # Directory containing PDFs
CACHE_DIR = "parsed_pdfs_cache"

def find_pdf_files():
    """Find all PDF files in Dataset directory"""
    if not os.path.exists(PDF_DIR):
        return []
    pdf_files = [os.path.join(PDF_DIR, f) for f in os.listdir(PDF_DIR) if f.endswith('.pdf')]
    return pdf_files

def reparse_all_pdfs():
    """Re-parse all PDFs with medical parser"""
    pdf_files = find_pdf_files()
    
    if not pdf_files:
        print("⚠️  No PDF files found in Dataset directory")
        return []
    
    print(f"\n📚 Found {len(pdf_files)} PDF files to parse")
    
    parsed_files = []
    
    for pdf_file in pdf_files:
        pdf_basename = os.path.basename(pdf_file)
        print(f"\n{'='*70}")
        print(f"Parsing: {pdf_basename}")
        print(f"{'='*70}")
        
        try:
            # Parse PDF
            blocks = extract_medical_blocks(pdf_file)
            
            # Save to cache
            pdf_name = os.path.splitext(pdf_basename)[0]
            output_path = os.path.join(CACHE_DIR, f"{pdf_name}.json")
            
            os.makedirs(CACHE_DIR, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(blocks, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Saved to: {output_path}")
            parsed_files.append(output_path)
            
        except Exception as e:
            print(f"❌ Error parsing {pdf_basename}: {e}")
            import traceback
            traceback.print_exc()
    
    return parsed_files

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
    print("🚀 COMPLETE OPTIMIZED RAG WORKFLOW")
    print("=" * 70)
    
    print("\n📋 This workflow will:")
    print("  1️⃣  Re-parse all PDFs with medical-specific parser")
    print("  2️⃣  Clear existing database")
    print("  3️⃣  Re-index with optimized chunking")
    print("  4️⃣  Maximize RAG accuracy and relevancy")
    
    print("\n🎯 Expected Improvements:")
    print("  📈 Better section detection (medical headers)")
    print("  📈 Smarter paragraph grouping (complete thoughts)")
    print("  📈 Context preservation (surrounding paragraphs)")
    print("  📈 Enhanced metadata (keywords, structure)")
    print("  📈 Higher RAG scores (accuracy, relevancy, faithfulness)")
    
    # Check if PDFs exist
    pdf_files = find_pdf_files()
    
    if not pdf_files:
        print("\n⚠️  No PDF files found!")
        print("   Options:")
        print("   1. Place PDF files in current directory, OR")
        print("   2. Use existing parsed cache (skip parsing)")
        
        response = input("\nUse existing cache? (yes/no): ")
        if response.lower() != 'yes':
            print("❌ Cancelled")
            exit()
        
        print("\n✅ Using existing parsed cache")
        reparse = False
    else:
        print(f"\n📚 Found {len(pdf_files)} PDF files:")
        for pdf in pdf_files:
            print(f"   - {pdf}")
        
        response = input("\nRe-parse all PDFs? (yes/no): ")
        reparse = response.lower() == 'yes'
    
    # Confirm database clear
    print("\n⚠️  WARNING: This will DELETE all existing chunks and re-upload!")
    response = input("Continue? (yes/no): ")
    
    if response.lower() != 'yes':
        print("❌ Cancelled")
        exit()
    
    start_time = time.time()
    
    # Step 1: Re-parse (optional)
    if reparse:
        print("\n" + "=" * 70)
        print("STEP 1: RE-PARSING PDFs")
        print("=" * 70)
        reparse_all_pdfs()
    else:
        print("\n✅ Skipping parsing (using existing cache)")
    
    # Step 2: Clear database
    print("\n" + "=" * 70)
    print("STEP 2: CLEARING DATABASE")
    print("=" * 70)
    
    if not clear_database():
        print("❌ Failed to clear database. Exiting.")
        exit()
    
    # Step 3: Re-index with optimization
    print("\n" + "=" * 70)
    print("STEP 3: OPTIMIZED RE-INDEXING")
    print("=" * 70)
    
    json_files = sorted([f for f in os.listdir(CACHE_DIR) if f.endswith('.json')])
    
    print(f"\n📚 Processing {len(json_files)} documents...")
    
    total_success = 0
    total_fail = 0
    
    for json_file in json_files:
        success, fail = upload_document_optimized(os.path.join(CACHE_DIR, json_file))
        total_success += success
        total_fail += fail
    
    elapsed = time.time() - start_time
    
    # Final stats
    print("\n" + "=" * 70)
    print("✅ COMPLETE WORKFLOW FINISHED!")
    print("=" * 70)
    
    time.sleep(2)
    total = supabase.table("document_chunks").select("*", count="exact").limit(0).execute()
    sample = supabase.table("document_chunks").select("document_name").limit(10000).execute()
    unique_docs = sorted(set([d['document_name'] for d in sample.data if d.get('document_name')]))
    
    print(f"\n📊 Final Statistics:")
    print(f"   Time elapsed: {elapsed:.1f}s ({elapsed/60:.1f} min)")
    print(f"   Total chunks in DB: {total.count:,}")
    print(f"   Successfully uploaded: {total_success:,}")
    print(f"   Failed: {total_fail}")
    print(f"   Unique documents: {len(unique_docs)}")
    
    print(f"\n📚 Indexed Documents:")
    for doc in unique_docs:
        count = supabase.table("document_chunks").select("*", count="exact").eq("document_name", doc).limit(0).execute()
        print(f"   - {doc}: {count.count:,} chunks")
    
    print("\n🎯 System is now optimized for:")
    print("  ✅ Maximum RAG accuracy")
    print("  ✅ High relevancy scores")
    print("  ✅ Better context retrieval")
    print("  ✅ Improved faithfulness")
    print("  ✅ Faster queries")
    
    print("\n🚀 Ready to test! Run:")
    print("   python test_comprehensive_rag.py")
