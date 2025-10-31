"""
Demo: Test fallback feature with questions NOT in database
"""
import asyncio
import sys
sys.path.insert(0, '.')

from rag_api import search_documents, query_cohere

async def test_fallback_demo():
    print("=" * 80)
    print("🎯 FALLBACK FEATURE DEMONSTRATION")
    print("=" * 80)
    
    test_questions = [
        "What is the minimum time a stretch should be held for?",
        "Walking down a street late at night, an adult male pedestrian notices a young female on the ground. According to the bystander effect, what changes behavior?",
        "Which planet is closest to the sun?"  # Definitely not medical!
    ]
    
    for i, query in enumerate(test_questions, 1):
        print(f"\n{'='*80}")
        print(f"TEST {i}: {query[:70]}...")
        print('='*80)
        
        # Try RAG search
        print(f"🔍 Searching RAG database...")
        contexts = await search_documents(query, top_k=3)
        
        if not contexts or len(contexts) == 0:
            print(f"⚠️  NO contexts found in database")
            print(f"\n🤖 Using Cohere's pre-trained knowledge...")
            
            fallback_prompt = f"""You are a helpful expert. Answer this question concisely.

Question: {query}

Provide a clear answer in 2-3 sentences."""
            
            try:
                answer = await query_cohere(fallback_prompt)
                print(f"\n✅ FALLBACK ANSWER:")
                print("-" * 80)
                print(answer)
                print("-" * 80)
            except Exception as e:
                print(f"❌ Error: {e}")
        else:
            print(f"✅ Found {len(contexts)} contexts (would use RAG)")
        
        print()

if __name__ == "__main__":
    asyncio.run(test_fallback_demo())
