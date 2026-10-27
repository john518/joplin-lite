"""Functions accessible to javascript via the pywebview Python-JS bridge."""

from datetime import datetime

class Api:
    def __init__(self):
        pass

    def ping(self) -> dict:
        """Health check endpoint to verify backend is responsive."""
        # print("Enter ping()")
        return {
            "status": "ok",
            "timestamp": datetime.now().isoformat()
        }
