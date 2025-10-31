# Project Structure

## 📁 Root Directory

Contains main application files and configuration:

### Main Applications

- `rag_api.py` - Main RAG API server (FastAPI) ⭐
- `api_server.py` - Alternative API server
- `complete_optimization.py` - Full workflow orchestrator: parse + index

### Configuration

- `requirements.txt` - Python dependencies
- `.env` - Environment variables (not tracked)
- `.gitignore` - Git ignore rules
- `PROJECT_STRUCTURE.md` - This file

---

## 🧠 core/

Core library modules (reusable components):

### Database

- `supabase_client.py` - Supabase connection and client

### Parsers

- `medical_parser.py` - Medical-specific PDF parser with smart header detection
- `parser.py` - Generic PDF parser

### Processing

- `semantic_matcher.py` - Semantic search functionality
- `keyword_extractor.py` - Keyword extraction utility
- `smart_indexer.py` - Optimized indexing with context preservation

### Usage

```python
from core.medical_parser import extract_medical_blocks
from core.supabase_client import supabase
from core.smart_indexer import create_optimized_chunks
```

---

## 🔧 scripts/

Utility scripts for maintenance and batch operations:

### Indexing Scripts

- `simple_upload.py` - Windows-compatible upload script
- `optimized_reindex.py` - Enhanced chunking strategy
- `fast_batch_index.py` - Fast batch indexing
- `batch_index_pdfs.py` - Batch PDF indexing
- `index_documents.py` - Document indexing

### Maintenance Scripts

- `clean_reindex.py` - Clean and re-index database
- `clear_database_batches.py` - Batch deletion utility
- `retry_upload.py` - Retry failed uploads
- `reupload_missing_pdfs.py` - Re-upload missing documents
- `setup_bucket.py` - Initialize Supabase storage

### Usage

```bash
# Upload optimized chunks
python scripts/simple_upload.py

# Clean and re-index
python scripts/clean_reindex.py
```

---

## 📂 tests/

Contains all test and verification scripts:

### API Tests

- `test_api_format.py` - API format compliance testing
- `test_api_request.py` - API request testing
- `test_gemini.py` - Gemini API testing

### RAG Tests

- `test_comprehensive_rag.py` - Comprehensive RAG evaluation
- `test_rag_direct.py` - Direct RAG testing
- `test_rag_query.py` - RAG query testing
- `test_cardiology_query.py` - Cardiology-specific query test

### Database Tests

- `test_supabase.py` - Supabase connection testing
- `test_upload.py` - Upload functionality testing
- `test_indexing.py` - Indexing tests
- `test_indexing_2.py` - Additional indexing tests

### Verification Scripts

- `check_buckets.py` - Verify Supabase buckets
- `check_documents.py` - Check database documents
- `quick_db_check.py` - Quick database verification
- `verify_format.py` - Format verification
- `verify_upload.py` - Verify upload success
- `step1_verify_database.py` - Database verification step

### Testing Quick Reference

```bash
# Run comprehensive RAG evaluation
python tests/test_comprehensive_rag.py

# Verify database state
python tests/verify_upload.py

# Test API format
python tests/test_api_format.py
```

---

## 📚 docs/

Contains all project documentation:

### Documentation Files

- `README.md` - Main project README
- `README_RAG.md` - RAG system documentation
- `API_FORMAT_COMPLIANCE.md` - API format specifications
- `FORMAT_VERIFICATION.md` - Format verification report
- `OPTIMIZATION_REPORT.md` - Optimization results and metrics
- `FINAL_SUMMARY.md` - Project summary and outcomes

---

## 📊 Dataset/

Contains source PDF files:

- 9 medical PDFs (Anatomy, Cardiology, Dentistry, etc.)

## 💾 parsed_pdfs_cache/

Contains parsed JSON files:

- Optimized parsed data from medical PDFs
- Used for fast re-indexing without re-parsing

---

## Quick Start

### 1. Start RAG API Server

```bash
python rag_api.py
```

Server runs on `http://localhost:8000`

- Root: `GET /` - API info
- Stats: `GET /stats` - Database statistics
- Query: `POST /query` - RAG queries

### 2. Run Optimization Workflow

```bash
python complete_optimization.py
```

Full workflow: Parse all PDFs → Create optimized chunks → Upload to database

### 3. Upload Optimized Chunks

```bash
python scripts/simple_upload.py
```

Batch upload with progress tracking

### 4. Verify Upload

```bash
python tests/verify_upload.py
```

Check all 9 documents are properly indexed

### 5. Test RAG System

```bash
python tests/test_comprehensive_rag.py
```

Evaluate accuracy, faithfulness, and relevancy

---

## Architecture Overview

```
┌──────────────────────┐
│    PDF Files         │
│    (Dataset/)        │
│  9 Medical Textbooks │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Medical Parser      │
│  (core/medical_      │
│   parser.py)         │
│  • Font analysis     │
│  • Header detection  │
│  • List extraction   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Smart Indexer       │
│  (core/smart_        │
│   indexer.py)        │
│  • Context preserve  │
│  • Section awareness │
│  • Keywords (20/doc) │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Supabase Database   │
│  (document_chunks)   │
│  431,726 chunks      │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  RAG API Server      │
│  (rag_api.py)        │
│  • FastAPI           │
│  • Gemini 2.5 Flash  │
│  • Vector search     │
└──────────────────────┘
```

---

## Project Statistics

**Current State (October 28, 2025):**

- ✅ Total Chunks: 431,726
- ✅ Documents: 9 medical textbooks
- ✅ Optimization: Complete
- ✅ Database: Fully indexed
- ✅ Organization: Professional structure

**Medical Documents:**

1. Anatomy&Physiology (20,679 chunks)
2. Cardiology (52,195 chunks)
3. Dentistry (15,128 chunks)
4. EmergencyMedicine (45,023 chunks)
5. Gastrology (81,183 chunks)
6. General (27,267 chunks)
7. InfectiousDisease (3,252 chunks)
8. InternalMedicine (94,251 chunks)
9. Nephrology (92,748 chunks)

**Optimization Features:**

- Medical-specific parsing
- Smart header detection
- Context preservation (±100 chars)
- Section awareness
- Keyword extraction (20 per chunk)
- Coverage flags
- Enhanced metadata

---

**Last Updated:** October 28, 2025
