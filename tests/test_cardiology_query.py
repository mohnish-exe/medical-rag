"""
Test RAG with a better query about cardiology
"""
import asyncio
from rag_api import search_documents, query_gemini

async def test_cardiology():
    print("=" * 70)
    print("🧪 Testing RAG with Cardiology Query")
    print("=" * 70)
    
    query = "heart failure treatment"
    top_k = 5
    
    print(f"\nQuery: {query}")
    print(f"Top K: {top_k}\n")
    
    print("Searching documents...")
    contexts = await search_documents(query, top_k)
    
    print(f"\n✅ Found {len(contexts)} contexts:\n")
    for i, ctx in enumerate(contexts, 1):
        print(f"{i}. {ctx[:200]}...\n")
    
    if contexts:
        print("Generating answer...")
        
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
        print("📝 ANSWER")
        print("=" * 70)
        print(answer)
        print("\n" + "=" * 70)

if __name__ == "__main__":
    asyncio.run(test_cardiology())
