"""
Step 2: Index PDFs into the database
This script processes PDF files and stores all text chunks in Supabase
Run this ONCE to index all your medical PDFs
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import requests
from core.parser import extract_formatted_blocks
from core.supabase_client import supabase
from datetime import datetime
import tempfile

def index_pdf_from_url(pdf_url: str, document_name: str = None):
    """
    Download and index a PDF from URL
    
    Args:
        pdf_url: URL to the PDF file
        document_name: Name to identify this document (optional, will use URL if not provided)
    """
    if not document_name:
        document_name = pdf_url.split('/')[-1] or "unnamed_document"
    
    print(f"\n{'='*60}")
    print(f"📄 Processing: {document_name}")
    print(f"{'='*60}")
    
    # Step 1: Download PDF
    print("⏳ Downloading PDF...")
    try:
        response = requests.get(pdf_url, timeout=60)
        if response.status_code != 200:
            print(f"❌ Failed to download PDF: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Download error: {e}")
        return False
    
    # Step 2: Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
        tmp_pdf.write(response.content)
        tmp_pdf.flush()
        pdf_path = tmp_pdf.name
    
    print(f"✅ Downloaded ({len(response.content) / 1024:.1f} KB)")
    
    # Step 3: Extract text blocks
    print("⏳ Parsing PDF and extracting text blocks...")
    try:
        blocks = extract_formatted_blocks(pdf_path)
        print(f"✅ Extracted {len(blocks)} text blocks")
    except Exception as e:
        print(f"❌ Parsing error: {e}")
        os.unlink(pdf_path)
        return False
    
    # Step 4: Check if document already exists
    print("⏳ Checking if document already indexed...")
    existing = supabase.table("document_chunks").select("id").eq("document_name", document_name).limit(1).execute()
    
    if existing.data:
        print(f"⚠️  Document '{document_name}' already exists in database!")
        print(f"   Do you want to re-index? This will DELETE old data and add new.")
        choice = input("   Type 'yes' to re-index, or anything else to skip: ")
        
        if choice.lower() == 'yes':
            print("🗑️  Deleting old chunks...")
            supabase.table("document_chunks").delete().eq("document_name", document_name).execute()
            print("✅ Old chunks deleted")
        else:
            print("⏭️  Skipping this document")
            os.unlink(pdf_path)
            return False
    
    # Step 5: Insert chunks into database
    print("⏳ Inserting chunks into database...")
    
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
    
    # Insert in batches of 100 to avoid timeouts
    batch_size = 100
    total_inserted = 0
    
    for i in range(0, len(chunks_to_insert), batch_size):
        batch = chunks_to_insert[i:i+batch_size]
        try:
            supabase.table("document_chunks").insert(batch).execute()
            total_inserted += len(batch)
            print(f"   Inserted {total_inserted}/{len(chunks_to_insert)} chunks...")
        except Exception as e:
            print(f"❌ Error inserting batch: {e}")
            os.unlink(pdf_path)
            return False
    
    print(f"✅ Successfully indexed {total_inserted} chunks")
    
    # Clean up temp file
    os.unlink(pdf_path)
    
    print(f"{'='*60}")
    print(f"✅ Document '{document_name}' indexed successfully!")
    print(f"{'='*60}\n")
    
    return True


def index_pdf_from_file(pdf_path: str, document_name: str = None):
    """
    Index a PDF from local file path
    
    Args:
        pdf_path: Path to local PDF file
        document_name: Name to identify this document (optional, will use filename)
    """
    if not document_name:
        document_name = os.path.basename(pdf_path)
    
    if not os.path.exists(pdf_path):
        print(f"❌ File not found: {pdf_path}")
        return False
    
    print(f"\n{'='*60}")
    print(f"📄 Processing: {document_name}")
    print(f"{'='*60}")
    
    # Step 1: Extract text blocks
    print("⏳ Parsing PDF and extracting text blocks...")
    try:
        blocks = extract_formatted_blocks(pdf_path)
        print(f"✅ Extracted {len(blocks)} text blocks")
    except Exception as e:
        print(f"❌ Parsing error: {e}")
        return False
    
    # Step 2: Check if document already exists
    print("⏳ Checking if document already indexed...")
    existing = supabase.table("document_chunks").select("id").eq("document_name", document_name).limit(1).execute()
    
    if existing.data:
        print(f"⚠️  Document '{document_name}' already exists in database!")
        print(f"   Do you want to re-index? This will DELETE old data and add new.")
        choice = input("   Type 'yes' to re-index, or anything else to skip: ")
        
        if choice.lower() == 'yes':
            print("🗑️  Deleting old chunks...")
            supabase.table("document_chunks").delete().eq("document_name", document_name).execute()
            print("✅ Old chunks deleted")
        else:
            print("⏭️  Skipping this document")
            return False
    
    # Step 3: Insert chunks into database
    print("⏳ Inserting chunks into database...")
    
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
    
    # Insert in batches of 100
    batch_size = 100
    total_inserted = 0
    
    for i in range(0, len(chunks_to_insert), batch_size):
        batch = chunks_to_insert[i:i+batch_size]
        try:
            supabase.table("document_chunks").insert(batch).execute()
            total_inserted += len(batch)
            print(f"   Inserted {total_inserted}/{len(chunks_to_insert)} chunks...")
        except Exception as e:
            print(f"❌ Error inserting batch: {e}")
            return False
    
    print(f"✅ Successfully indexed {total_inserted} chunks")
    print(f"{'='*60}")
    print(f"✅ Document '{document_name}' indexed successfully!")
    print(f"{'='*60}\n")
    
    return True


def show_indexed_documents():
    """Show all currently indexed documents"""
    print("\n" + "="*60)
    print("📊 Currently Indexed Documents")
    print("="*60)
    
    try:
        stats = supabase.table("document_stats").select("*").execute()
        
        if not stats.data:
            print("   (No documents indexed yet)")
        else:
            total_chunks = 0
            for doc in stats.data:
                print(f"\n📄 {doc['document_name']}")
                print(f"   Chunks: {doc['chunk_count']}")
                print(f"   Pages: {doc['first_page']} - {doc['last_page']}")
                print(f"   Indexed: {doc['indexed_at']}")
                total_chunks += doc['chunk_count']
            
            print(f"\n{'='*60}")
            print(f"Total: {len(stats.data)} documents, {total_chunks} chunks")
            print(f"{'='*60}\n")
    
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("📚 PDF Indexing Tool")
    print("="*60)
    print("\nThis tool indexes PDFs into your database for RAG search.")
    print("\nOptions:")
    print("  1. Index from URL")
    print("  2. Index from local file")
    print("  3. Batch index from folder")
    print("  4. Show indexed documents")
    print("  5. Exit")
    
    while True:
        print("\n" + "-"*60)
        choice = input("Select option (1-5): ").strip()
        
        if choice == "1":
            url = input("Enter PDF URL: ").strip()
            name = input("Enter document name (or press Enter to use URL): ").strip()
            index_pdf_from_url(url, name if name else None)
        
        elif choice == "2":
            path = input("Enter PDF file path: ").strip()
            name = input("Enter document name (or press Enter to use filename): ").strip()
            index_pdf_from_file(path, name if name else None)
        
        elif choice == "3":
            folder = input("Enter folder path containing PDFs: ").strip()
            if os.path.exists(folder):
                pdf_files = [f for f in os.listdir(folder) if f.lower().endswith('.pdf')]
                print(f"\nFound {len(pdf_files)} PDF files")
                confirm = input(f"Index all {len(pdf_files)} files? (yes/no): ").strip()
                
                if confirm.lower() == 'yes':
                    success_count = 0
                    for pdf_file in pdf_files:
                        pdf_path = os.path.join(folder, pdf_file)
                        if index_pdf_from_file(pdf_path):
                            success_count += 1
                    
                    print(f"\n{'='*60}")
                    print(f"✅ Indexed {success_count}/{len(pdf_files)} documents")
                    print(f"{'='*60}")
            else:
                print("❌ Folder not found!")
        
        elif choice == "4":
            show_indexed_documents()
        
        elif choice == "5":
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid option!")
