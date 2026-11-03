"""Functions accessible to javascript via the pywebview Python-JS bridge."""

import json
import urllib.request
import urllib.error
import urllib.parse
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

from joplin_lite.utils import build_notebook_tree


STATE_FILE = Path.home() / ".config" / "joplin-lite" / "state.json"


class HttpMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


@dataclass
class ResponseObject:
    success: bool
    status: int
    data: dict = field(default_factory=dict)
    err_data: dict | str | None = None


@dataclass
class NotesObject:
    """Data returned by get_notes()"""
    success: bool
    items: list[dict]
    has_more: bool
    error_data: dict | str | None = None


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
    ) -> ResponseObject:
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

                return ResponseObject(success=True, status=response.status, data=parsed_data)

        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            try:
                err_data = json.loads(err_body)
            except json.JSONDecodeError:
                err_data = err_body

            return ResponseObject(success=False, status=e.code, data=None, err_data=err_data)

        except Exception as e:
            return ResponseObject(success=False, status=500, data=None, err_data=str(e))

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
        # print("FLATTENED:")
        # print(flattened)
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
            err_data = response.err_data
            if err_data is not None:
                raise RuntimeError(err_data)

            if not response.data:
                break

            if not response.data:
                break

            items = response.data.get("items", [])
            if not items:
                break

            all_notebooks.extend(items)

            # Check if there are more pages
            has_more = response.data.get("has_more", False)
            if not has_more or len(items) < limit:
                break

            page += 1

        return all_notebooks

    def get_notes(self, notebook_id: str, page: int = 1, limit: int = 50) -> NotesObject:
        """Fetches notes from the Joplin API for specified notebook.

        Note that `notebook_id` 0 represents all notes
        """
        endpoint = "notes" if notebook_id == 0 else f"folders/{notebook_id}/notes"
        params = {
            "limit": limit,
            "page": page,
            "include_conflicts": 1,
            "order_by": "updated_time",
            "order_dir": "desc",
        }

        response = self.request(HttpMethod.GET, endpoint, params)

        if response.err_data:
            return NotesObject(
                success=False, items=[], has_more=False, error_data=response.err_data)

        # (else)
        data = response.data
        return NotesObject(
            success=True, items=data.get("items", []), has_more=data.get("has_more", False))

    def get_user_state(self):
        """Retrieves the full user state dictionary from disk."""
        if STATE_FILE.exists():
            try:
                with open(STATE_FILE, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def get_user_state_value(self, key):
        """Retrieves a specific value from the saved user state."""
        state = self.get_user_state()
        return {"success": True, "value": state.get(key)}

    def save_user_state_value(self, key, value):
        """Saves a single key-value preference to the state file."""
        try:
            STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
            state = self.get_user_state()
            state[key] = value

            with open(STATE_FILE, "w") as f:
                json.dump(state, f, indent=2)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
