"""
Collections Examples

Demonstrates collection management operations
"""

import sys
import os

# Add parent directory to path to allow importing lib
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib import Client

client = Client('http://localhost:9200')

# List collections
collections = client.list_collections(0, 10)
print(f"Collections: {collections.get_body()}")

# Get collection details
if collections.is_success():
    body = collections.get_body()
    if body.get('collections'):
        first_collection = body['collections'][0]
        collection_name = first_collection['name'] if isinstance(first_collection, dict) else first_collection
        
        # Get collection
        collection = client.get_collection(collection_name)
        print(f"Collection details: {collection.get_body()}")
        
        # Get formatted fields
        fields = client.get_collection_fields(collection_name)
        print(f"Collection fields: {fields.get_body()}")
