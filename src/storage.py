import json
from google.cloud import storage
from fastapi import HTTPException

BUCKET_NAME = "ai-trend-cache"

client = storage.Client()

def upload_json(path: str, data: dict):
    """Upload dictionary as JSON to GCS."""
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(path)

    blob.upload_from_string(
        json.dumps(data, indent=2),
        content_type="application/json"
    )
    return {"status": "uploaded", "path": path}


def download_json(path: str) -> dict:
    """Download JSON from GCS."""
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(path)

    if not blob.exists():
        raise HTTPException(status_code=404, detail=f"{path} not found in bucket")

    content = blob.download_as_string()
    return json.loads(content)