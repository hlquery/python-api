<div align="center">
  <img src="https://docs.hlquery.com/img/hlquery/2.png" alt="hlquery logo" width="200">
</div>

<div align="center">

**A modular Python client library for hlquery, designed with a familiar and intuitive API structure.**

[![Twitter Follow](https://img.shields.io/twitter/url/https/x.com/hlquery.svg?style=social&label=Follow%20%40hlquery)](https://x.com/hlquery)
[![Linux Build](https://github.com/hlquery/python-api/workflows/Linux%20build/badge.svg)](https://github.com/hlquery/python-api/actions)
[![macOS Build](https://github.com/hlquery/python-api/workflows/macOS%20Build/badge.svg)](https://github.com/hlquery/python-api/actions)
[![Commit Activity](https://img.shields.io/github/commit-activity/m/hlquery/python-api)](https://github.com/hlquery/python-api/pulse)
[![GitHub stars](https://img.shields.io/github/stars/hlquery/python-api?style=social)](https://github.com/hlquery/python-api/stargazers)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

[Documentation](https://docs.hlquery.com) • [hlquery](https://github.com/hlquery/hlquery) • [Discord](https://discord.hlquery.com)

</div>


## Features

-  **Modular Architecture**: Clean separation of concerns with organized classes
-  **Intuitive API**: Familiar and easy-to-use structure
-  **Authentication Support**: Bearer token and X-API-Key authentication
-  **Flexible Parameters**: Support for multiple parameter formats
-  **Auto-detection**: Automatically detects searchable fields when not specified
-  **Type-safe Responses**: Response objects with helper methods
-  **Comprehensive Validation**: Input validation for all operations
-  **No External Dependencies**: Uses Python's built-in `urllib` and `json` modules
-  **Professional Structure**: Well-organized and modular architecture

## Installation

Core client usage has no dependencies beyond Python's standard library. PDF parsing uses the optional `PyPDF2` package.

Simply import the client:

```python
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
client = Client('http://localhost:9200')

# Health check
health = client.health()
print(f"Status: {health.get_status_code()}")

# List collections
collections = client.list_collections(0, 10)
if collections.is_success():
    body = collections.get_body()
    print(f"Found {len(body.get('collections', []))} collections")
```

### With Authentication

```python
# Method 1: Set token in constructor
client = Client('http://localhost:9200', {
    'token': 'your_token_here',
    'auth_method': 'bearer'  # or 'api-key'
})

# Method 2: Set token dynamically
client = Client('http://localhost:9200')
client.set_auth_token('your_token_here', 'bearer')

# Method 3: Use X-API-Key
client.set_auth_token('your_token_here', 'api-key')
```

### Reduce Text Example

If the `ai_search` module is enabled, you can use the raw request helper to ask hlquery to summarize a stored document:

```python
summary = client.execute_request(
    "GET",
    "/modules/ai_search/talk",
    query_params={
        "q": "summarize onboarding guide in docs",
        "run": "true",
    },
)

print(summary.get_body())
```

## Architecture

### Core Classes

#### `Client`
Main client class that provides access to all API operations.

#### `Request`
Handles HTTP requests, authentication, and error handling.

#### `Response`
Response wrapper with helper methods:
- `get_status_code()` - Get HTTP status code
- `get_body()` - Get response body
- `is_success()` - Check if request was successful
- `is_error()` - Check if request failed
- `get_error()` - Get error message
- `to_dict()` - Convert to dictionary format (for backward compatibility)

#### API Classes

`Collections` manages collections.
`Documents` handles document CRUD and import.
`Search` handles search requests and flexible parameter input.

### Utilities

`Auth` provides token helpers and validation.
`Config` handles defaults and URL/config normalization.
`Validator` validates request input before it is sent.

### Exceptions

`HlqueryException` is the base type.
Use `AuthenticationException`, `RequestException`, `ValidationException`, `CollectionException`, `DocumentException`, and `SearchException` for specific failures.

## API Methods

### System APIs

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

#### Field Value Character Restrictions

**Important**: String field values have character restrictions:

**❌ Invalid Characters** (not allowed):
- Commas (`,`) - Reserved for internal parsing

** Valid Characters** (allowed):
- Letters, numbers, underscores (`_`), hyphens (`-`), spaces, periods, and most punctuation (except commas)

**Examples:**

 **Valid:**
```python
doc = {
    'id': 'doc1',
    'tags': 'tag1_tag2_tag3',        #  Use underscores
    'cast': 'Actor1_Actor2',          #  Use underscores
    'genre': 'Action_Drama'            #  Use underscores
}

# Or use arrays for multiple values:
doc2 = {
    'id': 'doc2',
    'tags': ['tag1', 'tag2', 'tag3']  #  Arrays are fine
}
```

❌ **Invalid:**
```python
doc = {
    'id': 'doc1',
    'tags': 'tag1,tag2,tag3',         # ❌ Commas not allowed
    'cast': 'Actor1, Actor2',         # ❌ Commas not allowed
    'genre': 'Action,Drama'           # ❌ Commas not allowed
}
```

**Workarounds:**
- Use underscores (`_`) or spaces instead of commas
- Use arrays for multiple values: `tags: ['tag1', 'tag2', 'tag3']`
- Use separate fields if you need comma-separated data

#### Convenience Methods

```python
# List documents
docs = client.list_documents('collection', {'offset': 0, 'limit': 10})

# Get document
doc = client.get_document('collection', 'doc_id')
```

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

## Response Handling

All methods return a `Response` object:

```python
response = client.health()

# Check status
if response.is_success():
    # Handle success
    body = response.get_body()

# Or check status code
if response.get_status_code() == 200:
    # Handle success

# Get error
if response.is_error():
    error = response.get_error()
    print(f"Error: {error}")

# Convert to dictionary (for backward compatibility)
result_dict = response.to_dict()
# Returns: {'status': 200, 'body': {...}}
```

## Error Handling

The client throws exceptions for errors:

```python
from lib import Client
from lib.exceptions import RequestException, AuthenticationException, ValidationException

try:
    result = client.search('collection', {'q': 'test'})
    
    if result.is_error():
        # Handle HTTP error
        print(f"Error: {result.get_error()}")
except RequestException as e:
    # Handle request errors
    print(f"Request failed: {e}")
    print(f"Status: {e.status_code}")
except AuthenticationException as e:
    # Handle authentication errors
    print(f"Auth failed: {e}")
except ValidationException as e:
    # Handle validation errors
    print(f"Validation failed: {e}")
except Exception as e:
    # Handle other errors
    print(f"Error: {e}")
```

## Examples

### Complete Example

See `example.py` for a complete example demonstrating:
- Health checks
- Authentication (with and without token)
- Listing collections
- Getting collection fields
- Listing documents with pagination
- Multiple search methods
- Dynamic authentication

Run the example:

```bash
# Without authentication
python example.py

# With authentication
python example.py your_token_here
```

### Organized Examples

Check the `examples/` directory for organized examples:
- `basic_usage.py` - Basic operations
- `search.py` - Search patterns
- `collections.py` - Collection management
- `documents.py` - Document CRUD


## Requirements

- Python >= 3.6
- No external dependencies (uses built-in `urllib` and `json`)

## Installation

This package can be installed via pip:

```bash
pip install -e .
```

Or add to your `requirements.txt`:

```
# No external dependencies required
```

## Architecture

For detailed information about the library architecture, design decisions, and internal structure, see [STRUCTURE.md](STRUCTURE.md).
