# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests",
# ]
# ///

"""Diagnostic script to test connection to the local Joplin Data/API server.

This script queries the local Joplin Data API endpoint (/folders) to verify
that authentication and network communication are working correctly.

Usage:
    uv run test_joplin_connection.py
"""

import json
import sys
import requests
from pathlib import Path

CONFIG_FILE = ".config/joplin-lite/settings.json"


def test_joplin_connection():
    """Fetches and displays top-level notebooks from the local Joplin API."""
    # Read server settings file
    config_path = Path.home() / CONFIG_FILE
    if not config_path.exists():
        print(f"\nFAILED: Missing config file {config_path}.")
        sys.exit(1)

    config_dict = None
    with open(config_path, "r", encoding="utf-8") as fp:
        config_dict = json.load(fp)

    api_port = config_dict.get("api.port", 41183)
    api_token = config_dict.get("api.token")

    BASE_URL = f"http://localhost:{api_port}"

    params = {"token": api_token}

    print(f"Connecting to Joplin API at {BASE_URL}...")

    try:
        # ping endpoint is documented (https://joplinapp.org/help/api/references/rest_api)
        # but does not work ("Error details: Expecting value: line 1 column 1 (char 0)")
        #
        # url = f"{BASE_URL}/ping"
        # response = requests.get(url, timeout=5)
        # response.raise_for_status()
        # data = response.json()
        # print("Server response (data):")
        # print(data)

        url = f"{BASE_URL}/folders"
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        print("Server response (data):")
        print(data)

        folders = data.get("items", [])
        print(f"\nSUCCESS: Successfully connected to Joplin server!")
        print(f"Found {len(folders)} total folder(s) in database.\n")

        print("Top-level Notebooks:")
        print("-" * 40)

        main_folder_id = None
        top_level_count = 0
        for folder in folders:
            if folder.get("title") == "Main":
                main_folder_id = folder.get("id")

            # Top-level notebooks typically have an empty or null parent_id
            if not folder.get("parent_id"):
                top_level_count += 1
                print(f"  - {folder.get('title')} (ID: {folder.get('id')})")

        if top_level_count == 0:
            print("  (No top-level notebooks found or all notebooks are nested)")

        # Get notes for a folder
        if main_folder_id is not None:
            url = f"{BASE_URL}/folders/{main_folder_id}/notes"
            limit = 5
            params = {
                "token": api_token,
                "order_by": "updated_time",
                "order_dir": "desc",
                "limit": limit,
            }

            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()

            print(f"\nLast {limit} notes in Main Notebook:")
            print("-" * 40)
            print(data)

        # Get notes from search query
        url = f"{BASE_URL}/search"
        query = "Joplin"
        limit = 10
        params = {
            "token": api_token,
            "query": query,
            "fields": "id,title,created_time,parent_id",
            "order_by": "updated_time",
            "order_dir": "desc",
            "limit": limit,
        }

        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        print(f"\nSearch result for {query}")
        print("-" * 40)
        print(data)


    except requests.exceptions.RequestException as e:
        print(f"\nFAILED: Could not connect to Joplin API.")
        print(f"Error details: {e}")
        sys.exit(1)


if __name__ == "__main__":
    test_joplin_connection()
