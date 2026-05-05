"""
SAM Examples

Demonstrates SAM search, status, and history.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib import Client


def main():
    base_url = os.environ.get("HLQ_BASE_URL") or os.environ.get("HLQUERY_BASE_URL") or "http://localhost:9200"
    collection_name = sys.argv[1] if len(sys.argv) > 1 else "music"
    query = sys.argv[2] if len(sys.argv) > 2 else "queen of pop"
    token = sys.argv[3] if len(sys.argv) > 3 else None

    client = Client(base_url)

    if token:
        client.set_auth_token(token, "bearer")

    sam = client.sam()

    status = sam.status(collection_name)
    print(f"SAM status ({status.get_status_code()}): {status.get_body()}")

    results = sam.search(collection_name, query, {"limit": 5})
    print(f"SAM search ({results.get_status_code()}): {results.get_body()}")

    history = sam.history(collection_name, 5)
    print(f"SAM history ({history.get_status_code()}): {history.get_body()}")


if __name__ == "__main__":
    main()
