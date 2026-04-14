"""
Search Examples

Demonstrates search operations
"""

import sys
import os

# Add parent directory to path to allow importing lib
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib import Client

client = Client('http://localhost:9200')

# Get a real collection name first
collections = client.list_collections(0, 1)
if collections.is_success():
    body = collections.get_body()
    if body.get('collections'):
        collection_name = body['collections'][0]['name']
        print(f"Using collection: {collection_name}\n")
        
        # Simple search
        results = client.search(collection_name, {
            'q': 'test',
            'query_by': 'title,content',
            'limit': 10
        })
        print(f"Search results: {results.get_body()}")
        
        # Search with highlighting
        results = client.search(collection_name, {
            'q': 'test',
            'query_by': 'title,content',
            'highlight': True,
            'highlight_fields': ['title', 'content'],
            'limit': 10
        })
        print(f"Search with highlights: {results.get_body()}")
    else:
        print("No collections found")
        collection_name = None
else:
    print("Failed to list collections")
    collection_name = None

if collection_name:
    # Search with filters and sorting
    results = client.search(collection_name, {
        'q': 'test',
        'query_by': 'title',
        'sort_by': 'title',
        'limit': 5
    })
    print(f"Filtered search: {results.get_body()}")
    
    # Supported query semantics
    # Field-specific search
    results = client.search(collection_name, {
        'q': 'title:laptop',
        'query_by': 'title,content',
        'limit': 10
    })
    print(f"Field search: {results.get_body()}")
    
    # Boolean OR query
    results = client.search(collection_name, {
        'q': 'title:laptop OR title:notebook',
        'query_by': 'title,content',
        'limit': 10
    })
    print(f"Boolean OR search: {results.get_body()}")
    
    # Boolean NOT query
    results = client.search(collection_name, {
        'q': 'title:laptop NOT title:refurbished',
        'query_by': 'title,content',
        'limit': 10
    })
    print(f"Boolean NOT search: {results.get_body()}")
    
    # Phrase search
    results = client.search(collection_name, {
        'q': '"wireless keyboard"',
        'query_by': 'title',
        'limit': 10
    })
    print(f"Phrase search: {results.get_body()}")
    
    # Wildcard search
    results = client.search(collection_name, {
        'q': 'laptop*',
        'query_by': 'title,content',
        'limit': 10
    })
    print(f"Wildcard search: {results.get_body()}")
    
    # query_by restriction
    results = client.search(collection_name, {
        'q': 'laptop',
        'query_by': 'title',
        'limit': 10
    })
    print(f"query_by restricted search: {results.get_body()}")
    
    # Filter operators belong in filter_by
    results = client.search(collection_name, {
        'q': '*',
        'query_by': 'title,content',
        'filter_by': 'price:>100&&category:electronics',
        'limit': 10
    })
    print(f"Filtered search: {results.get_body()}")
    
    # Vector search
    vector_query = [0.1, 0.2, 0.3, 0.4, 0.5]
    results = client.vector_search(collection_name, {
        'body': {
            'vector': vector_query,
            'field_name': 'embedding',
            'topk': 5,
            'threshold': 0.0,
            'include_distance': True,
            'query_params': {'ef': 64, 'nprobe': 4, 'is_linear': True}
        }
    })
    print(f"Vector search: {results.get_body()}")
    
    # Multi-search
    searches = [
        {'collection': collection_name, 'q': 'test', 'query_by': 'title'},
        {'collection': collection_name, 'q': 'test', 'query_by': 'content'}
    ]
    results = client.search_api().multi_search(searches)
    print(f"Multi-search: {results.get_body()}")
