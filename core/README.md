# Core Library Modules

Reusable components for the RAG system.

## 📦 Modules

### Database

**`supabase_client.py`**

- Supabase connection and client instance
- Environment variable management

```python
from core.supabase_client import supabase
```

---

### Parsers

**`medical_parser.py`** ⭐
Medical-specific PDF parser with smart header detection.

Features:

- Font analysis for header detection
- Bold text identification
- Medical terminology patterns
- Paragraph grouping
- List extraction
- Clean text output

```python
from core.medical_parser import extract_medical_blocks

blocks = extract_medical_blocks("path/to/medical.pdf")
# Returns: {"headers": [...], "paragraphs": [...], "lists": [...]}
```

**`parser.py`**
Generic PDF parser for standard documents.

```python
from core.parser import extract_text_blocks
```

---

### Processing

**`smart_indexer.py`** 🎯
Optimized indexing with context preservation.

Features:

- Smart chunking (headers + content)
- Context preservation (±100 chars)
- Section awareness
- Keyword extraction
- Coverage flags

```python
from core.smart_indexer import create_optimized_chunks

chunks = create_optimized_chunks(parsed_data, doc_name)
# Returns: List of enhanced chunks ready for upload
```

**`keyword_extractor.py`**
Extract relevant keywords from text.

```python
from core.keyword_extractor import extract_keywords

keywords = extract_keywords(text, max_keywords=20)
```

**`semantic_matcher.py`**
Semantic search functionality.

```python
from core.semantic_matcher import semantic_search

results = semantic_search(query, documents, top_k=5)
```

---

## 🏗️ Architecture

```
core/
├── __init__.py          # Package initialization
├── supabase_client.py   # Database connection
├── medical_parser.py    # Medical PDF parsing
├── parser.py            # Generic PDF parsing
├── smart_indexer.py     # Optimized chunking
├── keyword_extractor.py # Keyword extraction
└── semantic_matcher.py  # Semantic search
```

---

## Usage Examples

### Import from main application

```python
# In rag_api.py or complete_optimization.py
from core.supabase_client import supabase
from core.medical_parser import extract_medical_blocks
from core.smart_indexer import create_optimized_chunks

# Use the modules
blocks = extract_medical_blocks("document.pdf")
chunks = create_optimized_chunks(blocks, "DocumentName")
```

### Import in scripts

```python
# In scripts/simple_upload.py
from core.medical_parser import extract_medical_blocks
from core.supabase_client import supabase
```

---

## Module Dependencies

- `supabase-py` - Database operations
- `PyPDF2` / `pdfplumber` - PDF parsing
- `spacy` - Keyword extraction
- Standard library modules

---

## Development

When adding new core modules:

1. Add to `core/` directory
2. Update `core/__init__.py`
3. Document in this README
4. Add usage examples

## Testing

Test core modules using scripts in `tests/` directory:

```bash
python tests/test_comprehensive_rag.py
```
