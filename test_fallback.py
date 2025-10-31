"""
Test the fallback feature - when RAG finds nothing, use Cohere's knowledge
"""
import asyncio
import sys
sys.path.insert(0, '.')

from rag_api import search_documents, query_cohere

async def test_fallback():
    print("=" * 80)
    print("🧪 TESTING FALLBACK FEATURE")
    print("=" * 80)
    
    # Test question that's NOT in the database
    test_query = "Creatine is synthesized from: A. amino acids in the muscles. B. amino acids in the liver. C. amino acids in the kidneys. D. creatinine in the kidneys."
    
    print(f"\n📝 Test Query:")
    print(f"   {test_query[:80]}...")
    
    # Step 1: Try RAG search
    print(f"\n🔍 Step 1: Searching RAG database...")
    contexts = await search_documents(test_query, top_k=3)
    
    if not contexts:
        print(f"   ⚠️ No relevant contexts found in RAG database")
        print(f"\n🤖 Step 2: Using Cohere's pre-trained knowledge as fallback...")
        
        # Step 2: Use Cohere's knowledge
        fallback_prompt = f"""You are a medical expert. Answer this medical question concisely using your medical knowledge.

Question: {test_query}

Provide a clear, accurate answer in 2-3 sentences. If it's a multiple choice question, explain the correct answer briefly."""
        
        try:
            answer = await query_cohere(fallback_prompt)
            
            print(f"\n✅ FALLBACK ANSWER:")
            print("-" * 80)
            print(answer)
            print("-" * 80)
            print(f"\n🎉 Fallback feature working! Cohere answered using its pre-trained knowledge.")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"   ✅ Found {len(contexts)} contexts in RAG database")
        print(f"   (This means the question IS in your database)")

if __name__ == "__main__":
    asyncio.run(test_fallback())
