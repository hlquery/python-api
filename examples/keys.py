#!/usr/bin/env python3
"""
hlquery Python Example - API Keys Management

This example demonstrates how to create, list, and delete API keys.
"""

import sys
import os

# Add parent directory to path to import lib
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.client import Client

# Replace with your hlquery master admin token
ADMIN_TOKEN = 'your_admin_token_here'
BASE_URL = 'http://localhost:9200'

def run():
    try:
        client = Client(BASE_URL)
        client.set_auth_token(ADMIN_TOKEN)

        print('1. Creating a scoped search key for "products" collection...')
        create_resp = client.keys_api().create({
            'description': 'Public search key for products',
            'collections': ['products'],
            'actions': ['search'],
            'embedded_filters': 'is_public:=true'
        })

        if create_resp.get_status_code() == 201:
            body = create_resp.get_body()
            new_key = body['key']
            key_id = body['id']
            print(f'   ✓ Key created: {new_key}')
            print(f'   ✓ Key ID: {key_id}')

            print('\n2. Listing all API keys...')
            list_resp = client.keys_api().list()
            print(f"   ✓ Found {len(list_resp.get_body()['keys'])} keys")

            print('\n3. Getting key details...')
            get_resp = client.keys_api().get(key_id)
            print(f"   ✓ Key description: {get_resp.get_body()['description']}")

            print('\n4. Updating key permissions...')
            client.keys_api().update(key_id, {
                'actions': ['search', 'create']
            })
            print('   ✓ Permissions updated')

            print('\n5. Deleting the key...')
            client.keys_api().delete(key_id)
            print('   ✓ Key deleted')
        else:
            print(f'   ✗ Failed to create key: {create_resp.get_body()}')

    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    run()
