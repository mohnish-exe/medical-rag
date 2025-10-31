"""
Step 2A: Test indexing with one PDF
"""
from index_documents import index_pdf_from_url, show_indexed_documents

# Test with your medical report PDF
test_pdf_url = "https://drive.usercontent.google.com/download?id=12nq14ovXolaVKLppDNho_pPo01m3KEj5&export=download"
test_doc_name = "Patient_Medical_Report_Test"

print("🧪 Testing PDF indexing with one document...\n")

# Index the test PDF
success = index_pdf_from_url(test_pdf_url, test_doc_name)

if success:
    print("\n✅ Test successful! Now showing all indexed documents:")
    show_indexed_documents()
else:
    print("\n❌ Test failed. Please check the error above.")
