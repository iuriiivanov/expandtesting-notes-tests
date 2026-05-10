"""HTTP client for API requests."""

from typing import Any

import requests


class ApiClient:
    """HTTP client for Notes API."""

    def __init__(self, token: str | None = None) -> None:
        self.session = requests.Session()
        self.token = token
        self._set_headers()

    def _set_headers(self) -> None:
        """Set default headers for requests."""
        self.session.headers.update(
            {"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}
        )
        if self.token:
            self.session.headers.update({"x-auth-token": self.token})

    def set_token(self, token: str) -> None:
        """Set authentication token."""
        self.token = token
        self.session.headers.update({"x-auth-token": token})

    def clear_token(self) -> None:
        """Clear authentication token."""
        self.token = None
        self.session.headers.pop("x-auth-token", None)

    def get(
        self,
        url: str,
        *,
        timeout: float | tuple[float, float] | None = None,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
    ) -> requests.Response:
        """Send GET request."""
        kwargs: dict[str, Any] = {}
        if timeout is not None:
            kwargs["timeout"] = timeout
        if headers is not None:
            kwargs["headers"] = headers
        if params is not None:
            kwargs["params"] = params
        return self.session.get(url, **kwargs)

    def post(
        self,
        url: str,
        data: dict[str, Any] | None = None,
        *,
        timeout: float | tuple[float, float] | None = None,
        headers: dict[str, str] | None = None,
    ) -> requests.Response:
        """Send POST request."""
        kwargs: dict[str, Any] = {}
        if timeout is not None:
            kwargs["timeout"] = timeout
        if headers is not None:
            kwargs["headers"] = headers
        if data is not None:
            kwargs["data"] = data
        return self.session.post(url, **kwargs)

    def put(
        self,
        url: str,
        data: dict[str, Any] | None = None,
        *,
        timeout: float | tuple[float, float] | None = None,
        headers: dict[str, str] | None = None,
    ) -> requests.Response:
        """Send PUT request."""
        kwargs: dict[str, Any] = {}
        if timeout is not None:
            kwargs["timeout"] = timeout
        if headers is not None:
            kwargs["headers"] = headers
        if data is not None:
            kwargs["data"] = data
        return self.session.put(url, **kwargs)

    def patch(
        self,
        url: str,
        data: dict[str, Any] | None = None,
        *,
        timeout: float | tuple[float, float] | None = None,
        headers: dict[str, str] | None = None,
    ) -> requests.Response:
        """Send PATCH request."""
        kwargs: dict[str, Any] = {}
        if timeout is not None:
            kwargs["timeout"] = timeout
        if headers is not None:
            kwargs["headers"] = headers
        if data is not None:
            kwargs["data"] = data
        return self.session.patch(url, **kwargs)

    def delete(
        self,
        url: str,
        *,
        timeout: float | tuple[float, float] | None = None,
        headers: dict[str, str] | None = None,
    ) -> requests.Response:
        """Send DELETE request."""
        kwargs: dict[str, Any] = {}
        if timeout is not None:
            kwargs["timeout"] = timeout
        if headers is not None:
            kwargs["headers"] = headers
        return self.session.delete(url, **kwargs)
