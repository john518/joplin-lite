"""Functions accessible to javascript via the pywebview Python-JS bridge."""

import json
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime
from enum import Enum
from typing import Any

from joplin_lite.utils import build_notebook_tree


class HttpMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


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
        method: HttpMethod,
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

    def get_notebooks(self) -> list[dict]:
        """Fetches all notebooks from the Joplin API and formats them as a flattened list.

        Returns:
            list of dict: A flattened list of notebook dictionaries sorted hierarchically and
            alphanumerically, with an added 'depth' integer field indicating the nesting level.
        """
        notebooks = self._fetch_all_notebooks()

        # Skip notebooks that are in Trash folder
        active_notebooks = [nb for nb in notebooks if nb.get("deleted_time", 0) == 0]

        # Generate the flattened list
        flattened = build_notebook_tree(active_notebooks)  # need to worry about empty case?
        print("FLATTENED:")
        print(flattened)
        return flattened

    def _fetch_all_notebooks(self) -> list[dict]:
        """Fetches all notebooks from the Joplin API, handling pagination."""
        page = 1
        limit = 50
        all_notebooks = []

        while True:
            params = {
                "limit": limit,
                "page": page
            }
            response = self.request(HttpMethod.GET, "folders", params)
            error = response.get("error")
            if error is not None:
                raise RuntimeError(error)

            data = response.get("data")
            if not data:
                break

            items = data.get("items", response)
            if not items:
                break

            all_notebooks.extend(items)

            # Check if there are more pages
            has_more = response.get("has_more", False)
            if not has_more or len(items) < limit:
                break

            page += 1

        return all_notebooks
