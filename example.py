#!/usr/bin/env python3
"""
hlquery Python API Comprehensive Example

This example tests ALL routes found in the HTTP server:
- Health, stats, metrics, status, root
- Collections (list, create, get, delete, update)
- Documents (list, get, add, update, delete, import, delete by filter)
- Search (regular search, vector search, multi-search)
- Synonyms, stopwords, overrides, aliases

Usage: python example.py [command] [token]
  Commands:
    cols   - Run collections API examples
    docs   - Run documents API examples
    open   - List and open collections (interactive)
    status - Show server health and status information
    help   - Show this help message
    all    - Run all examples (default)
"""

import sys
import json
import os
from lib import Client

# Configuration
BASE_URL = os.environ.get('HLQ_BASE_URL') or os.environ.get('HLQUERY_BASE_URL') or 'http://localhost:9200'

# Parse command line arguments
COMMAND = 'all'
TEST_TOKEN = None
OFFSET = 0
LIMIT = 1000
COLLECTION_NAME = None

if len(sys.argv) > 1:
    first_arg = sys.argv[1]
    if first_arg in ['cols', 'docs', 'open', 'status', 'help', 'all']:
        COMMAND = first_arg
        # Parse pagination for cols command: cols [offset] [limit] [token]
        if COMMAND == 'cols' and len(sys.argv) >= 3:
            try:
                OFFSET = int(sys.argv[2])
                if len(sys.argv) >= 4:
                    try:
                        LIMIT = int(sys.argv[3])
                        TEST_TOKEN = sys.argv[4] if len(sys.argv) > 4 else None
                    except ValueError:
                        TEST_TOKEN = sys.argv[3]
                else:
                    TEST_TOKEN = None
            except ValueError:
                TEST_TOKEN = sys.argv[2] if len(sys.argv) > 2 else None
        elif COMMAND == 'docs' and len(sys.argv) >= 3:
            # For docs command: docs [collection_name] [token]
            COLLECTION_NAME = sys.argv[2]
            TEST_TOKEN = sys.argv[3] if len(sys.argv) > 3 else None
        else:
            # Look for token in remaining args (skip numeric args)
            for i in range(2, len(sys.argv)):
                try:
                    int(sys.argv[i])  # Skip if numeric
                except ValueError:
                    TEST_TOKEN = sys.argv[i]
                    break
    else:
        # First arg is token, use 'all' command
        TEST_TOKEN = first_arg

# Show help if requested
if COMMAND == 'help':
    print("=== hlquery Python API Example ===\n")
    print("Usage: python example.py [command] [args...] [token]\n")
    print("Commands:")
    print("  cols   - List collections (with pagination)")
    print("          Usage: cols [offset] [limit] [token]")
    print("          Example: cols 0 200 (list first 200 collections)")
    print("  docs   - Run documents API examples")
    print("          Usage: docs [collection_name] [token]")
    print("          Example: docs my_collection")
    print("  open   - List and open collections (interactive)")
    print("  status - Show server health and status information")
    print("  help   - Show this help message")
    print("  all    - Run all examples (default)\n")
    print("Authentication:")
    print("  Token is optional. Only provide if server requires authentication.")
    print("  Example: python example.py cols 0 200 my_token")
    print("  Example: python example.py docs my_collection my_token\n")
    print("Examples:")
    print("  python example.py")
    print("  python example.py cols")
    print("  python example.py cols 0 200")
    print("  python example.py docs my_collection")
    print("  python example.py status")
    sys.exit(0)

print("=== hlquery Python API Example ===")
print(f"Command: {COMMAND}\n")

# Helper function to print results
def print_result(title, response, print_body=True):
    print("=" * 70)
    print(f"TEST: {title}")
    print("-" * 70)
    
    from lib.response import Response
    if isinstance(response, Response):  # Check if it's a Response object
        status = response.get_status_code()
        body = response.get_body()
        headers = response.get_headers()
        
        print(f"Status Code: {status}")
        
        if print_body and body:
            print("Response Body:")
            if isinstance(body, (dict, list)):
                print(json.dumps(body, indent=2, ensure_ascii=False))
            else:
                print(body)
        
        if 200 <= status < 300:
            print("✓ SUCCESS")
        else:
            print("✗ FAILED")
    else:
        print("Invalid response type")
    print()

