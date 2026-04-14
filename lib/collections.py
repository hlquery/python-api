import urllib.parse


class Collections:
    def __init__(self, request):
        self._request = request

    def list(self, offset=0, limit=10):
        return self._request.execute("GET", "/collections", query_params={"offset": offset, "limit": limit})

    def get(self, name):
        return self._request.execute("GET", f"/collections/{urllib.parse.quote(name, safe='')}")

    def get_fields(self, name):
        return self._request.execute("GET", f"/collections/{urllib.parse.quote(name, safe='')}/fields")

    def create(self, name, schema):
        payload = dict(schema or {})
        payload["name"] = name
        return self._request.execute("POST", "/collections", payload=payload)

    def update(self, name, schema):
        return self._request.execute("POST", f"/collections/{urllib.parse.quote(name, safe='')}/update", payload=schema or {})

    def delete(self, name):
        return self._request.execute("DELETE", f"/collections/{urllib.parse.quote(name, safe='')}")
