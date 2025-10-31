"""Verify all documents uploaded correctly"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.supabase_client import supabase

print("\n" + "="*70)
print("DATABASE VERIFICATION")
print("="*70)

# Get total count
total_result = supabase.table('document_chunks').select('id', count='exact').limit(1).execute()
total_chunks = total_result.count

print(f"\nTotal chunks in database: {total_chunks:,}")

# Get unique documents with counts
documents = {}
for doc_name in ['Anatomy&Physiology', 'Cardiology', 'Dentistry', 'EmergencyMedicine', 
                 'Gastrology', 'General', 'InfectiousDisease', 'InternalMedicine', 'Nephrology']:
    result = supabase.table('document_chunks')\
        .select('id', count='exact')\
        .eq('document_name', doc_name)\
        .limit(1)\
        .execute()
    if result.count > 0:
        documents[doc_name] = result.count

print(f"\nUnique documents found: {len(documents)}/9")
print("\nDocument breakdown:")
for doc, count in sorted(documents.items()):
    print(f"  - {doc}: {count:,} chunks")

print("\n" + "="*70)

# Check for missing documents
expected = {'Anatomy&Physiology', 'Cardiology', 'Dentistry', 'EmergencyMedicine', 
            'Gastrology', 'General', 'InfectiousDisease', 'InternalMedicine', 'Nephrology'}
found = set(documents.keys())
missing = expected - found

if missing:
    print(f"\nWARNING: Missing documents: {', '.join(missing)}")
else:
    print("\nSUCCESS: All 9 documents uploaded!")
    
print("="*70 + "\n")
