from core.supabase_client import supabase

# Test database connection
result = supabase.table('document_chunks').select('text_content', count='exact').ilike('text_content', '%diabetes%').limit(5).execute()

print(f'✅ Database connection working!')
print(f'📊 Found {result.count} chunks containing "diabetes"')
if result.data:
    print(f'📄 Sample: {result.data[0]["text_content"][:150]}...')
else:
    print('⚠️ No data returned')
