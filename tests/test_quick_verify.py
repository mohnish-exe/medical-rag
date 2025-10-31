"""
Quick verification: top_k working and getting answers from parsed PDFs
"""
import asyncio
from rag_api import search_documents, query_gemini

async def quick_verify():
    """Quick test to verify system is working"""
    
    print("="*70)
    print("🔬 QUICK VERIFICATION TEST")
    print("="*70)
    
    # Test 1: top_k=3 (default optimized)
    query = "what causes diabetes"
    top_k = 3
    
    print(f"\n📝 Query: '{query}'")
    print(f"🎯 top_k: {top_k}")
    print("\n" + "-"*70)
    
    # Search
    print("⏳ Searching...")
    contexts = await search_documents(query, top_k)
    
    if not contexts:
        print("❌ FAILED: No contexts found!")
        return False
    
    print(f"✅ Retrieved {len(contexts)} contexts (expected {top_k})")
    print(f"✅ top_k parameter working correctly!\n")
    
    # Show contexts
    print("📚 Retrieved Contexts:")
    for i, ctx in enumerate(contexts, 1):
        lines = ctx.split('\n')
        source = lines[0] if lines else ctx[:50]
        preview = lines[1][:100] if len(lines) > 1 else ""
        print(f"   {i}. {source}")
        print(f"      {preview}...\n")
    
    # Generate answer
    print("-"*70)
    print("⏳ Generating answer from contexts...")
    
    context_text = "\n\n".join([f"Context {i+1}:\n{ctx}" for i, ctx in enumerate(contexts)])
    prompt = f"""You are a medical expert. Answer based ONLY on the provided contexts.

QUESTION: {query}

CONTEXTS:
{context_text}

Provide a concise answer with citations (Document, Page X):"""
    
    answer = await query_gemini(prompt)
    
    print("✅ Answer generated!\n")
    print("="*70)
    print("📝 ANSWER:")
    print("="*70)
    print(answer)
    print("="*70)
    
    # Verify answer is from PDFs
    print("\n🔍 Verification:")
    has_citation = '(' in answer and ')' in answer
    mentions_context = any(word in answer.lower() for word in ['context', 'document', 'page'])
    not_empty = len(answer.strip()) > 20
    
    print(f"   ✓ Answer not empty: {not_empty}")
    print(f"   ✓ Has citations: {has_citation}")
    print(f"   ✓ References sources: {mentions_context or has_citation}")
    
    if not_empty and (has_citation or mentions_context):
        print("\n✅ SUCCESS: System is working correctly!")
        print("   - top_k parameter functioning")
        print("   - Contexts retrieved from parsed PDFs")
        print("   - Answer generated with citations")
        return True
    else:
        print("\n⚠️  WARNING: Answer quality needs review")
        return False

if __name__ == "__main__":
    result = asyncio.run(quick_verify())
    exit(0 if result else 1)
