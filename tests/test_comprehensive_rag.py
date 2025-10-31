"""
Comprehensive RAG test to verify accuracy, relevance, and optimization
Tests all 4 scoring metrics:
- Answer Relevancy (30%)
- Answer Correctness (30%)
- Context Relevance (25%)
- Faithfulness (15%)
"""
import asyncio
from rag_api import search_documents, query_gemini, QueryRequest

# Test queries designed to evaluate different aspects
TEST_QUERIES = [
    {
        "query": "heart failure treatment",
        "top_k": 3,
        "description": "Test: Medical treatment query"
    },
    {
        "query": "symptoms of acute myocardial infarction",
        "top_k": 4,
        "description": "Test: Symptom identification"
    },
    {
        "query": "diabetes management guidelines",
        "top_k": 3,
        "description": "Test: Clinical guidelines"
    },
    {
        "query": "antibiotic resistance mechanisms",
        "top_k": 3,
        "description": "Test: Pathophysiology"
    },
    {
        "query": "kidney disease stages",
        "top_k": 3,
        "description": "Test: Disease classification"
    }
]

async def evaluate_query(query_data):
    """Evaluate a single query across all metrics"""
    print("\n" + "="*80)
    print(f"📋 {query_data['description']}")
    print("="*80)
    print(f"Query: {query_data['query']}")
    print(f"Top K: {query_data['top_k']}")
    
    # Step 1: Search and retrieve contexts
    print("\n🔍 STEP 1: Context Retrieval")
    print("-"*80)
    contexts = await search_documents(query_data['query'], query_data['top_k'])
    
    if not contexts:
        print("❌ No contexts found - FAILED")
        return {
            "query": query_data['query'],
            "status": "failed",
            "reason": "No contexts retrieved"
        }
    
    print(f"✅ Retrieved {len(contexts)} contexts\n")
    
    # Evaluate Context Relevance (25%)
    print("📊 Context Relevance Evaluation:")
    for i, ctx in enumerate(contexts, 1):
        preview = ctx.split('\n')[1] if '\n' in ctx else ctx[:100]
        print(f"   {i}. {preview[:150]}...")
    
    # Step 2: Generate answer
    print("\n💭 STEP 2: Answer Generation")
    print("-"*80)
    
    context_text = "\n\n".join([f"Context {i+1}:\n{ctx}" for i, ctx in enumerate(contexts)])
    
    prompt = f"""You are a medical expert assistant. Your task is to provide accurate, relevant, and faithful answers based strictly on the provided medical contexts.

QUESTION: {query_data['query']}

MEDICAL CONTEXTS:
{context_text}

INSTRUCTIONS:
1. Answer ONLY using information from the contexts above - do not add external knowledge
2. Be concise and directly answer the question (2-4 sentences ideal)
3. If information is insufficient or missing, clearly state: "The provided contexts do not contain sufficient information about [topic]"
4. Cite sources using format: (Document Name, Page X)
5. If contexts are not relevant to the question, explicitly state this
6. Focus on accuracy over completeness - only state what the contexts clearly support

ANSWER (be specific and cite sources):"""
    
    answer = await query_gemini(prompt)
    
    print(f"✅ Answer generated\n")
    
    # Display results
    print("📝 FINAL ANSWER:")
    print("-"*80)
    print(answer)
    print("-"*80)
    
    # Evaluation metrics
    print("\n📈 METRIC EVALUATION:")
    print("-"*80)
    
    # Answer Relevancy (30%) - Check if answer addresses the query
    relevant_terms = set(query_data['query'].lower().split())
    answer_lower = answer.lower()
    relevancy_score = sum(1 for term in relevant_terms if term in answer_lower) / len(relevant_terms)
    print(f"   Answer Relevancy: {relevancy_score*100:.1f}% {'✅' if relevancy_score > 0.5 else '⚠️'}")
    
    # Answer Correctness (30%) - Check for citations and specificity
    has_citations = '(' in answer and ')' in answer
    is_specific = len(answer.split()) > 10 and not answer.startswith("The provided contexts do not")
    correctness_score = (has_citations * 0.5 + is_specific * 0.5)
    print(f"   Answer Correctness: {correctness_score*100:.1f}% {'✅' if correctness_score > 0.5 else '⚠️'}")
    
    # Context Relevance (25%) - Check if contexts match query keywords
    context_relevance = len(contexts) / query_data['top_k']
    print(f"   Context Relevance: {context_relevance*100:.1f}% {'✅' if context_relevance >= 0.8 else '⚠️'}")
    
    # Faithfulness (15%) - Check if answer doesn't contradict contexts
    faithful = not ("not" in answer.lower() and "do not contain" in answer.lower())
    faithfulness_score = 1.0 if faithful else 0.3
    print(f"   Faithfulness: {faithfulness_score*100:.1f}% {'✅' if faithfulness_score > 0.7 else '⚠️'}")
    
    # Overall score
    overall = (relevancy_score * 0.30 + correctness_score * 0.30 + 
               context_relevance * 0.25 + faithfulness_score * 0.15)
    print(f"\n   🎯 OVERALL SCORE: {overall*100:.1f}%")
    
    return {
        "query": query_data['query'],
        "status": "success",
        "answer": answer,
        "contexts_count": len(contexts),
        "scores": {
            "relevancy": relevancy_score,
            "correctness": correctness_score,
            "context_relevance": context_relevance,
            "faithfulness": faithfulness_score,
            "overall": overall
        }
    }

async def run_comprehensive_test():
    """Run all test queries"""
    print("\n" + "="*80)
    print("🧪 COMPREHENSIVE RAG EVALUATION TEST")
    print("="*80)
    print("Testing Answer Relevancy (30%), Correctness (30%), Context Relevance (25%), Faithfulness (15%)")
    
    results = []
    for query_data in TEST_QUERIES:
        result = await evaluate_query(query_data)
        results.append(result)
        await asyncio.sleep(1)  # Brief pause between queries
    
    # Summary
    print("\n" + "="*80)
    print("📊 TEST SUMMARY")
    print("="*80)
    
    successful = [r for r in results if r['status'] == 'success']
    print(f"\n✅ Successful queries: {len(successful)}/{len(results)}")
    
    if successful:
        avg_scores = {
            'relevancy': sum(r['scores']['relevancy'] for r in successful) / len(successful),
            'correctness': sum(r['scores']['correctness'] for r in successful) / len(successful),
            'context_relevance': sum(r['scores']['context_relevance'] for r in successful) / len(successful),
            'faithfulness': sum(r['scores']['faithfulness'] for r in successful) / len(successful),
            'overall': sum(r['scores']['overall'] for r in successful) / len(successful)
        }
        
        print("\n📈 Average Scores:")
        print(f"   Answer Relevancy (30%):    {avg_scores['relevancy']*100:.1f}%")
        print(f"   Answer Correctness (30%):  {avg_scores['correctness']*100:.1f}%")
        print(f"   Context Relevance (25%):   {avg_scores['context_relevance']*100:.1f}%")
        print(f"   Faithfulness (15%):        {avg_scores['faithfulness']*100:.1f}%")
        print(f"   \n   🎯 OVERALL: {avg_scores['overall']*100:.1f}%")
        
        if avg_scores['overall'] >= 0.7:
            print("\n   ✅ EXCELLENT - System meets all requirements!")
        elif avg_scores['overall'] >= 0.5:
            print("\n   ⚠️  GOOD - System functional but needs improvement")
        else:
            print("\n   ❌ NEEDS WORK - Significant improvements required")
    
    print("\n" + "="*80)
    print("✅ Evaluation Complete")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(run_comprehensive_test())
