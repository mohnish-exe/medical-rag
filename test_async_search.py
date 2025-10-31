from core.supabase_client import supabase
import asyncio

async def test_search():
    # Simple search with one keyword and ORDER BY
    print("Testing with single keyword 'diabetes' and ordering...")
    
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None,
        lambda: supabase.table("document_chunks") \
            .select("text_content, document_name, page_number") \
            .ilike("text_content", f"%diabetes%") \
            .order("id", desc=False) \
            .limit(10) \
            .execute()
    )
    
    print(f"✅ Found {len(result.data)} chunks")
    if result.data:
        for i, chunk in enumerate(result.data[:3], 1):
            print(f"\n{i}. {chunk['document_name']} (Page {chunk['page_number']})")
            print(f"   {chunk['text_content'][:100]}...")

asyncio.run(test_search())
