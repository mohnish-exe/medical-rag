"""
View query logs from the RAG system
"""
import requests
import json
from datetime import datetime

API_URL = "http://localhost:8000"

def view_logs(limit=20, success_only=False):
    """View recent query logs"""
    print("=" * 100)
    print("📊 RAG QUERY LOGS VIEWER")
    print("=" * 100)
    
    try:
        response = requests.get(f"{API_URL}/query-logs", params={
            "limit": limit,
            "success_only": success_only
        })
        
        if response.status_code == 200:
            data = response.json()
            
            if "error" in data:
                print(f"\n❌ {data['error']}")
                print(f"💡 {data['message']}")
                return
            
            # Display summary
            print(f"\n📈 SUMMARY:")
            print(f"   Total Queries: {data['total_queries']}")
            print(f"   ✅ Successful: {data['successful']}")
            print(f"   ❌ Failed: {data['failed']}")
            print(f"   📚 Avg Contexts Found: {data['average_contexts_found']}")
            
            print(f"\n{'─' * 100}")
            print(f"📋 RECENT QUERIES (showing {len(data['logs'])} logs):")
            print(f"{'─' * 100}")
            
            for i, log in enumerate(data['logs'], 1):
                timestamp = log.get('timestamp', 'N/A')
                if timestamp != 'N/A':
                    # Parse ISO timestamp
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    timestamp = dt.strftime('%Y-%m-%d %H:%M:%S')
                
                query = log.get('query', 'N/A')
                top_k = log.get('top_k', 'N/A')
                contexts = log.get('contexts_found', 0)
                success = log.get('success', False)
                preview = log.get('response_preview', 'N/A')
                error = log.get('error_message', '')
                
                status = "✅" if success else "❌"
                
                print(f"\n{i}. {status} [{timestamp}]")
                print(f"   Query: \"{query}\"")
                print(f"   Top-K: {top_k} | Contexts Found: {contexts}")
                
                if success and preview and preview != 'N/A':
                    # Show first 150 chars of response
                    preview_text = preview[:150] + "..." if len(preview) > 150 else preview
                    print(f"   Answer: {preview_text}")
                elif not success and error:
                    print(f"   Error: {error}")
                
                if i % 10 == 0 and i < len(data['logs']):
                    print(f"\n{'─' * 100}")
            
            print(f"\n{'=' * 100}")
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
    
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to API server")
        print("💡 Make sure the server is running: python rag_api.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")

def view_popular_queries(limit=10):
    """View most common queries"""
    print("=" * 100)
    print("🔥 POPULAR QUERIES")
    print("=" * 100)
    
    try:
        response = requests.get(f"{API_URL}/query-logs", params={"limit": 500})
        
        if response.status_code == 200:
            data = response.json()
            
            if "error" in data or not data.get('logs'):
                print("\n⚠️ No query logs available yet")
                return
            
            # Count query frequencies
            query_counts = {}
            for log in data['logs']:
                query = log.get('query', '').lower().strip()
                if query:
                    query_counts[query] = query_counts.get(query, 0) + 1
            
            # Sort by frequency
            sorted_queries = sorted(query_counts.items(), key=lambda x: x[1], reverse=True)[:limit]
            
            print(f"\nTop {len(sorted_queries)} most searched queries:\n")
            for i, (query, count) in enumerate(sorted_queries, 1):
                print(f"{i}. [{count}x] \"{query[:80]}{'...' if len(query) > 80 else ''}\"")
            
            print(f"\n{'=' * 100}")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    import sys
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "popular":
            view_popular_queries()
        elif command == "success":
            view_logs(limit=20, success_only=True)
        elif command == "all":
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 50
            view_logs(limit=limit)
        else:
            print("Usage:")
            print("  python view_query_logs.py           # View last 20 queries")
            print("  python view_query_logs.py all 50    # View last 50 queries")
            print("  python view_query_logs.py success   # View only successful queries")
            print("  python view_query_logs.py popular   # View most popular queries")
    else:
        # Default: show last 20 queries
        view_logs(limit=20)
