"""
Basic Usage Example

Demonstrates basic client initialization and simple operations
"""

import sys
import os

# Add parent directory to path to allow importing lib
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib import Client

client = Client('http://localhost:9200')

# Health check
health = client.health()
print(f"Health: {health.get_status_code()}")

# List collections
collections = client.list_collections(0, 10)
if collections.is_success():
    body = collections.get_body()
    print(f"Found {len(body.get('collections', []))} collections")
