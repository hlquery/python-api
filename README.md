<div align="center">
  <img src="https://docs.hlquery.com/img/hlquery/2.png" alt="hlquery logo" width="200">
</div>

<div align="center">

**A modular Python client library for hlquery, designed with a familiar and intuitive API structure.**

[![Follow hlquery](https://img.shields.io/badge/Follow-%40hlquery-blue?logo=x&logoColor=white)](https://x.com/hlquery)
[![Commit Activity](https://img.shields.io/github/commit-activity/m/hlquery/hlquery)](https://github.com/hlquery/python-api/pulse)
[![GitHub](https://img.shields.io/badge/GitHub-python--api-181717?logo=github&logoColor=white)](https://github.com/hlquery/python-api/stargazers)
[![hlquery](https://img.shields.io/badge/GitHub-hlquery-blue?logo=github&logoColor=white)](https://github.com/hlquery/hlquery/stargazers)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

</div>

### What is the hlquery Python API?

The hlquery Python API is the official Python client for [hlquery](https://github.com/hlquery/hlquery). It wraps the server's HTTP interface in a small modular client with helpers for collections, documents, search, SQL, and SAM.

It is intended for scripts, services, notebooks, and internal tools that want a cleaner integration layer than manual `urllib` or `requests` code.

### Why use it?

- Simple client layout with convenience methods and grouped APIs.
- Built-in auth handling.
- Standard-library-first design for the core client.
- Coverage for SAM and raw custom module routes.

### Why choose it over raw HTTP?

Choose the Python client over raw HTTP when you want less repetitive request and JSON parsing code, predictable response helpers, and application-level hlquery calls that remain easy to read.

### Install

Core client usage has no dependencies beyond Python's standard library.

```python
from lib import Client
```

Editable local install:

```bash
pip install -e .
```

Optional PDF parsing:

```bash
pip install PyPDF2
```

### Quick Start

```python
import os
from lib import Client

client = Client(os.environ.get('HLQ_BASE_URL') or os.environ.get('HLQUERY_BASE_URL') or 'http://localhost:9200')

health = client.health()
print(f"Status: {health.get_status_code()}")

collections = client.list_collections(0, 10)
if collections.is_success():
    print(collections.get_body())
```

### Auth

```python
client = Client('http://localhost:9200', {
    'token': 'your_token_here',
    'auth_method': 'bearer'
})

client.set_auth_token('your_token_here', 'bearer')
client.set_auth_token('your_api_key_here', 'api-key')
```

### SAM

SAM is separate from vector search. It performs term and intent-style lookup, not vector similarity search.

```python
from lib import Client

client = Client('http://localhost:9200')
sam = client.sam()

status = sam.status('music')
history = sam.history('music', 5)
results = sam.search('music', 'queen of pop', {
    'limit': 5,
})

print(status.get_body())
print(history.get_body())
print(results.get_body())
```

### SQL

```python
sql = client.sql_api()

rows = sql.query('SHOW COLLECTIONS;')
books = sql.search(
    'books',
    'SELECT id, title FROM books ORDER BY title ASC LIMIT 3;'
)

print(rows.get_body())
print(books.get_body())
```

### Reduce Text Example

Use the raw request helper for custom module routes:

```python
module_response = client.execute_request(
    "GET",
    "/modules/<name>/<route>",
    query_params={
        "q": "example query",
    },
)

print(module_response.get_body())
```

### Contributing

We welcome contributions from the community! All contributions must be released under the BSD 3-Clause license.

### How to Contribute

- Check existing [issues](https://github.com/hlquery/hlquery/issues) or create new ones
- Contribute to client libraries (Node.js, Go, Java, Python, PHP, Ruby, Rust, Perl, C++)
- Test and report bugs
- Improve documentation

### Community

- 📖 [Documentation](https://docs.hlquery.com)
- 🐦 [X (Twitter)](https://x.com/hlquery)
- 📦 [GitHub](https://github.com/hlquery/hlquery)

### License

hlquery is licensed under the [BSD 3-Clause License](https://opensource.org/licenses/BSD-3-Clause).
