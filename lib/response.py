class Response:
    def __init__(self, status_code=0, body=None, raw_body="", headers=None, error=None):
        self._status_code = status_code
        self._body = body
        self._raw_body = raw_body
        self._headers = headers or {}
        self._error = error

    def get_status_code(self):
        return self._status_code

    def get_body(self):
        return self._body

    def get_raw_body(self):
        return self._raw_body

    def get_headers(self):
        return self._headers

    def get_error(self):
        return self._error

    def is_success(self):
        return 200 <= self._status_code < 300

    def is_error(self):
        return not self.is_success()

    def to_dict(self):
        return {
            "status_code": self._status_code,
            "body": self._body,
            "raw_body": self._raw_body,
            "headers": self._headers,
            "error": self._error,
        }
