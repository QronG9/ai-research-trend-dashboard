"""
ARCHIVED: The project now uses a backendless architecture.

This FastAPI server is deprecated and intentionally disabled.
All data is served as static JSON from GCS and refreshed via a Cloud Function.

- Static JSON: https://storage.googleapis.com/ai-trend-cache/{slug}_2010_2025.json
- Refresh trigger: deploy Cloud Function and POST to its URL

Keeping this file as a stub to avoid accidental use.
"""

raise ImportError("frontend_api.server is archived; backend server is no longer used.")
