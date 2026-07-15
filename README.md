<div align="center">
  <img src="https://docs.hlquery.com/img/hlquery/2.png" alt="hlquery logo" width="200">
</div>

<div align="center">

**A modular Python client library for hlquery, designed with a familiar and intuitive API structure.**

[![Follow hlquery](https://img.shields.io/badge/Follow-%40hlquery-blue?logo=x&logoColor=white&labelColor=000000)](https://x.com/hlquery)
[![Python build](https://img.shields.io/badge/Python%20build-passing-brightgreen?logo=node.js&logoColor=white&labelColor=000000)](https://github.com/hlquery/python-api/actions/workflows/ci.yml)
[![python-api](https://img.shields.io/badge/GitHub-python--api-purple?logo=github&logoColor=white&labelColor=000000)](https://github.com/hlquery/python-api/)
[![hlquery](https://img.shields.io/badge/GitHub-hlquery-blue?logo=github&logoColor=white&labelColor=000000)](https://github.com/hlquery/hlquery/)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-a35a0f?logo=open-source-initiative&logoColor=white&labelColor=000000)](https://opensource.org/licenses/BSD-3-Clause)


</div>

### What is the hlquery Python API?

The hlquery Python API is the official Python client for [hlquery](https://github.com/hlquery/hlquery). It wraps the server's HTTP interface in a small modular client with helpers for collections, documents, search, and SQL.

It is intended for scripts, services, notebooks, and internal tools that want a cleaner integration layer than manual `urllib` or `requests` code.

### Why use it?

Use the Python client when you want a simple client layout with convenience methods, grouped APIs, and built-in auth handling. The client covers collections, documents, search, SQL, raw custom module routes, and direct PDF ingestion through one package.

### Install

Install the package locally to get the client and its integrated PDF reader dependency:

```bash
$ pip install -e .
```

You can also install the dependency list directly:

```bash
$ pip install -r requirements.txt
```

```python
from lib import Client
```

### PDF Documents

PDF support is installed with the package. Use `add_pdf` when you want the client to read a local PDF, extract text and metadata, build a document, and submit it to hlquery in one call:

```python
from lib import Client
client = Client('http://localhost:9200')

response = client.documents_api().add_pdf('books', './manual.pdf', {
    'document': {
        'source_type': 'pdf'
    }
})

print(response.get_body())
```

The helper fills `title`, `content`, `file_name`, `file_path`, `mime_type`, `page_count`, and PDF metadata fields by default. You can override the generated id, title, content field, or metadata behavior through the options argument:

```python
response = client.add_pdf_document('books', './manual.pdf', {
    'id': 'manual_v1',
    'title': 'Product Manual',
    'content_field': 'body',
    'include_metadata': False,
})
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

### Contributing

We welcome contributions from the community! All contributions must be released under the BSD 3-Clause license.

### How to Contribute

- Check existing [Python API issues](https://github.com/hlquery/python-api/issues) or create new ones
- Contribute Python client changes to [hlquery/python-api](https://github.com/hlquery/python-api)
- Contribute shared server/API changes to [hlquery/hlquery](https://github.com/hlquery/hlquery)
- Test and report bugs against the Python client
- Improve Python-specific documentation and examples

### Community

- 📖 [Documentation](https://docs.hlquery.com)
- 🐦 [X (Twitter)](https://x.com/hlquery)
- 🧪 [Python API GitHub](https://github.com/hlquery/python-api)
- 📦 [hlquery GitHub](https://github.com/hlquery/hlquery)

### License

The hlquery Python API is licensed under the [BSD 3-Clause License](https://opensource.org/licenses/BSD-3-Clause).
