# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests",
#     "python-dotenv",
# ]
# ///

"""Diagnostic script to test connection to the local Joplin Data/API server.

This script queries the local Joplin Data API endpoint (/folders) to verify
that authentication and network communication are working correctly.

Usage:
    uv run test_joplin_connection.py
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables from a local .env file if present
load_dotenv()

BASE_URL = os.getenv("JOPLIN_API_URL")
TOKEN = os.getenv("JOPLIN_API_TOKEN")


def test_joplin_connection():
    """Fetches and displays top-level notebooks from the local Joplin API."""
    url = f"{BASE_URL}/folders"
    params = {"token": TOKEN}

    print(f"Connecting to Joplin API at {BASE_URL}...")

    try:
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
                "token": TOKEN,
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
            "token": TOKEN,
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
