"""
Create query_logs table in Supabase for tracking user queries
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.supabase_client import supabase

def create_query_logs_table():
    """
    Creates the query_logs table in Supabase
    
    Table schema:
    - id: auto-increment primary key
    - query: user's search query
    - top_k: number of results requested
    - timestamp: when the query was made
    - contexts_found: number of contexts retrieved
    - success: whether the query was successful
    - response_preview: first 200 chars of answer
    """
    
    print("🔧 Creating query_logs table in Supabase...")
    print("\nNote: You need to run this SQL in your Supabase SQL Editor:")
    print("=" * 80)
    
    sql = """
-- Create query_logs table for tracking user queries
CREATE TABLE IF NOT EXISTS query_logs (
    id BIGSERIAL PRIMARY KEY,
    query TEXT NOT NULL,
    top_k INTEGER NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    contexts_found INTEGER DEFAULT 0,
    success BOOLEAN DEFAULT TRUE,
    response_preview TEXT,
    error_message TEXT
);

-- Create index on timestamp for faster queries
CREATE INDEX IF NOT EXISTS idx_query_logs_timestamp ON query_logs(timestamp DESC);

-- Create index on success for filtering
CREATE INDEX IF NOT EXISTS idx_query_logs_success ON query_logs(success);

-- Enable Row Level Security (optional)
ALTER TABLE query_logs ENABLE ROW LEVEL SECURITY;

-- Create policy to allow all operations (adjust based on your needs)
CREATE POLICY "Allow all operations on query_logs" ON query_logs
    FOR ALL
    USING (true)
    WITH CHECK (true);
"""
    
    print(sql)
    print("=" * 80)
    print("\n✅ Copy and paste the SQL above into your Supabase SQL Editor")
    print("📍 Go to: Supabase Dashboard → SQL Editor → New Query")
    print("\nAfter creating the table, the query logging will work automatically!")

if __name__ == "__main__":
    create_query_logs_table()