# Helper to get first collection name
def get_first_collection(client):
    collections = client.list_collections(0, 1)
    if collections.get_status_code() == 200:
        body = collections.get_body()
        if 'collections' in body and body['collections']:
            first = body['collections'][0]
            return first['name'] if isinstance(first, dict) and 'name' in first else first
    return None

# Create client
client = Client(BASE_URL)

# Optional: Set authentication token if provided
# Uncomment and set token if your server requires authentication:
# auth_token = 'your_token_here'
# client.set_auth_token(auth_token, 'bearer')

if TEST_TOKEN:
    client.set_auth_token(TEST_TOKEN, 'bearer')
    print(f"Using authentication token: {TEST_TOKEN[:8]}...\n")

# ----------------------------------------------------------------====================================
# STATUS COMMAND
# ----------------------------------------------------------------====================================
if COMMAND == 'status':
    print("\n" + "#" * 70)
    print("# SERVER STATUS")
    print("#" * 70 + "\n")
    
    try:
        # GET /health
        print_result("GET /health", client.health())
        
        # GET /stats
        print_result("GET /stats", client.stats())
        
        # GET /etc (protocol codes)
        etc = client.execute_request('GET', '/etc')
        print_result("GET /etc (Protocol Codes)", etc)
        
        # GET /status
        status = client.execute_request('GET', '/status')
        print_result("GET /status", status)
        
        # GET / (Root Info) - show concise version
        info = client.info()
        print("=" * 70)
        print("TEST: GET / (Root Info)")
        print("-" * 70)
        if info:
            status_code = info.get_status_code()
            body = info.get_body()
            print(f"Status Code: {status_code}")
            if status_code >= 200 and status_code < 300 and isinstance(body, dict):
                print(f"Name: {body.get('name', 'N/A')}")
                print(f"Version: {body.get('version', 'N/A')}")
                print(f"Description: {body.get('description', 'N/A')}")
                print("✓ SUCCESS")
            else:
                print("Response Body:")
                print(json.dumps(body, indent=2))
                print("✓ SUCCESS")
        else:
            print("Invalid response")
        print()
    except Exception as e:
        print(f"Error getting status: {e}\n")
    sys.exit(0)

# ----------------------------------------------------------------====================================
# System APIs (only for 'all' command)
# ----------------------------------------------------------------====================================
if COMMAND == 'all':
    print("\n" + "#" * 70)
    print("# System APIs")
    print("#" * 70 + "\n")

    try:
        # GET /health
        print_result("GET /health", client.health())
        
        # GET /stats
        print_result("GET /stats", client.stats())
        
        # GET /etc (protocol codes)
        etc = client.execute_request('GET', '/etc')
        print_result("GET /etc (Protocol Codes)", etc)
        
        # GET /metrics (Prometheus-compatible)
        metrics = client.execute_request('GET', '/metrics')
        print_result("GET /metrics", metrics)
        
        # GET /status
        status = client.execute_request('GET', '/status')
        print_result("GET /status", status)
        
        # GET /
        print_result("GET / (Root)", client.info())
        
    except Exception as e:
        print(f"Error in system APIs: {e}\n")

