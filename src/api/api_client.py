"""Reusable API client for HTTP operations."""

from __future__ import annotations

import logging
from typing import Any

import requests

LOGGER = logging.getLogger(__name__)


class APIClient:
    """Thin wrapper around requests.Session with common behavior."""

    def __init__(self, base_url: str, timeout_seconds: int = 15) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json; charset=UTF-8"})

    def close(self) -> None:
        self.session.close()

    def get(self, path: str, **kwargs: Any) -> requests.Response:
        return self._request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> requests.Response:
        return self._request("POST", path, **kwargs)

    def put(self, path: str, **kwargs: Any) -> requests.Response:
        return self._request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> requests.Response:
        return self._request("DELETE", path, **kwargs)

    def _request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        url = f"{self.base_url}/{path.lstrip('/')}"
        LOGGER.info("API request | method=%s | url=%s", method, url)
        response = self.session.request(method=method, url=url, timeout=self.timeout_seconds, **kwargs)
        LOGGER.info("API response | method=%s | status_code=%s", method, response.status_code)
        return response
