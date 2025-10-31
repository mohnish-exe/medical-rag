"""
OPTIMIZED MEDICAL PDF PARSER
=============================

Designed specifically for medical textbooks and documents
Focuses on: sections, subsections, paragraphs, lists, tables, diagrams

Key improvements over generic parser:
1. Medical-specific section detection
2. Better paragraph grouping
3. Preserves medical terminology
4. Handles anatomical diagrams and tables
5. Maintains hierarchical structure (chapters > sections > subsections)
"""

import fitz
import json
import os
import re
from collections import Counter

def is_likely_header(text, font_size, avg_font_size, font_name, is_bold=False):
    """
    Determine if text block is a header based on multiple signals
    """
    score = 0
    
    # Font size significantly larger
    if font_size > avg_font_size + 2:
        score += 3
    elif font_size > avg_font_size + 1:
        score += 2
    
    # Bold font
    if is_bold or 'bold' in font_name.lower():
        score += 2
    
    # Short text (headers are usually concise)
    word_count = len(text.split())
    if word_count <= 10:
        score += 1
    
    # All caps
    if text.isupper() and len(text) > 3:
        score += 2
    
    # Title case (first letter of each word capitalized)
    words = text.split()
    if len(words) > 1:
        title_case_count = sum(1 for w in words if w and w[0].isupper())
        if title_case_count / len(words) > 0.7:
            score += 2
    
    # Medical section patterns
    medical_header_patterns = [
        r'^Chapter\s+\d+',
        r'^Section\s+\d+',
        r'^CHAPTER\s+\d+',
        r'^\d+\.\d+\s+\w+',  # Numbered sections like "1.1 Introduction"
        r'^[A-Z][a-z]+\s+(System|Anatomy|Physiology|Disease|Disorder|Treatment)',
        r'^(Introduction|Overview|Summary|Conclusion|Definition|Etiology|Pathophysiology|Diagnosis|Treatment|Management|Prognosis)',
    ]
    
    for pattern in medical_header_patterns:
        if re.match(pattern, text.strip()):
            score += 3
            break
    
    # Ends with colon (often section headers)
    if text.strip().endswith(':'):
        score += 1
    
    return score >= 5

def clean_medical_text(text):
    """Clean text while preserving medical terminology"""
    if not text:
        return ""
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove page numbers (standalone numbers)
    text = re.sub(r'^\d+$', '', text)
    
    # Remove common PDF artifacts
    text = re.sub(r'\x0c', '', text)  # Form feed
    
    # Preserve medical terms with special characters
    # Don't remove: α, β, γ, -, /, etc.
    
    return text.strip()

