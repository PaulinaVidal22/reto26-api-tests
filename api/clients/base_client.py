import httpx
from typing import Optional, Dict, Any


class BaseClient:
    def __init__(self, base_url: str, token: Optional[str] = None):
        self.base_url = base_url
        self._token = token

        # Cliente SIN headers por defecto
        self.client = httpx.Client(
            base_url=self.base_url,
            timeout=10.0
        )

    def _build_headers(
        self,
        headers_override: Optional[Dict[str, Optional[str]]] = None
    ) -> Dict[str, str]:
        headers: Dict[str, str] = {}

        # Agregar Authorization si hay token
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"

        # Aplicar overrides
        if headers_override:
            for key, value in headers_override.items():
                if value is None:
                    headers.pop(key, None)
                else:
                    headers[key] = value

        return headers

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers_override: Optional[Dict[str, Optional[str]]] = None,
    ):
        headers = self._build_headers(headers_override)

        return self.client.request(
            method=method,
            url=endpoint,
            params=params,
            json=json,
            headers=headers,
        )

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers_override: Optional[Dict[str, Optional[str]]] = None,
    ):
        return self._request("GET", endpoint, params=params, headers_override=headers_override)

    def post(self, endpoint: str, data: Dict[str, Any]):
        return self._request("POST", endpoint, json=data)

    def put(self, endpoint: str, data: Dict[str, Any]):
        return self._request("PUT", endpoint, json=data)

    def delete(self, endpoint: str):
        return self._request("DELETE", endpoint)

    def close(self):
        self.client.close()