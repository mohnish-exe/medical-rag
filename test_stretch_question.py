"""
Test the stretch MCQ question with hybrid RAG+Fallback
"""
import asyncio
import sys
sys.path.insert(0, '.')

from rag_api import search_documents, query_cohere

async def test_stretch():
    query = """What is the minimum time a stretch should be held for?

A. 0-10 seconds.
B. 10-30 seconds.
C. 30-50 seconds.
D. 60 seconds."""
    
    print("=" * 80)
    print("🎯 TESTING: Stretch Duration MCQ")
    print("=" * 80)
    print(f"\nQuestion: {query}\n")
    
    # Step 1: Try RAG search
    print("🔍 Searching RAG database...")
    contexts = await search_documents(query, top_k=5)
    
    if not contexts or len(contexts) == 0:
        print(f"\n⚠️  No relevant contexts found (score below threshold)")
        print(f"🤖 Using Cohere's pre-trained medical knowledge...\n")
        
        fallback_prompt = f"""You are a medical expert. Answer this medical question concisely using your medical knowledge.

Question: {query}

Provide a clear, accurate answer in 2-3 sentences. If it's a multiple choice question, explain the correct answer briefly."""
        
        try:
            answer = await query_cohere(fallback_prompt)
            print("=" * 80)
            print("✅ FALLBACK ANSWER (from Cohere's knowledge):")
            print("=" * 80)
            print(answer)
            print("=" * 80)
            print(f"\n📊 Mode: 🤖 FALLBACK (No RAG contexts used)")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print(f"\n✅ Found {len(contexts)} contexts in RAG database")
        print(f"📊 Mode: 📚 RAG (would use database contexts)")
        print(f"\nSample context:")
        print("-" * 80)
        print(contexts[0][:200] + "...")

if __name__ == "__main__":
    asyncio.run(test_stretch())
