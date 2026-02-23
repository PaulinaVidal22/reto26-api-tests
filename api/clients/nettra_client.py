import httpx
from typing import Optional


class NettraClient:
    def __init__(self, base_url: str, token: Optional[str] = None):
        headers = {}

        if token:
            headers["Authorization"] = f"Bearer {token}"

        self.client = httpx.Client(
            base_url=base_url,
            headers=headers,
            timeout=10.0
        )

    def get(self, endpoint: str, params: dict | None = None):
        return self.client.get(endpoint, params=params)

    def post(self, endpoint: str, data: dict):
        return self.client.post(endpoint, json=data)

    def put(self, endpoint: str, data: dict):
        return self.client.put(endpoint, json=data)

    def delete(self, endpoint: str):
        return self.client.delete(endpoint)

    def close(self):
        self.client.close()