# ----------------------------------------------------------------====================================
# COLLECTIONS API
# ----------------------------------------------------------------====================================
if COMMAND in ['all', 'cols', 'open']:
    print("\n" + "#" * 70)
    print("# COLLECTIONS API")
    print("#" * 70 + "\n")

    try:
        # GET /collections with pagination
        collections = client.list_collections(OFFSET, LIMIT)
        
        if COMMAND == 'cols':
            # Simple list display for cols command
            if collections.get_status_code() == 200:
                body = collections.get_body()
                if 'collections' in body:
                    cols_list = body['collections']
                    total = len(cols_list)
                    print(f"Collections (showing {total}, offset: {OFFSET}, limit: {LIMIT}):\n")
                    for col in cols_list:
                        name = col['name'] if isinstance(col, dict) and 'name' in col else col
                        print(f"  {name}")
                    print()
                else:
                    print("No collections found.\n")
            else:
                print(f"Error: {collections.get_status_code()}\n")
                body = collections.get_body()
                if isinstance(body, dict) and 'message' in body:
                    print(f"Message: {body['message']}\n")
        else:
            # Full display for 'all' and 'open' commands
            print_result("GET /collections (List)", collections)
            
            # Get first collection for other tests
            first_collection = get_first_collection(client)
            
            if first_collection and COMMAND == 'all':
                print(f"Using collection: {first_collection}\n")
                
                # GET /collections/{name}
                print_result("GET /collections/{name}", client.get_collection(first_collection))
                
                # GET /collections/{name} (fields formatted)
                print_result("GET /collections/{name}/fields (formatted)", 
                            client.get_collection_fields(first_collection))
                
                # Test creating a temporary collection
                import time
                test_collection_name = 'test_collection_' + str(int(time.time()))
                test_schema = {
                    'fields': [
                        {'name': 'title', 'type': 'string'},
                        {'name': 'content', 'type': 'string'},
                        {'name': 'embedding', 'type': 'float[]'}
                    ]
                }
                
                # POST /collections
                create_result = client.collections_api().create(test_collection_name, test_schema)
                print_result("POST /collections (Create)", create_result)
                
                if create_result.get_status_code() in [200, 201]:
                    # POST /collections/{name}/update
                    update_schema = {
                        'fields': [
                            {'name': 'title', 'type': 'string'},
                            {'name': 'content', 'type': 'string'},
                            {'name': 'embedding', 'type': 'float[]'},
                            {'name': 'tags', 'type': 'string[]'}
                        ]
                    }
                    update_result = client.collections_api().update(test_collection_name, update_schema)
                    print_result("POST /collections/{name}/update", update_result)
                    
                    # DELETE /collections/{name} (cleanup)
                    delete_result = client.collections_api().delete(test_collection_name)
                    print_result("DELETE /collections/{name}", delete_result)
            elif not first_collection:
                print("No collections found - skipping collection-specific tests\n")
        
        # For 'open' command, list all collections
        if COMMAND == 'open':
            collections = client.list_collections(0, 1000)
            if collections.get_status_code() == 200:
                body = collections.get_body()
                if 'collections' in body:
                    print("\nAvailable Collections:")
                    print("-" * 70)
                    for col in body['collections']:
                        name = col['name'] if isinstance(col, dict) and 'name' in col else col
                        print(f"  {name}")
                    print()
    
    except Exception as e:
        print(f"Error in collections API: {e}\n")

# ----------------------------------------------------------------====================================
# DOCUMENTS API
# ----------------------------------------------------------------====================================
if COMMAND in ['all', 'docs', 'open']:
    print("\n" + "#" * 70)
    print("# DOCUMENTS API")
    print("#" * 70 + "\n")

    # Use provided collection name or get first collection
    test_collection = COLLECTION_NAME or get_first_collection(client)
    if not test_collection:
        if COMMAND == 'docs' and not COLLECTION_NAME:
            print("Error: No collection name provided and no collections found.")
            print("Usage: python example.py docs [collection_name] [token]\n")
        else:
            print("No collections available - skipping document tests\n")
    else:
        if COMMAND == 'docs' and COLLECTION_NAME:
            print(f"Using collection: {test_collection}\n")
        try:
            # GET /collections/{name}/documents
            documents = client.list_documents(test_collection, {'offset': 0, 'limit': LIMIT})
            
            if COMMAND == 'docs':
                # Simple list display for docs command
                if documents.get_status_code() == 200:
                    body = documents.get_body()
                    if 'documents' in body:
                        docs_list = body['documents']
                        total = len(docs_list)
                        print(f"Documents in '{test_collection}' (showing {total}, limit: {LIMIT}):\n")
                        for doc in docs_list:
                            doc_id = doc.get('id') if isinstance(doc, dict) and 'id' in doc else doc
                            print(f"  {doc_id}")
                        print()
                    else:
                        print("No documents found.\n")
                else:
                    print(f"Error: {documents.get_status_code()}\n")
                    body = documents.get_body()
                    if isinstance(body, dict) and 'message' in body:
                        print(f"Message: {body['message']}\n")
            else:
                # Full display for 'all' command
                print_result("GET /collections/{name}/documents (List)", documents)
            
            # Get a document ID if available (for 'all' command)
            test_doc_id = None
            if COMMAND == 'all':
                documents = client.list_documents(test_collection, {'offset': 0, 'limit': 1})
                if documents.get_status_code() == 200:
                    body = documents.get_body()
                    if 'documents' in body and body['documents']:
                        doc = body['documents'][0]
                        test_doc_id = doc.get('id') if isinstance(doc, dict) else None
        
            if test_doc_id:
                # GET /collections/{name}/documents/{id}
                print_result("GET /collections/{name}/documents/{id}",
                            client.get_document(test_collection, test_doc_id))

            # POST /collections/{name}/documents (Add)
            import time
            new_doc = {
                'id': 'test_doc_' + str(int(time.time())),
                'title': 'Test Document',
                'content': 'This is a test document for API testing',
                'embedding': [0.1, 0.2, 0.3, 0.4, 0.5]  # Sample vector
            }
            add_result = client.documents_api().add(test_collection, new_doc)
            print_result("POST /collections/{name}/documents (Add)", add_result)

            if add_result.get_status_code() in [200, 201]:
                added_doc_id = new_doc['id']

                # PUT /collections/{name}/documents/{id}
                updated_doc = {
                    'title': 'Updated Test Document',
                    'content': 'This document has been updated'
                }
                update_result = client.documents_api().update(test_collection, added_doc_id, updated_doc)
                print_result("PUT /collections/{name}/documents/{id} (Update)", update_result)

                # POST /collections/{name}/documents/import
                bulk_docs = [
                    {'id': 'bulk_1', 'title': 'Bulk Doc 1', 'content': 'Content 1'},
                    {'id': 'bulk_2', 'title': 'Bulk Doc 2', 'content': 'Content 2'},
                    {'id': 'bulk_3', 'title': 'Bulk Doc 3', 'content': 'Content 3'}
                ]
                import_result = client.documents_api().import_documents(test_collection, bulk_docs)
                print_result("POST /collections/{name}/documents/import (Bulk Import)", import_result)

                # DELETE /collections/{name}/documents/{id}
                delete_result = client.documents_api().delete(test_collection, added_doc_id)
                print_result("DELETE /collections/{name}/documents/{id}", delete_result)

                # DELETE /collections/{name}/documents (by filter)
                delete_by_filter_result = client.documents_api().delete_by_filter(test_collection, 'title:Bulk*')
                print_result("DELETE /collections/{name}/documents (by filter)", delete_by_filter_result)

        except Exception as e:
            print(f"Error in documents API: {e}\n")