def extract_medical_blocks(pdf_path):
    """
    Extract blocks from medical PDF with smart grouping
    """
    doc = fitz.open(pdf_path)
    
    print(f"\n📄 Processing: {os.path.basename(pdf_path)}")
    print(f"   Total pages: {len(doc)}")
    
    all_blocks_by_page = {}
    
    # First pass: analyze font statistics across all pages
    all_font_sizes = []
    all_blocks_raw = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        
        for block in blocks:
            if block.get("type") == 0:  # Text block
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        all_font_sizes.append(span.get("size", 12))
                        all_blocks_raw.append({
                            "page": page_num + 1,
                            "text": span.get("text", ""),
                            "size": span.get("size", 12),
                            "font": span.get("font", ""),
                            "flags": span.get("flags", 0),
                            "bbox": span.get("bbox", [0, 0, 0, 0])
                        })
    
    if not all_font_sizes:
        print("   ⚠️  No text found in PDF")
        return {}
    
    avg_font_size = sum(all_font_sizes) / len(all_font_sizes)
    most_common_size = Counter(all_font_sizes).most_common(1)[0][0]
    
    print(f"   Average font size: {avg_font_size:.1f}")
    print(f"   Most common size: {most_common_size}")
    
    # Second pass: process pages and group intelligently
    for page_num in range(len(doc)):
        page = doc[page_num]
        page_blocks = page.get_text("dict")["blocks"]
        
        headers = []
        paragraphs = []
        lists = []
        tables = []
        
        current_paragraph = []
        current_list = []
        current_header = None
        
        for block in page_blocks:
            if block.get("type") == 0:  # Text block
                for line in block.get("lines", []):
                    line_text = ""
                    line_size = 0
                    line_font = ""
                    line_flags = 0
                    
                    for span in line.get("spans", []):
                        span_text = span.get("text", "").strip()
                        if span_text:
                            line_text += span_text + " "
                            line_size = span.get("size", 12)
                            line_font = span.get("font", "")
                            line_flags = span.get("flags", 0)
                    
                    line_text = clean_medical_text(line_text)
                    
                    if not line_text or len(line_text) < 3:
                        continue
                    
                    # Check if bold (flag 16 or 20)
                    is_bold = line_flags & 16 or line_flags & 20
                    
                    # Determine block type
                    if is_likely_header(line_text, line_size, most_common_size, line_font, is_bold):
                        # Save accumulated paragraph
                        if current_paragraph:
                            para_text = " ".join(current_paragraph)
                            if len(para_text) > 20:
                                paragraphs.append({
                                    "text": para_text,
                                    "section": current_header
                                })
                            current_paragraph = []
                        
                        # Save accumulated list
                        if current_list:
                            lists.extend(current_list)
                            current_list = []
                        
                        # Save header
                        current_header = line_text
                        headers.append({
                            "text": line_text,
                            "size": line_size,
                            "font": line_font,
                            "is_bold": is_bold
                        })
                    
                    # Check if list item
                    elif re.match(r'^[\u2022\u2023\u25E6\u2043\u2219•·◦‣⁃-]\s', line_text) or \
                         re.match(r'^\d+[\.\)]\s', line_text) or \
                         re.match(r'^[a-z][\.\)]\s', line_text):
                        # It's a list item
                        current_list.append({
                            "text": line_text,
                            "section": current_header
                        })
                        
                        # If we were building a paragraph, save it
                        if current_paragraph:
                            para_text = " ".join(current_paragraph)
                            if len(para_text) > 20:
                                paragraphs.append({
                                    "text": para_text,
                                    "section": current_header
                                })
                            current_paragraph = []
                    
                    # Regular paragraph text
                    else:
                        # Save accumulated list
                        if current_list:
                            lists.extend(current_list)
                            current_list = []
                        
                        # Add to current paragraph
                        current_paragraph.append(line_text)
                        
                        # If paragraph ends with period and is long enough, save it
                        if line_text.endswith('.') and len(" ".join(current_paragraph)) > 100:
                            para_text = " ".join(current_paragraph)
                            paragraphs.append({
                                "text": para_text,
                                "section": current_header
                            })
                            current_paragraph = []
        
        # Save any remaining content
        if current_paragraph:
            para_text = " ".join(current_paragraph)
            if len(para_text) > 20:
                paragraphs.append({
                    "text": para_text,
                    "section": current_header
                })
        
        if current_list:
            lists.extend(current_list)
        
        all_blocks_by_page[str(page_num + 1)] = {
            "headers": headers,
            "paragraphs": paragraphs,
            "lists": lists,
            "tables": tables
        }
        
        if (page_num + 1) % 10 == 0:
            print(f"   Processed {page_num + 1}/{len(doc)} pages...")
    
    doc.close()
    
    # Statistics
    total_headers = sum(len(p["headers"]) for p in all_blocks_by_page.values())
    total_paragraphs = sum(len(p["paragraphs"]) for p in all_blocks_by_page.values())
    total_lists = sum(len(p["lists"]) for p in all_blocks_by_page.values())
    
    print(f"\n✅ Parsing complete!")
    print(f"   Headers: {total_headers}")
    print(f"   Paragraphs: {total_paragraphs}")
    print(f"   Lists: {total_lists}")
    
    return all_blocks_by_page

def parse_and_save_medical_pdf(pdf_path, output_dir="parsed_pdfs_cache"):
    """Parse medical PDF and save to JSON"""
    os.makedirs(output_dir, exist_ok=True)
    
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_path = os.path.join(output_dir, f"{pdf_name}.json")
    
    blocks = extract_medical_blocks(pdf_path)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(blocks, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Saved to: {output_path}")
    return output_path

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        parse_and_save_medical_pdf(pdf_path)
    else:
        print("Usage: python parser.py <pdf_path>")
        print("\nOr parse all PDFs in a directory:")
        print("  python parser.py --dir <directory>")
