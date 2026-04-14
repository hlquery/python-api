"""
Documents Examples

Demonstrates document CRUD operations
"""

import sys
import os

# Add parent directory to path to allow importing lib
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib import Client

client = Client('http://localhost:9200')

# List documents - get a real collection name first
collections = client.list_collections(0, 1)
if collections.is_success():
    body = collections.get_body()
    if body.get('collections'):
        collection_name = body['collections'][0]['name']
        documents = client.list_documents(collection_name, {'offset': 0, 'limit': 10})
        print(f"Documents: {documents.get_body()}")
    else:
        print("No collections found")
        collection_name = None
else:
    print("Failed to list collections")
    collection_name = None

if collection_name:
    # Get document
    if documents.is_success():
        body = documents.get_body()
        if body.get('documents'):
            doc_id = body['documents'][0].get('id')
            if doc_id:
                document = client.get_document(collection_name, doc_id)
                print(f"Document: {document.get_body()}")

    # Add document
    import time
    new_doc = {
        'id': 'doc_' + str(int(time.time())),
        'title': 'Test Document',
        'content': 'This is a test document'
    }
    result = client.documents_api().add(collection_name, new_doc)
    print(f"Add result: {result.get_status_code()}")
    
    if result.is_success():
        doc_id = new_doc['id']
        # Update document
        updated_doc = {
            'title': 'Updated Document',
            'content': 'Updated content'
        }
        result = client.documents_api().update(collection_name, doc_id, updated_doc)
        print(f"Update result: {result.get_status_code()}")
        
        # Delete document
        result = client.documents_api().delete(collection_name, doc_id)
        print(f"Delete result: {result.get_status_code()}")
