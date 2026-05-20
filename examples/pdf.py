"""
PDF Parsing Example

Usage:
    python examples/pdf.py <collection> <pdf-path> [token]
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib import Client


def main():
    if len(sys.argv) < 3:
        print("Usage: python examples/pdf.py <collection> <pdf-path> [token]")
        sys.exit(1)

    collection_name = sys.argv[1]
    pdf_path = sys.argv[2]
    token = sys.argv[3] if len(sys.argv) > 3 else None

    client = Client('http://localhost:9200')

    if token:
        client.set_auth_token(token, 'bearer')

    response = client.documents_api().add_pdf(collection_name, pdf_path, {
        'document': {
            'source_type': 'pdf',
            'source_path': os.path.abspath(pdf_path)
        }
    })

    print(f"Status: {response.get_status_code()}")
    print(response.get_body())


if __name__ == '__main__':
    main()
