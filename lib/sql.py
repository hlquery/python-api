"""
hlquery Python Client - SQL API
"""

from .service import Service


class SQL(Service):
    """SQL API helper."""

    def query(self, sql, query_params=None):
        params = dict(query_params or {})
        params["sql"] = str(sql)
        return self.client.execute_request("GET", "/sql", query_params=params)

    def exec(self, sql):
        return self.client.execute_request("POST", "/sql", body={"exec": str(sql)})

    def search(self, collection_name, sql, params=None):
        return self.client.search_api().sql(collection_name, sql, params or {})
