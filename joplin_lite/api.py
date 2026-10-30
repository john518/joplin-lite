"""Functions accessible to javascript via the pywebview Python-JS bridge."""

import json
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime
from typing import Any


class Api:
    """
    PyWebView bridge class exposed to the frontend UI to forward API requests
    to the local Joplin server.
    """
    def __init__(self, port: int, token: str) -> None:
        self.port = port
        self.token = token
        self.base_url = f"http://localhost:{port}"

    def ping(self) -> dict:
        """Health check pywebview endpoint to verify backend is responsive."""
        # print("Enter ping()")
        return {
            "status": "ok",
            "timestamp": datetime.now().isoformat()
        }

    def request(
        self,
        method: str,
        endpoint: str,
        data: dict[str, Any] | list[Any] | None = None,
        params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """
        Generic request forwarder callable from JavaScript via pywebview.api.request(...)
        """
        # Ensure endpoint starts with a slash
        if not endpoint.startswith("/"):
            endpoint = f"/{endpoint}"

        url = f"{self.base_url}{endpoint}"

        # Joplin API uses the 'token' query parameter for authentication
        query_params = {"token": self.token}
        if params:
            query_params.update(params)

        url = f"{url}?{urllib.parse.urlencode(query_params)}"

        headers = {"Content-Type": "application/json"}
        body = json.dumps(data).encode("utf-8") if data is not None else None

        req = urllib.request.Request(url, data=body, headers=headers, method=method.upper())

        try:
            with urllib.request.urlopen(req, timeout=10.0) as response:
                res_body = response.read().decode("utf-8")
                try:
                    parsed_data = json.loads(res_body)
                except json.JSONDecodeError:
                    parsed_data = res_body

                return {
                    "success": True,
                    "status": response.status,
                    "data": parsed_data
                }

        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            try:
                err_data = json.loads(err_body)
            except json.JSONDecodeError:
                err_data = err_body

            return {
                "success": False,
                "status": e.code,
                "error": err_data
            }

        except Exception as e:
            return {
                "success": False,
                "status": 500,
                "error": str(e)
            }
