"""
Fetches yearly paper counts for 30+ AI directions and uploads all JSON + CSV results
to Google Cloud Storage (GCS).

Local backup is kept under ./output/, but Cloud Run will use GCS only.

Usage:
    python run_all_directions.py
"""
from __future__ import annotations
import os
import pandas as pd

from src.config.directions import DIRECTIONS
from src.data.aggregate import aggregate_all_directions
from src.storage import upload_json   # GCS uploader
from src.viz.heatmap import plot_direction_heatmap


START_YEAR = 2010
END_YEAR = 2025
OUTPUT_DIR = "output"
CSV_NAME = "ai_directions_counts.csv"
HEATMAP_NAME = "ai_directions_heatmap.png"

# Remote GCS paths
CSV_GCS_PATH = f"output/{CSV_NAME}"
HEATMAP_GCS_PATH = f"output/{HEATMAP_NAME}"


def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # ----------------------------------------
    # 1) Aggregate counts for all directions
    # ----------------------------------------
    df = aggregate_all_directions(DIRECTIONS, START_YEAR, END_YEAR)

    # ----------------------------------------
    # 2) Save combined CSV locally
    # ----------------------------------------
    local_csv = os.path.join(OUTPUT_DIR, CSV_NAME)
    df.to_csv(local_csv, index=False)
    print(f"[LOCAL] Saved CSV: {local_csv}")

    # ----------------------------------------
    # 3) Upload combined CSV to GCS
    # ----------------------------------------
    upload_json(
        CSV_GCS_PATH,
        df.to_dict(orient="list")  # CSV stored as JSON (100% API-friendly)
    )
    print(f"[GCS] Uploaded merged JSON to: gs://ai-trend-cache/{CSV_GCS_PATH}")

    # ----------------------------------------
    # 4) Save heatmap locally
    # ----------------------------------------
    local_heatmap = os.path.join(OUTPUT_DIR, HEATMAP_NAME)
    plot_direction_heatmap(df, START_YEAR, END_YEAR, save_path=local_heatmap)
    print(f"[LOCAL] Saved heatmap: {local_heatmap}")

    # ----------------------------------------
    # 5) Upload heatmap ("image as bytes") to GCS
    # ----------------------------------------
    with open(local_heatmap, "rb") as f:
        image_bytes = f.read()

    # wrap upload for image
    upload_json(
        HEATMAP_GCS_PATH,
        {"file_bytes_b64": image_bytes.hex()}  # store binary as hex
    )
    print(f"[GCS] Uploaded heatmap to: gs://ai-trend-cache/{HEATMAP_GCS_PATH}")

    # ----------------------------------------
    # 6) Upload each direction’s JSON to GCS
    # (each produced inside aggregate step)
    # ----------------------------------------
    print("[INFO] Uploading each direction JSON to GCS...")

    for d in DIRECTIONS:
        fname = d.safe_filename()
        local_path = f"cache/{fname}"
        if os.path.exists(local_path):
            # load local file
            import json
            with open(local_path, "r", encoding="utf-8") as f:
                content = json.load(f)

            # GCS path
            gcs_path = f"cache/{fname}"

            upload_json(gcs_path, content)
            print(f"[GCS] Uploaded {fname} → gs://ai-trend-cache/{gcs_path}")
        else:
            print(f"[WARN] Local JSON missing: {local_path}")

    print("\n🎉 All data written to GCS successfully!\n")


if __name__ == "__main__":
    main()