# ----------------------------------------------------------------====================================
# SEARCH API (only for 'all' command)
# ----------------------------------------------------------------====================================
if COMMAND == 'all':
    print("\n" + "#" * 70)
    print("# SEARCH API")
    print("#" * 70 + "\n")

    search_collection = get_first_collection(client)
    if not search_collection:
        print("No collections available - skipping search tests\n")
    else:
        try:
            # GET/POST /collections/{name}/documents/search (Regular search)
            search_params = {
                'q': 'test',
                'query_by': 'title,content',
                'limit': 5
            }
            print_result("GET /collections/{name}/documents/search (Regular Search)",
                        client.search(search_collection, search_params))

            # Sorting examples
            print("\n--- Sorting Examples ---\n")

            # Sort by relevance (default)
            search_relevance = {
                'q': 'test',
                'query_by': 'title,content',
                'sort_by': '_text_match:desc',
                'limit': 5
            }
            print_result("Search sorted by Relevance (Best Match)",
                        client.search(search_collection, search_relevance))

            # Sort by title alphabetically
            search_title = {
                'q': 'test',
                'query_by': 'title,content',
                'sort_by': 'title:asc',
                'limit': 5
            }
            print_result("Search sorted by Title (A-Z)",
                        client.search(search_collection, search_title))

            # Sort by document ID
            search_id = {
                'q': 'test',
                'query_by': 'title,content',
                'sort_by': 'id:asc',
                'limit': 5
            }
            print_result("Search sorted by Document ID (A-Z)",
                        client.search(search_collection, search_id))

            # Sort by date (if available)
            search_date = {
                'q': 'test',
                'query_by': 'title,content',
                'sort_by': 'created_at:desc',
                'limit': 5
            }
            print_result("Search sorted by Date (Newest First)",
                    client.search(search_collection, search_date))
        
            # POST /collections/{name}/documents/search (POST method)
            search_params_post = {
                'q': 'document',
                'query_by': 'title,content',
                'limit': 3,
                'sort_by': 'title:asc'
            }
            search_post = client.search_api().search(search_collection, {
                'body': search_params_post,
                'q': 'document',
                'query_by': 'title,content',
                'limit': 3
            })
            print_result("POST /collections/{name}/documents/search", search_post)

            # POST /collections/{name}/vector_search (Vector search body)
            vector_query = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]  # Sample 10D vector
            vector_params = {
                'body': {
                    'vector': vector_query,
                    'field_name': 'embedding',
                    'topk': 5,
                    'threshold': 0.0,
                    'normalize': True,
                    'include_vector': False
                }
            }
            print_result("POST /collections/{name}/vector_search (Vector Search)",
                        client.vector_search(search_collection, vector_params))

            # POST /multi_search
            multi_search_params = {
                'searches': [
                    {
                        'collection': search_collection,
                        'q': 'test',
                        'query_by': 'title'
                    },
                    {
                        'collection': search_collection,
                        'q': 'document',
                        'query_by': 'content'
                    }
                ]
            }
            print_result("POST /multi_search",
                        client.search_api().multi_search(multi_search_params['searches']))

            # POST /collections/{name}/documents/facet_counts
            facet_params = {
                'facet_by': 'title',
                'q': '*',
                'limit': 0
            }
            import urllib.parse
            facet_result = client.execute_request('POST',
                '/collections/' + urllib.parse.quote(search_collection) + '/documents/facet_counts',
                facet_params)
            print_result("POST /collections/{name}/documents/facet_counts", facet_result)

            # POST /collections/{name}/documents/export
            export_params = {
                'filter_by': '',
                'limit': 10
            }
            export_result = client.execute_request('POST',
                '/collections/' + urllib.parse.quote(search_collection) + '/documents/export',
                export_params)
            print_result("POST /collections/{name}/documents/export", export_result, print_body=False)
        
        except Exception as e:
            print(f"Error in search API: {e}\n")

