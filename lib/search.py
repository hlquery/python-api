import urllib.parse


class Search:
    def __init__(self, request):
        self._request = request

    def search(self, collection, params=None):
        return self._request.execute(
            "GET",
            f"/collections/{urllib.parse.quote(collection, safe='')}/documents/search",
            query_params=params or {},
        )

    def vector_search(self, collection, params=None):
        params = params or {}
        body = params.get("body", params)
        return self._request.execute(
            "POST",
            f"/collections/{urllib.parse.quote(collection, safe='')}/search",
            payload=body,
        )

    def multi_search(self, searches):
        return self._request.execute("POST", "/multi_search", payload={"searches": searches or []})
