"""
Direct test of RAG functions (no server needed)
"""
import asyncio
from rag_api import search_documents, query_gemini, QueryRequest

async def test_rag():
    print("=" * 70)
    print("🧪 Testing RAG System Directly")
    print("=" * 70)
    
    # Test query
    query = "What are the symptoms of heart disease?"
    top_k = 3
    
    print(f"\nQuery: {query}")
    print(f"Top K: {top_k}\n")
    
    # Step 1: Search
    print("Step 1: Searching documents...")
    contexts = await search_documents(query, top_k)
    
    print(f"\n✅ Found {len(contexts)} contexts:\n")
    for i, ctx in enumerate(contexts, 1):
        print(f"{i}. {ctx[:150]}...\n")
    
    # Step 2: Generate answer
    if contexts:
        print("\nStep 2: Generating answer with Gemini...")
        
        context_text = "\n\n".join([f"Context {i+1}:\n{ctx}" for i, ctx in enumerate(contexts)])
        
        prompt = f"""You are a medical assistant. Answer the following question based ONLY on the provided medical document contexts.

Question: {query}

Medical Document Contexts:
{context_text}

Instructions:
- Provide a clear, accurate answer based on the contexts above
- If the contexts don't contain enough information, say so
- Cite specific documents/pages when relevant
- Keep the answer concise but comprehensive

Answer:"""
        
        answer = await query_gemini(prompt)
        
        print("\n" + "=" * 70)
        print("📝 FINAL ANSWER")
        print("=" * 70)
        print(answer)
        print("\n" + "=" * 70)
        print("✅ RAG Test Complete!")
        print("=" * 70)
    else:
        print("\n❌ No contexts found")

if __name__ == "__main__":
    asyncio.run(test_rag())
