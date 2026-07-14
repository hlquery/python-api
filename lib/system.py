"""
hlquery Python Client - System API
"""

from .service import Service


class System(Service):
    """System and operational API helper."""

    def health(self):
        return self.client.execute_request("GET", "/health")

    def status(self):
        return self.client.execute_request("GET", "/status")

    def startup(self):
        return self.client.execute_request("GET", "/startup")

    def boot_status(self):
        return self.client.execute_request("GET", "/boot-status")

    def ready(self):
        return self.client.execute_request("GET", "/ready")

    def info(self):
        return self.client.execute_request("GET", "/")

    def query(self):
        return self.client.execute_request("GET", "/query")

    def stats(self):
        return self.client.execute_request("GET", "/stats")

    def metrics(self):
        return self.client.execute_request("GET", "/metrics")

    def metrics_json(self):
        return self.client.execute_request("GET", "/metrics.json")

    def metrics_history(self):
        return self.client.execute_request("GET", "/metrics/history")

    def metrics_history_alias(self):
        return self.client.execute_request("GET", "/metrics-history")

    def cache(self):
        return self.client.execute_request("GET", "/cache")

    def connections(self):
        return self.client.execute_request("GET", "/connections")

    def rocksdb(self):
        return self.client.execute_request("GET", "/rocksdb")

    def rocksdb_internal(self):
        return self.client.execute_request("GET", "/_rocksdb")

    def doc_total(self):
        return self.client.execute_request("GET", "/doctotal")

    def etc(self):
        return self.client.execute_request("GET", "/etc")

    def ping(self):
        return self.client.execute_request("GET", "/ping")

    def integrity(self):
        return self.client.execute_request("GET", "/integrity")

    def consistency(self):
        return self.client.execute_request("GET", "/consistency")

    def self_check(self):
        return self.client.execute_request("GET", "/self-check")

    def storage_status(self):
        return self.client.execute_request("GET", "/admin/storage_status")

    def search_config(self):
        return self.client.execute_request("GET", "/search-config")

    def config_files(self):
        return self.client.execute_request("GET", "/config-files")

    def update_counters(self, params=None, method="POST"):
        method = self._get_or_post(method, "Update counters")
        if method == "POST":
            return self.client.execute_request(method, "/update-counters", body=params or {})
        return self.client.execute_request(method, "/update-counters", query_params=params or {})

    def debug_counters(self):
        return self.client.execute_request("GET", "/debug/counters")

    def repair(self, params=None, method="POST"):
        method = self._get_or_post(method, "Repair")
        if method == "POST":
            return self.client.execute_request(method, "/repair", body=params or {})
        return self.client.execute_request(method, "/repair", query_params=params or {})

    def flush(self):
        return self.client.execute_request("POST", "/flush")

    @staticmethod
    def _get_or_post(method, operation):
        method = str(method).upper()
        if method not in ("GET", "POST"):
            raise ValueError(f"{operation} method must be GET or POST")
        return method
