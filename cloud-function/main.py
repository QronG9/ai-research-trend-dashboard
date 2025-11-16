import functions_framework
import json
import pandas as pd
from google.cloud import storage
from flask import make_response

from src.config.directions import DIRECTIONS
from src.data.aggregate import aggregate_all_directions

BUCKET_NAME = "ai-trend-cache"

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
}

@functions_framework.http
def refresh(request):
    if request.method == "OPTIONS":
        # CORS preflight
        return make_response(('', 204, CORS_HEADERS))
    if request.method != "POST":
        resp = make_response((json.dumps({"error": "POST required"}), 405))
        for k, v in CORS_HEADERS.items():
            resp.headers[k] = v
        resp.headers["Content-Type"] = "application/json"
        return resp

    # 1) Aggregate all directions 2010–2025
    df = aggregate_all_directions(DIRECTIONS, 2010, 2025)

    # 2) Convert to per-direction JSON and upload to GCS
    direction_json = {}
    for _, row in df.iterrows():
        direction = row["direction"]
        year = int(row["year"])
        count = int(row["count"])
        direction_json.setdefault(direction, {})[year] = count

    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)

    for direction, counts in direction_json.items():
        slug = direction.lower().replace(" ", "_").replace("/", "_")
        blob = bucket.blob(f"{slug}_2010_2025.json")
        blob.upload_from_string(json.dumps(counts), content_type="application/json")

    payload = json.dumps({"status": "ok"})
    resp = make_response((payload, 200))
    for k, v in CORS_HEADERS.items():
        resp.headers[k] = v
    resp.headers["Content-Type"] = "application/json"
    return resp
