"""
Test with actual exam questions from query_logs_rows.csv
"""
import asyncio
import sys
sys.path.insert(0, '.')

from rag_api import search_documents, query_cohere

async def test_exam_questions():
    print("=" * 80)
    print("🎓 TESTING EXAM QUESTIONS WITH FALLBACK")
    print("=" * 80)
    
    exam_questions = [
        "Creatine is synthesized from: A. amino acids in the muscles. B. amino acids in the liver. C. amino acids in the kidneys. D. creatinine in the kidneys.",
        "What is the minimum time a stretch should be held for? A. 0-10 seconds. B. 10-30 seconds. C. 30-50 seconds. D. 60 seconds.",
        "A healthy 23-year-old male is undergoing an exercise stress test. If blood were sampled at different locations before and after the test, which area would contain the lowest oxygen content at both time points? A. Inferior vena cava B. Coronary sinus C. Pulmonary artery D. Pulmonary vein.",
    ]
    
    for i, query in enumerate(exam_questions, 1):
        print(f"\n{'='*80}")
        print(f"QUESTION {i}:")
        print(query[:100] + "...")
        print('='*80)
        
        # Try RAG search
        contexts = await search_documents(query, top_k=3)
        
        if not contexts:
            print(f"\n🤖 No relevant RAG contexts - Using Cohere's knowledge...")
            
            fallback_prompt = f"""You are a medical expert. Answer this medical question concisely using your medical knowledge.

Question: {query}

Provide a clear, accurate answer in 2-3 sentences. If it's a multiple choice question, explain the correct answer briefly."""
            
            answer = await query_cohere(fallback_prompt)
            print(f"\n✅ ANSWER (from Cohere's pre-trained knowledge):")
            print("-" * 80)
            print(answer)
            print("-" * 80)
        else:
            print(f"\n✅ Found {len(contexts)} contexts in RAG database")
            print("(Would use RAG answer)")

if __name__ == "__main__":
    asyncio.run(test_exam_questions())
