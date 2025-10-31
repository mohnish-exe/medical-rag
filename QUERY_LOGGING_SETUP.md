# 🎯 Query Logging Setup - Quick Guide

## ✅ What Was Added

Your RAG system now automatically logs ALL user queries including:

- Query text
- Number of results requested (top_k)
- Timestamp
- Number of contexts found
- Success/failure status
- First 200 characters of the answer
- Error messages (if any)

## 📋 Setup Steps

### Step 1: Create the Database Table

**Copy this SQL and run it in Supabase SQL Editor:**

```sql
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

CREATE INDEX idx_query_logs_timestamp ON query_logs(timestamp DESC);
CREATE INDEX idx_query_logs_success ON query_logs(success);

ALTER TABLE query_logs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow all operations on query_logs" ON query_logs
    FOR ALL
    USING (true)
    WITH CHECK (true);
```

**Where to run it:**

1. Go to your Supabase Dashboard
2. Click "SQL Editor" in the left sidebar
3. Click "New Query"
4. Paste the SQL above
5. Click "Run" button

### Step 2: That's It!

Once you create the table, logging will work automatically. The server is already running with logging enabled!

## 📊 How to View Logs

### Option 1: Using the Viewer Script

```bash
# View last 20 queries
python view_query_logs.py

# View last 100 queries
python view_query_logs.py all 100

# View only successful queries
python view_query_logs.py success

# View most popular queries
python view_query_logs.py popular
```

### Option 2: Using the API

```bash
# Get query logs via API
curl http://localhost:8000/query-logs

# Get last 100 logs
curl http://localhost:8000/query-logs?limit=100
```

### Option 3: Directly in Supabase

Go to Supabase → Table Editor → query_logs

## 🔍 Example Use Cases

**Find queries with no results:**

```sql
SELECT query, timestamp
FROM query_logs
WHERE contexts_found = 0
ORDER BY timestamp DESC;
```

**Most popular queries:**

```sql
SELECT query, COUNT(*) as count
FROM query_logs
GROUP BY query
ORDER BY count DESC
LIMIT 10;
```

**Failed queries:**

```sql
SELECT query, error_message, timestamp
FROM query_logs
WHERE success = false
ORDER BY timestamp DESC;
```

## 📁 Files Added/Modified

**New Files:**

- `scripts/create_query_logs_table.py` - Shows SQL for table creation
- `view_query_logs.py` - View logs from command line
- `docs/QUERY_LOGGING.md` - Full documentation

**Modified Files:**

- `rag_api.py` - Added logging to `/query` endpoint
  - Added `log_query()` function
  - Added `/query-logs` endpoint for viewing logs
  - Logs every query automatically (non-blocking)

## ⚡ Quick Test

After creating the table in Supabase:

```bash
# 1. Make a test query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is diabetes?", "top_k": 3}'

# 2. View the log
python view_query_logs.py
```

You should see your query logged with timestamp, contexts found, and answer preview!

## 💡 Benefits

- ✅ Track what users are searching for
- ✅ Identify queries that fail or return no results
- ✅ Monitor API usage patterns
- ✅ Improve search quality based on real queries
- ✅ Debug issues with specific queries
- ✅ Analyze popular topics

## 🔒 Privacy Note

Query logs contain user search queries. Consider:

- Adding data retention policies
- Anonymizing sensitive queries
- Securing access to the logs
- Complying with data protection regulations
