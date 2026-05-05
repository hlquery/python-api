"""
hlquery Python Client - Response wrapper
"""


class Response:
    """HTTP response wrapper with helper methods."""

    def __init__(self, status_code, headers=None, body=None, raw_body="", error=""):
        self._status_code = int(status_code or 0)
        self._headers = headers or {}
        self._body = body
        self._raw_body = raw_body if isinstance(raw_body, str) else ""
        self._error = error if isinstance(error, str) else ""

    def is_success(self):
        return 200 <= self._status_code < 300

    def is_error(self):
        return self._status_code >= 400 or self._status_code == 0

    def get_status_code(self):
        return self._status_code

    def get_headers(self):
        return self._headers

    def get_body(self):
        return self._body

    def get_raw_body(self):
        return self._raw_body

    def get_error(self):
        return self._error

    def get_message(self):
        if self._error:
            return self._error

        if isinstance(self._body, dict):
            if isinstance(self._body.get("message"), str):
                return self._body["message"]
            if isinstance(self._body.get("error"), str):
                return self._body["error"]

        return ""
