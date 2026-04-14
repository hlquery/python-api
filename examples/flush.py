"""
Flush Example

Demonstrates the flush operation:
1. Create a fake collection
2. Create a fake document
3. Check collection count
4. Flush all data
5. Re-check collection count (should be 0)
"""

import sys
import os
import time

# Add parent directory to path to allow importing lib
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib import Client

client = Client('http://localhost:9200')

print("=" * 70)
print("FLUSH EXAMPLE")
print("=" * 70)
print()

# Step 1: Create a fake collection
print("Step 1: Creating a fake collection...")
collection_name = 'flush_test_collection_' + str(int(time.time()))

schema = {
    'fields': [
        {'name': 'title', 'type': 'string'},
        {'name': 'content', 'type': 'string'},
        {'name': 'value', 'type': 'int'}
    ]
}

create_result = client.collections_api().create(collection_name, schema)
if create_result.is_success():
    print(f"  ✓ Collection '{collection_name}' created successfully")
else:
    print(f"  ✗ Failed to create collection: {create_result.get_status_code()}")
    print(f"  Error: {create_result.get_body()}")
    sys.exit(1)

print()

# Step 2: Create a fake document
print("Step 2: Creating a fake document...")
doc = {
    'id': 'flush_test_doc_' + str(int(time.time())),
    'title': 'Flush Test Document',
    'content': 'This is a test document for flush example',
    'value': 42
}

add_result = client.documents_api().add(collection_name, doc)
if add_result.is_success():
    print(f"  ✓ Document '{doc['id']}' added successfully")
else:
    print(f"  ✗ Failed to add document: {add_result.get_status_code()}")
    print(f"  Error: {add_result.get_body()}")

print()

# Step 3: Check collection count before flush
print("Step 3: Checking collection count before flush...")
collections_before = client.list_collections(0, 1000)
if collections_before.is_success():
    body = collections_before.get_body()
    collections_list = body.get('collections', [])
    count_before = len(collections_list)
    print(f"  Collections before flush: {count_before}")
    if count_before == 0:
        print("  ⚠ Warning: No collections found before flush")
else:
    print(f"  ✗ Failed to list collections: {collections_before.get_status_code()}")
    count_before = 0

print()

# Step 4: Flush all data
print("Step 4: Flushing all data...")
flush_result = client.flush()
if flush_result.is_success():
    body = flush_result.get_body()
    collections_deleted = body.get('collections_deleted', 0)
    print(f"  ✓ Flush completed successfully")
    print(f"  Collections deleted: {collections_deleted}")
    print(f"  Message: {body.get('message', 'N/A')}")
else:
    print(f"  ✗ Flush failed: {flush_result.get_status_code()}")
    print(f"  Error: {flush_result.get_body()}")
    sys.exit(1)

print()

# Step 5: Re-check collection count after flush
print("Step 5: Checking collection count after flush...")
collections_after = client.list_collections(0, 1000)
if collections_after.is_success():
    body = collections_after.get_body()
    collections_list = body.get('collections', [])
    count_after = len(collections_list)
    print(f"  Collections after flush: {count_after}")
    
    if count_after == 0:
        print("  ✓ SUCCESS: All collections have been flushed")
    else:
        print(f"  ⚠ Warning: Expected 0 collections, but found {count_after}")
else:
    print(f"  ✗ Failed to list collections: {collections_after.get_status_code()}")
    count_after = -1

print()
print("=" * 70)
print("FLUSH EXAMPLE COMPLETED")
print("=" * 70)
print(f"Summary:")
print(f"  Collections before flush: {count_before}")
print(f"  Collections after flush: {count_after}")
print()
