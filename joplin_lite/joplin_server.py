#!/usr/bin/env python3
"""
joplin_server.py - Utility module to manage the local Joplin server instance,
parse its config (api.port, api.token), and ensure it is online before UI startup.
"""

import atexit
import json
import logging
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from . import JOPLIN_PROFILE_PATH


# Keep track of the process internally within the module
_active_process: subprocess.Popen | None = None

logger = logging.getLogger(__name__)

# Default paths and settings
JOPLIN_SETTINGS_FILEPATH = JOPLIN_PROFILE_PATH / "settings.json"
DEFAULT_TIMEOUT = 15.0  # Seconds to wait for server to come online
POLL_INTERVAL = 0.5     # Seconds between health check polls


def get_server_config(config_path: Path = JOPLIN_SETTINGS_FILEPATH) -> dict[str, Any]:
    """
    Reads the Joplin settings file and extracts configuration values
    such as api.port and api.token.
    """
    if not config_path.exists():
        logger.warning(f"Joplin settings file not found at: {config_path}")
        return {}

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except Exception as e:
        logger.error(f"Failed to read Joplin config file {config_path}: {e}")
        return {}


def get_api_credentials(config_path: Path = JOPLIN_SETTINGS_FILEPATH) -> tuple[int | None, str | None]:
    """
    Convenience function to retrieve the configured API port and token.
    """
    config = get_server_config(config_path)
    # Adjust keys based on how Joplin structures its settings JSON
    port = config.get("api.port")
    token = config.get("api.token")
    logger.info(f"Using config with api.port {port} and token starting {token[:16]}")
    return port, token


def check_server_status() -> bool:
    """
    Checks if the Joplin server is running using the CLI status command,
    falling back to a precise HTTP request check.
    """
    # 1. Try CLI check first
    try:
        result = subprocess.run(
            ["joplin", "--profile", str(JOPLIN_PROFILE_PATH), "server", "status"],
            capture_output=True,
            text=True,
            timeout=3.0
        )
        if result.returncode == 0 and "is running" in result.stdout.lower():
            return True
    except (subprocess.SubprocessError, FileNotFoundError):
        pass

    # 2. Fallback to HTTP endpoint check
    port, _ = get_api_credentials()
    if not port:
        return False

    url = f"http://localhost:{port}/ping"
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=1.5) as response:
            return response.status == 200

    except urllib.error.HTTPError as e:
        # The server IS running, but returned an HTTP error code (e.g., 401, 404, 500).
        # For a health/ping endpoint, even an error response means the server daemon is alive.
        logger.debug(f"Joplin server responded with HTTP error: {e.code} {e.reason}")
        return True

    except urllib.error.URLError as e:
        # The server is likely not running (e.g., ConnectionRefusedError)
        logger.debug(f"Joplin server unreachable: {e.reason}")
        return False

    except TimeoutError:
        logger.debug("Joplin server health check timed out.")
        return False

    except Exception as e:
        # Catch-all for any truly unexpected edge cases
        logger.debug(f"Unexpected error during server check: {e}")
        return False


def start_server(stop_on_exit: bool = True) -> subprocess.Popen | None:
    """
    Starts the Joplin server in the background as a subprocess
    if it is not already running.
    """
    global _active_process

    if check_server_status():
        logger.info("Joplin server is already running.")
        return None

    logger.info("Starting Joplin server...")

    log_dir = Path.home() / ".local" / "share" / "joplin-lite"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / "joplin_server.log"

    try:
        log_file = open(log_path, "a", encoding="utf-8")
        log_file.write("Starting Joplin server...\n")

        _active_process = subprocess.Popen(
            ["joplin", "--profile", str(JOPLIN_PROFILE_PATH), "server", "start"],
            stdout=log_file,
            stderr=subprocess.STDOUT,
            text=True
        )
        logger.info(f"Joplin server started (PID: {_active_process.pid}), logging to {log_path}")
    except Exception as e:
        logger.error(f"Failed to start Joplin server: {e}")
        return None

    if stop_on_exit:
        # Automatically register cleanup the first time we successfully start it
        atexit.register(stop_server, _active_process)

    return _active_process


def wait_for_server(timeout: float = 15.0, poll_interval: float = 0.5) -> bool:
    """
    Synchronously waits for the Joplin server to come online and respond.
    """
    start_time = time.time()
    while (time.time() - start_time) < timeout:
        if check_server_status():
            logger.info("Joplin server is online and responding.")
            return True
        time.sleep(poll_interval)

    logger.error(f"Timed out waiting for Joplin server after {timeout} seconds.")
    return False


def stop_server(process: subprocess.Popen | None = None) -> None:
    """
    Stops the Joplin server. If a subprocess handle was kept from `start_server()`,
    it terminates it; otherwise, it attempts a CLI stop command.
    """
    # Fallback to the module-level process if none is explicitly passed
    target_process = process or _active_process

    if target_process and target_process.poll() is None:
        logger.info("Stopping Joplin server subprocess...")
        target_process.terminate()
        try:
            target_process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            target_process.kill()
    else:
        logger.info("Executing Joplin server stop command...")
        try:
            subprocess.run(["joplin", "server", "stop"], capture_output=True, timeout=5)
        except Exception as e:
            logger.error(f"Error stopping Joplin server via CLI: {e}")
