"""
Test indexing a second PDF document
"""
import asyncio
from index_documents import index_pdf_from_url, show_indexed_documents

async def test_second_pdf():
    """Test with a different medical PDF"""
    
    print("🧪 Testing PDF indexing with a second document...\n")
    
    # Test with another medical report PDF
    test_url = "https://www.africau.edu/images/default/sample.pdf"
    document_name = "Sample_Medical_Document_2"
    
    # Index the PDF
    success = await index_pdf_from_url(test_url, document_name)
    
    if success:
        print("\n✅ Test successful! Now showing all indexed documents:\n")
        await show_indexed_documents()
    else:
        print("\n❌ Test failed!")
        
if __name__ == "__main__":
    asyncio.run(test_second_pdf())
