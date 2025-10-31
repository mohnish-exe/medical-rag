# Query Logging System

## Overview

The RAG system now automatically logs all user queries to Supabase for analytics and monitoring.

## Features

- ✅ Automatic logging of all queries
- ✅ Tracks query text, top_k, timestamp, contexts found, success status
- ✅ Stores response preview (first 200 chars)
- ✅ Records error messages for failed queries
- ✅ Non-blocking (doesn't slow down API)
- ✅ Analytics endpoint for viewing logs

## Setup

### 1. Create the Query Logs Table

Run the setup script to see the SQL:

```bash
python scripts/create_query_logs_table.py
```

Then copy the SQL and run it in your Supabase SQL Editor:

1. Go to Supabase Dashboard
2. Navigate to SQL Editor
3. Create a New Query
4. Paste the SQL and execute

### 2. Table Schema

```sql
query_logs (
    id              BIGSERIAL PRIMARY KEY,
    query           TEXT NOT NULL,
    top_k           INTEGER NOT NULL,
    timestamp       TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    contexts_found  INTEGER DEFAULT 0,
    success         BOOLEAN DEFAULT TRUE,
    response_preview TEXT,
    error_message   TEXT
)
```

## API Endpoints

### Get Query Logs

```bash
GET /query-logs?limit=50&success_only=false
```

**Parameters:**

- `limit` (optional): Max number of logs to return (default: 50, max: 500)
- `success_only` (optional): If true, only return successful queries (default: false)

**Response:**

```json
{
  "total_queries": 150,
  "successful": 142,
  "failed": 8,
  "average_contexts_found": 3.2,
  "logs": [
    {
      "id": 1,
      "query": "What is the Tdap vaccination schedule?",
      "top_k": 3,
      "timestamp": "2025-10-28T10:30:00Z",
      "contexts_found": 3,
      "success": true,
      "response_preview": "The Tdap vaccine is recommended...",
      "error_message": null
    }
  ]
}
```

## Viewing Logs

### Using the Log Viewer Script

View last 20 queries:

```bash
python view_query_logs.py
```

View last 50 queries:

```bash
python view_query_logs.py all 50
```

View only successful queries:

```bash
python view_query_logs.py success
```

View most popular queries:

```bash
python view_query_logs.py popular
```

### Using curl

```bash
# View last 20 queries
curl http://localhost:8000/query-logs

# View last 100 queries
curl http://localhost:8000/query-logs?limit=100

# View only successful queries
curl "http://localhost:8000/query-logs?success_only=true"
```

## Analytics Use Cases

### 1. Monitor Query Performance

Track which queries succeed vs fail to identify issues.

### 2. Identify Popular Topics

See what users are searching for most frequently.

### 3. Improve Search Relevance

Analyze queries that return few contexts to improve indexing.

### 4. Debug Issues

Review failed queries and error messages for troubleshooting.

### 5. Usage Analytics

Track API usage patterns, peak times, and query volume.

## Privacy Notes

- Logs are stored in Supabase with Row Level Security enabled
- Consider implementing data retention policies
- Be mindful of storing sensitive medical queries
- You can add user IDs or session tracking if needed

## Example Queries in Supabase

```sql
-- View recent queries
SELECT * FROM query_logs
ORDER BY timestamp DESC
LIMIT 20;

-- Count queries by success status
SELECT success, COUNT(*)
FROM query_logs
GROUP BY success;

-- Find queries with no contexts
SELECT query, timestamp
FROM query_logs
WHERE contexts_found = 0
ORDER BY timestamp DESC;

-- Most popular queries
SELECT query, COUNT(*) as count
FROM query_logs
GROUP BY query
ORDER BY count DESC
LIMIT 10;

-- Average contexts found per query
SELECT AVG(contexts_found) as avg_contexts
FROM query_logs
WHERE success = true;

-- Queries by hour
SELECT
    DATE_TRUNC('hour', timestamp) as hour,
    COUNT(*) as query_count
FROM query_logs
GROUP BY hour
ORDER BY hour DESC;
```

## Disabling Logging

If you want to disable logging temporarily, comment out the `await log_query()` calls in `rag_api.py`.

## Future Enhancements

- [ ] Add user ID/session tracking
- [ ] Track response time
- [ ] Add query categorization (symptoms, treatment, diagnosis, etc.)
- [ ] Export logs to CSV for analysis
- [ ] Add dashboard for real-time monitoring
- [ ] Implement data retention/cleanup policies
