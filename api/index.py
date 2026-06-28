import os
import sys

# Ensure the project root is on the path so `backend` package resolves correctly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.main import app  # noqa: F401 — Vercel uses this `app` as the ASGI handler