# ----------------------------------------------------------------====================================
# SYNONYMS API (only for 'all' command)
# ----------------------------------------------------------------====================================
if COMMAND == 'all':
    print("\n" + "#" * 70)
    print("# SYNONYMS API")
    print("#" * 70 + "\n")

    synonym_collection = get_first_collection(client)
    if not synonym_collection:
        print("No collections available - skipping synonym tests\n")
    else:
        try:
            import urllib.parse
            # GET /collections/{name}/synonyms
            synonyms_list = client.execute_request('GET',
                '/collections/' + urllib.parse.quote(synonym_collection) + '/synonyms')
            print_result("GET /collections/{name}/synonyms", synonyms_list)

            # GET /synonyms (all collections)
            all_synonyms = client.execute_request('GET', '/synonyms')
            print_result("GET /synonyms (All Collections)", all_synonyms)

            # POST /collections/{name}/synonyms/{id}
            synonym_data = {
                'synonyms': ['car', 'automobile', 'vehicle']
            }
            create_synonym = client.execute_request('POST',
                '/collections/' + urllib.parse.quote(synonym_collection) + '/synonyms/test_synonym_1',
                synonym_data)
            print_result("POST /collections/{name}/synonyms/{id} (Create)", create_synonym)

            if create_synonym.get_status_code() in [200, 201]:
                # GET /collections/{name}/synonyms/{id}
                get_synonym = client.execute_request('GET',
                    '/collections/' + urllib.parse.quote(synonym_collection) + '/synonyms/test_synonym_1')
                print_result("GET /collections/{name}/synonyms/{id}", get_synonym)

                # DELETE /collections/{name}/synonyms/{id}
                delete_synonym = client.execute_request('DELETE',
                    '/collections/' + urllib.parse.quote(synonym_collection) + '/synonyms/test_synonym_1')
                print_result("DELETE /collections/{name}/synonyms/{id}", delete_synonym)
        
        except Exception as e:
            print(f"Error in synonyms API: {e}\n")

# ----------------------------------------------------------------====================================
# STOPWORDS API (only for 'all' command)
# ----------------------------------------------------------------====================================
if COMMAND == 'all':
    print("\n" + "#" * 70)
    print("# STOPWORDS API")
    print("#" * 70 + "\n")

    stopword_collection = get_first_collection(client)
    if not stopword_collection:
        print("No collections available - skipping stopword tests\n")
    else:
        try:
            import urllib.parse
            # GET /collections/{name}/stopwords
            stopwords_list = client.execute_request('GET',
                '/collections/' + urllib.parse.quote(stopword_collection) + '/stopwords')
            print_result("GET /collections/{name}/stopwords", stopwords_list)

            # GET /stopwords (all collections)
            all_stopwords = client.execute_request('GET', '/stopwords')
            print_result("GET /stopwords (All Collections)", all_stopwords)

            # POST /collections/{name}/stopwords
            stopword_data = {'word': 'the'}
            create_stopword = client.execute_request('POST',
                '/collections/' + urllib.parse.quote(stopword_collection) + '/stopwords',
                stopword_data)
            print_result("POST /collections/{name}/stopwords (Create)", create_stopword)

            if create_stopword.get_status_code() in [200, 201]:
                # DELETE /collections/{name}/stopwords/{word}
                delete_stopword = client.execute_request('DELETE',
                    '/collections/' + urllib.parse.quote(stopword_collection) + '/stopwords/the')
                print_result("DELETE /collections/{name}/stopwords/{word}", delete_stopword)
        
        except Exception as e:
            print(f"Error in stopwords API: {e}\n")

