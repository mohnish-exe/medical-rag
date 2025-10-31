# Scripts Directory

Utility scripts for database management, indexing, and maintenance operations.

## 📤 Upload & Indexing

### `simple_upload.py`

Windows-compatible upload script with optimized chunking.

```bash
python scripts/simple_upload.py
```

- Creates enhanced chunks with context preservation
- Batch uploads with progress tracking
- Handles all 9 medical documents

### `optimized_reindex.py`

Enhanced chunking strategy for maximum RAG accuracy.

- Smart header detection
- Context preservation (±100 chars)
- Section awareness
- Keyword extraction (20 per chunk)

### `fast_batch_index.py`

Fast batch indexing for large document sets.

### `batch_index_pdfs.py`

Standard batch PDF indexing.

### `index_documents.py`

Single document indexing utility.

---

## 🧹 Maintenance

### `clean_reindex.py`

Complete database cleanup and re-indexing workflow.

```bash
python scripts/clean_reindex.py
```

### `clear_database_batches.py`

Batch deletion utility for clearing database in chunks.

- Prevents timeout on large tables
- Progress tracking

### `retry_upload.py`

Retry failed uploads with error recovery.

### `reupload_missing_pdfs.py`

Identify and re-upload missing documents.

```bash
python scripts/reupload_missing_pdfs.py
```

---

## ⚙️ Setup

### `setup_bucket.py`

Initialize Supabase storage bucket.

```bash
python scripts/setup_bucket.py
```

- Creates "pdf-documents" bucket
- Sets up CORS policies
- Configures permissions

---

## Usage Notes

- All scripts use modules from `core/` directory
- Requires `.env` file with Supabase credentials
- Uses `parsed_pdfs_cache/` for optimized re-indexing
- Check `tests/` directory for verification scripts

## Import Examples

```python
# From root directory
from core.supabase_client import supabase
from core.medical_parser import extract_medical_blocks

# Running scripts
python scripts/simple_upload.py
python scripts/clean_reindex.py
```
