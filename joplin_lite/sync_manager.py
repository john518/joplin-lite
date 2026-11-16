"""
Background synchronization manager for Joplin Lite.

This module handles asynchronous execution of the Joplin CLI sync command
using background daemon threads and tracks the live status and any error outputs
for safe consumption by the pywebview frontend.
"""

import logging
import subprocess
import threading

from . import JOPLIN_PROFILE_PATH

logger = logging.getLogger(__name__)


class SyncManager:
    """Manages background synchronization processes via the Joplin CLI."""

    def __init__(self) -> None:
        self._sync_in_progress = False
        self._sync_thread = None
        self._last_sync_error = None

    def trigger_sync(self) -> dict:
        """Triggers a background synchronization process using the Joplin CLI.

        Ensures that only one sync process runs at a time to prevent race conditions
        or database corruption. Spawns a daemon thread to keep the pywebview bridge
        responsive.

        Returns:
            dict: A response dictionary indicating success or failure to start.
        """
        if self._sync_in_progress:
            return {"success": False, "error_data": "Sync is already in progress."}

        self._sync_in_progress = True
        self._last_sync_error = None

        def run_sync():
            try:
                result = subprocess.run(
                    ["joplin", "--profile", str(JOPLIN_PROFILE_PATH), "sync"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                logger.info(f"Sync completed successfully: {result.stdout}")
            except subprocess.CalledProcessError as e:
                self._last_sync_error = e.stderr or e.stdout or str(e)
                logger.error(f"Sync failed: {self._last_sync_error}")
            except Exception as e:
                self._last_sync_error = str(e)
                logger.error(f"Sync exception: {self._last_sync_error}")
            finally:
                self._sync_in_progress = False

        self._sync_thread = threading.Thread(target=run_sync, daemon=True)
        self._sync_thread.start()

        return {"success": True, "data": {"message": "Sync started successfully"}}

    def get_status(self) -> dict:
        """Returns whether a sync is currently active and any recorded errors.

        Returns:
            dict: A response dictionary containing 'is_syncing' boolean and any 'error' string.
        """
        return {
            "success": True,
            "data": {
                "is_syncing": self._sync_in_progress,
                "error": self._last_sync_error
            }
        }
