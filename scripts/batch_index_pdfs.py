"""
Batch index all PDFs from the HackACure dataset folder
"""
import asyncio
import os
from pathlib import Path
from index_documents import index_pdf_from_file, show_indexed_documents

async def batch_index_folder():
    """Index all PDFs from the dataset folder"""
    
    folder_path = r"D:\Documents\HackACure-Dataset\Dataset"
    
    print("=" * 60)
    print("📚 Batch Indexing PDFs from HackACure Dataset")
    print("=" * 60)
    print(f"\n📁 Folder: {folder_path}\n")
    
    # Check if folder exists
    if not os.path.exists(folder_path):
        print(f"❌ Folder not found: {folder_path}")
        return
    
    # Get all PDF files
    pdf_files = list(Path(folder_path).glob("*.pdf"))
    
    if not pdf_files:
        print(f"❌ No PDF files found in {folder_path}")
        return
    
    print(f"✅ Found {len(pdf_files)} PDF files\n")
    
    # Show all files first
    print("Files to be indexed:")
    for i, pdf_path in enumerate(pdf_files, 1):
        print(f"   {i}. {pdf_path.name}")
    print()
    
    # Index each PDF
    successful = 0
    failed = 0
    
    for i, pdf_path in enumerate(pdf_files, 1):
        print(f"\n{'=' * 60}")
        print(f"📄 [{i}/{len(pdf_files)}] Processing: {pdf_path.name}")
        print(f"{'=' * 60}")
        
        # Use filename without extension as document name
        doc_name = pdf_path.stem
        
        try:
            success = await index_pdf_from_file(str(pdf_path), doc_name)
            if success:
                successful += 1
                print(f"✅ Successfully indexed: {doc_name}")
            else:
                failed += 1
                print(f"❌ Failed to index: {doc_name}")
        except Exception as e:
            failed += 1
            print(f"❌ Error indexing {doc_name}: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 BATCH INDEXING SUMMARY")
    print("=" * 60)
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📁 Total: {len(pdf_files)}")
    print()
    
    # Show all indexed documents
    print("\n" + "=" * 60)
    print("📚 All Indexed Documents")
    print("=" * 60)
    await show_indexed_documents()

if __name__ == "__main__":
    asyncio.run(batch_index_folder())
