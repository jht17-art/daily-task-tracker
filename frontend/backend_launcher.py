import threading
import time
import requests
import uvicorn
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from backend.main import app


_backend_thread = None


def _run_backend():
    config = uvicorn.Config(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="warning",
    )
    server = uvicorn.Server(config)
    server.run()


def ensure_backend_running(timeout_seconds: int = 10):
    global _backend_thread

    # Already running?
    try:
        response = requests.get("http://127.0.0.1:8000/", timeout=1)
        if response.ok:
            return
    except Exception:
        pass

    # Start it once
    if _backend_thread is None or not _backend_thread.is_alive():
        _backend_thread = threading.Thread(target=_run_backend, daemon=True)
        _backend_thread.start()

    # Wait until it responds
    start = time.time()
    while time.time() - start < timeout_seconds:
        try:
            response = requests.get("http://127.0.0.1:8000/", timeout=1)
            if response.ok:
                return
        except Exception:
            time.sleep(0.3)

    raise RuntimeError("Backend could not be started")