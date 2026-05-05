"""
hlquery Python Client - HTTP transport
"""

import json
import urllib.error
import urllib.parse
import urllib.request

from .response import Response
from utils.auth import Auth


class Request:
    """HTTP request helper built on urllib."""

    def __init__(self, base_url, timeout=30, token=None, auth_method="bearer"):
        self._base_url = str(base_url).rstrip("/")
        self._timeout = int(timeout) if timeout else 30
        self._token = token
        self._auth_method = auth_method or "bearer"

    def set_auth_token(self, token, auth_method="bearer"):
        self._token = token
        self._auth_method = auth_method or "bearer"

    def clear_auth(self):
        self._token = None

    def execute(self, method, path, body=None, query_params=None):
        url = self._build_url(path, query_params or {})
        payload = None
        headers = {
            "Accept": "application/json",
        }

        if self._token:
            auth_header = Auth.get_auth_header(self._token, self._auth_method)
            headers[auth_header["header"]] = auth_header["value"]

        if body is not None:
            payload = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"

        request = urllib.request.Request(url, data=payload, method=str(method).upper(), headers=headers)

        try:
            with urllib.request.urlopen(request, timeout=self._timeout) as handle:
                raw_body = handle.read().decode("utf-8")
                body_value = self._decode_body(raw_body)
                response_headers = dict(handle.headers.items())
                return Response(handle.getcode(), response_headers, body_value, raw_body, "")
        except urllib.error.HTTPError as error:
            raw_body = error.read().decode("utf-8") if error.fp else ""
            body_value = self._decode_body(raw_body)
            return Response(error.code, dict(error.headers.items()), body_value, raw_body, str(error))
        except urllib.error.URLError as error:
            return Response(0, {}, None, "", str(error.reason))

    def _build_url(self, path, query_params):
        normalized_path = "/" + str(path).lstrip("/")
        url = self._base_url + normalized_path

        if query_params:
            encoded = urllib.parse.urlencode(query_params, doseq=True)
            if encoded:
                url += "?" + encoded

        return url

    @staticmethod
    def _decode_body(raw_body):
        if not raw_body:
            return {}

        try:
            return json.loads(raw_body)
        except Exception:
            return raw_body
