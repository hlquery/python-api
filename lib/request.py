import json
import urllib.error
import urllib.parse
import urllib.request

from .response import Response


class Request:
    def __init__(self, base_url, options=None):
        options = options or {}
        self.base_url = (base_url or "http://localhost:9200").rstrip("/")
        self.auth_token = options.get("token")
        self.auth_method = options.get("auth_method", "bearer")
        self.timeout = options.get("timeout", 30)

    def set_auth_token(self, token, method="bearer"):
        self.auth_token = token
        self.auth_method = method or "bearer"

    def execute(self, method, path, payload=None, query_params=None, headers=None):
        url = self.base_url + path
        query = self._build_query_string(query_params)
        if query:
            url = f"{url}?{query}"

        request_headers = {"Accept": "application/json"}
        if headers:
            request_headers.update(headers)

        if self.auth_token:
            if self.auth_method == "api-key":
                request_headers["X-API-Key"] = self.auth_token
            else:
                request_headers["Authorization"] = f"Bearer {self.auth_token}"

        data = None
        if payload is not None:
            request_headers["Content-Type"] = "application/json"
            if isinstance(payload, (dict, list)):
                data = json.dumps(payload).encode("utf-8")
            elif isinstance(payload, str):
                data = payload.encode("utf-8")
            else:
                data = json.dumps(payload).encode("utf-8")

        req = urllib.request.Request(url, data=data, method=method.upper(), headers=request_headers)

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                raw = resp.read().decode("utf-8")
                body = self._decode_body(raw, resp.headers.get("Content-Type"))
                return Response(
                    status_code=resp.status,
                    body=body,
                    raw_body=raw,
                    headers=dict(resp.headers.items()),
                )
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode("utf-8")
            body = self._decode_body(raw, exc.headers.get("Content-Type") if exc.headers else None)
            error = None
            if isinstance(body, dict):
                error = body.get("message") or body.get("error")
            error = error or str(exc)
            return Response(
                status_code=exc.code,
                body=body,
                raw_body=raw,
                headers=dict(exc.headers.items()) if exc.headers else {},
                error=error,
            )
        except Exception as exc:
            return Response(status_code=0, body=None, raw_body="", headers={}, error=str(exc))

    def _decode_body(self, raw_body, content_type):
        if not raw_body:
            return None

        if (content_type and "application/json" in content_type.lower()) or raw_body[:1] in ("{", "["):
            try:
                return json.loads(raw_body)
            except Exception:
                return raw_body
        return raw_body

    def _build_query_string(self, query_params):
        if not query_params:
            return ""

        normalized = {}
        for key, value in query_params.items():
            if value is None:
                continue
            if isinstance(value, bool):
                normalized[key] = "true" if value else "false"
            elif isinstance(value, (dict, list)):
                normalized[key] = json.dumps(value)
            else:
                normalized[key] = str(value)
        return urllib.parse.urlencode(normalized)