# ----------------------------------------------------------------====================================
# OVERRIDES API (only for 'all' command)
# ----------------------------------------------------------------====================================
if COMMAND == 'all':
    print("\n" + "#" * 70)
    print("# OVERRIDES API")
    print("#" * 70 + "\n")

    override_collection = get_first_collection(client)
    if not override_collection:
        print("No collections available - skipping override tests\n")
    else:
        try:
            import urllib.parse
            # GET /collections/{name}/overrides
            overrides_list = client.execute_request('GET',
                '/collections/' + urllib.parse.quote(override_collection) + '/overrides')
            print_result("GET /collections/{name}/overrides", overrides_list)

            # POST /collections/{name}/overrides/{id}
            override_data = {
                'rule': {
                    'query': 'test query',
                    'match': 'exact'
                },
                'includes': [
                    {'id': 'doc1', 'position': 1}
                ]
            }
            create_override = client.execute_request('POST',
                '/collections/' + urllib.parse.quote(override_collection) + '/overrides/test_override_1',
                override_data)
            print_result("POST /collections/{name}/overrides/{id} (Create)", create_override)

            if create_override.get_status_code() in [200, 201]:
                # GET /collections/{name}/overrides/{id}
                get_override = client.execute_request('GET',
                    '/collections/' + urllib.parse.quote(override_collection) + '/overrides/test_override_1')
                print_result("GET /collections/{name}/overrides/{id}", get_override)

                # DELETE /collections/{name}/overrides/{id}
                delete_override = client.execute_request('DELETE',
                    '/collections/' + urllib.parse.quote(override_collection) + '/overrides/test_override_1')
                print_result("DELETE /collections/{name}/overrides/{id}", delete_override)
        
        except Exception as e:
            print(f"Error in overrides API: {e}\n")

# ----------------------------------------------------------------====================================
# ALIASES API (only for 'all' command)
# ----------------------------------------------------------------====================================
if COMMAND == 'all':
    print("\n" + "#" * 70)
    print("# ALIASES API")
    print("#" * 70 + "\n")

    try:
        # GET /aliases
        aliases_list = client.execute_request('GET', '/aliases')
        print_result("GET /aliases", aliases_list)

        alias_collection = get_first_collection(client)
        if alias_collection:
            import time
            # POST /aliases/{name}
            alias_name = 'test_alias_' + str(int(time.time()))
            alias_data = {'collection_name': alias_collection}
            create_alias = client.execute_request('POST', '/aliases/' + alias_name, alias_data)
            print_result("POST /aliases/{name} (Create)", create_alias)

            if create_alias.get_status_code() in [200, 201]:
                # GET /aliases/{name}
                get_alias = client.execute_request('GET', '/aliases/' + alias_name)
                print_result("GET /aliases/{name}", get_alias)

                # DELETE /aliases/{name}
                delete_alias = client.execute_request('DELETE', '/aliases/' + alias_name)
                print_result("DELETE /aliases/{name}", delete_alias)
    
    except Exception as e:
        print(f"Error in aliases API: {e}\n")

# ----------------------------------------------------------------====================================
# SUMMARY (only show for 'all' command)
# ----------------------------------------------------------------====================================
if COMMAND == 'all':
    print("\n" + "#" * 70)
    print("# TESTING COMPLETE")
    print("#" * 70 + "\n")

    print("Routes have been tested. Check the output above for results.")
    print("Note: Some tests may fail if:")
    print("  - Authentication is required but no token was provided")
    print("  - Collections don't exist")
    print("  - Required data is missing")
    print()
    print("Usage: python example.py [command] [args...] [token]")
    print("  Commands:")
    print("    cols   - List collections (with pagination)")
    print("             Usage: cols [offset] [limit] [token]")
    print("             Example: cols 0 200")
    print("    docs   - Run documents API examples")
    print("             Usage: docs [collection_name] [token]")
    print("             Example: docs my_collection")
    print("    open   - List and open collections")
    print("    status - Show server health and status information")
    print("    help   - Show help message")
    print("    all    - Run all examples (default)")
    print()
