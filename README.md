<div align="center">
  <img src="https://docs.hlquery.com/img/hlquery/2.png" alt="hlquery logo" width="200">
</div>

<div align="center">

**A modular Python client library for hlquery, designed with a familiar and intuitive API structure.**


[![Follow hlquery](https://img.shields.io/badge/Follow-%40hlquery-blue?logo=x&logoColor=white)](https://x.com/hlquery)
[![Commit Activity](https://img.shields.io/github/commit-activity/m/hlquery/hlquery)](https://github.com/hlquery/python-api/pulse)
[![python-api](https://img.shields.io/badge/Follow-%40hlquery-blue?logo=x&logoColor=white)](https://github.com/hlquery/python-api/stargazers)
[![GitHub](https://img.shields.io/badge/GitHub-hlquery-blue?logo=github&logoColor=white)](https://github.com/hlquery/hlquery/stargazers)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

</div>

### hlquery Python API Client


### Features

-  **Modular Architecture**: Clean separation of concerns with organized classes
-  **Intuitive API**: Familiar and easy-to-use structure
-  **Authentication Support**: Bearer token and X-API-Key authentication
-  **Flexible Parameters**: Support for multiple parameter formats
-  **Auto-detection**: Automatically detects searchable fields when not specified
-  **SAM Support**: Search, status, and history helpers for SAM endpoints
-  **Type-safe Responses**: Response objects with helper methods
-  **Comprehensive Validation**: Input validation for all operations
-  **No External Dependencies**: Uses Python's built-in `urllib` and `json` modules
-  **Professional Structure**: Well-organized and modular architecture

### Installation

Core client usage has no dependencies beyond Python's standard library. PDF parsing uses the optional `PyPDF2` package.

Simply import the client:

```python
import os
from lib import Client
```

Or install as a package:

```bash
pip install -e .
```

### Optional PDF Support

Install the optional PDF parser when you want to index local PDF files directly through the Python client:

```bash
pip install PyPDF2
```

CSV support is built in and does not require any extra package.

## Quick Start

### Basic Usage

```python
from lib import Client

# Initialize client
client = Client(os.environ.get('HLQ_BASE_URL') or os.environ.get('HLQUERY_BASE_URL') or 'http://localhost:9200')

# Health check
health = client.health()
print(f"Status: {health.get_status_code()}")

# List collections
collections = client.list_collections(0, 10)
if collections.is_success():
    body = collections.get_body()
    print(f"Found {len(body.get('collections', []))} collections")
```

### Example API Responses

Captured from a local `http://localhost:9200` server.

`client.health().get_body()`:

```json
{
  "server": "hlquery",
  "status": "ok",
  "version": "1.0"
}
```

`client.search_api().search('readme_demo', {'q': 'search', 'query_by': 'title,content', 'limit': 10}).get_body()`:

```json
{
  "hits": [
    {
      "document": {
        "id": "doc-2",
        "title": "Search Engineering Notes"
      },
      "highlights": {
        "title": "<em>Search</em> Engineering Notes"
      }
    }
  ],
  "found": 1
}
```

### With Authentication

```python
import os
# Method 1: Set token in constructor
client = Client(os.environ.get('HLQ_BASE_URL') or os.environ.get('HLQUERY_BASE_URL') or 'http://localhost:9200', {
    'token': 'your_token_here',
    'auth_method': 'bearer'  # or 'api-key'
})

# Method 2: Set token dynamically
client = Client(os.environ.get('HLQ_BASE_URL') or os.environ.get('HLQUERY_BASE_URL') or 'http://localhost:9200')
client.set_auth_token('your_token_here', 'bearer')

# Method 3: Use X-API-Key
client.set_auth_token('your_token_here', 'api-key')
```

### Reduce Text Example

You can use the raw request helper to call custom module routes directly:

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

### SAM Example

Use the SAM helper to search against generated SAM terms and inspect status/history:

```python
from lib import Client

client = Client('http://localhost:9200')
sam = client.sam()

status = sam.status('music')
print(status.get_body())

results = sam.search('music', 'queen of pop', {
    'limit': 5,
})
print(results.get_body())

history = sam.history('music', 5)
print(history.get_body())
```

### API Methods

#### `health()`
Check server health status.

```python
health = client.health()
if health.is_success():
    body = health.get_body()
    print(f"Status: {body.get('status')}")
```

#### `stats()`
Get server statistics.

```python
stats = client.stats()
```

#### `info()`
Get server information.

```python
info = client.info()
```

### Collections API

#### Using the Collections API Object

```python
collections = client.collections_api()

# List collections
result = collections.list(0, 10)

# Get collection
result = collections.get('my_collection')

# Create collection
result = collections.create('new_collection', schema)

# Delete collection
result = collections.delete('collection_name')

# Get formatted fields
result = collections.get_fields('my_collection')
```

#### Convenience Methods

```python
# List collections
collections = client.list_collections(0, 10)

# Get collection details
collection = client.get_collection('my_collection')

# Get collection fields (formatted)
fields = client.get_collection_fields('my_collection')
```

### SAM API

#### Using the SAM API Object

```python
sam = client.sam()

result = sam.search('music', 'queen of pop', {'limit': 10})
status = sam.status('music')
history = sam.history('music', 10)
```

#### Convenience Methods

```python
result = client.sam_search('music', 'queen of pop', {'limit': 10})
status = client.sam_status('music')
history = client.sam_history('music', 10)
```

### Documents API

#### Using the Documents API Object

```python
documents = client.documents_api()

# List documents
result = documents.list('collection', {'offset': 0, 'limit': 10})

# Get document
result = documents.get('collection', 'doc_id')

# Add document
result = documents.add('collection', document)

# Update document
result = documents.update('collection', 'doc_id', document)

# Delete document
result = documents.delete('collection', 'doc_id')

# Bulk import
result = documents.import_documents('collection', [doc1, doc2, doc3])

# Parse and add a local PDF file
result = documents.add_pdf('collection', './files/report.pdf')

# Parse and add a local CSV file
result = documents.add_csv('collection', './files/report.csv')
```

#### PDF Parsing

`documents.add_pdf(collection, file_path, options=None)` parses a local PDF file, normalizes the extracted text, and submits it as a regular document to hlquery.

```python
result = client.documents_api().add_pdf('reports', './files/q1-report.pdf', {
    'id': 'report_q1',
    'document': {
        'source_type': 'pdf'
    }
})
```

The generated document includes:
- `title`
- `content`
- `file_name`
- `file_path`
- `mime_type`
- `page_count`
- `file_size_bytes`
- normalized PDF metadata fields such as `pdf_meta_author`

Note: hlquery currently rejects commas in string field values. The PDF helper replaces commas with spaces before indexing so extracted text can be stored successfully.

#### CSV Parsing

`documents.add_csv(collection, file_path, options=None)` parses a local CSV file, flattens rows into normalized text, and submits it as a regular document to hlquery.

```python
result = client.documents_api().add_csv('reports', './files/metrics.csv', {
    'id': 'metrics_q1',
    'document': {
        'source_type': 'csv'
    }
})
```

The generated document includes:
- `title`
- `content`
- `file_name`
- `file_path`
- `mime_type`
- `row_count`
- `column_count`
- `columns`

CSV parsing uses the Python standard library only. Cells are flattened into plain text, and commas are replaced with spaces before indexing to satisfy hlquery field restrictions.

### Search API

#### Using the Search API Object

```python
search = client.search_api()

# Simple search
results = search.search('collection', {
    'q': 'search query',
    'query_by': 'title,content',
    'limit': 10
})

# Multi-search
results = search.multi_search([
    {'collection': 'col1', 'q': 'query1'},
    {'collection': 'col2', 'q': 'query2'}
])
```

#### Convenience Method

```python
# Search documents
results = client.search('collection', {
    'q': 'search query',
    'query_by': 'title,content',
    'limit': 10
})
```

### Ranking helpers

`hlquery.utils.ranker` exposes a reusable `compute_rank_signal` helper (for `rank_signal`, `popularity_score`, `hit_log`) plus `attach_rank_sort` so you can sort by the boosted field across all clients.

```python
from hlquery.utils import compute_rank_signal, attach_rank_sort

params = {'q': 'guide'}
signal = compute_rank_signal(popularity_score, hit_log)
params['rank_signal'] = signal
attach_rank_sort(params)  # ensures sort_by=rank_signal:desc
results = client.search('collection', params)
```

### Search Parameters

The `search()` method accepts flexible parameters:

#### Query Parameters
- `q` - Query string (supports field clauses, `OR`, `NOT`, phrases, and wildcards)
  - Examples: `q="title:laptop"`, `q="title:laptop OR title:notebook"`, `q="title:laptop NOT title:refurbished"`, `q="\"wireless keyboard\""`, `q="laptop*"`
- `query_by` - Fields to search in (string or list)
- `query` - Structured query object

#### Pagination
- `from` / `offset` - Starting offset
- `size` / `limit` - Number of results
- `page` - Page number (alternative to offset)
- `per_page` - Results per page

#### Filtering & Sorting
- `filter_by` - Filter conditions (string), for example `filter_by="price:>100&&category:electronics"`
- `filter` - Filter object
- `sort_by` - Sort fields (string or list)
- `sort` - Sort specification

#### Faceting
- `facet_by` - Facet fields (string or list)
- `facets` - Facet specification

### API Aliases

#### `indices(params=None)`
Alias for `list_collections()`.

```python
collections = client.indices({'offset': 0, 'limit': 10})
```

#### `get(params)`
Alias for `get_collection()` or `get_document()`.

```python
# Get document
doc = client.get({'index': 'collection', 'id': 'doc_id'})

# Get collection
collection = client.get({'index': 'collection'})
```

#### `cat(cat_type='indices', params=None)`
Cat API for listing collections and system information.

```python
indices = client.cat('indices', {'limit': 10})
```


## Requirements

- Python >= 3.6
- No external dependencies (uses built-in `urllib` and `json`)

## Installation

This package can be installed via pip:

```bash
pip install -e .
```

Or add to your `requirements.txt`:
