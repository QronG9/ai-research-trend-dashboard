from __future__ import annotations
from typing import Dict, List
import os
import json
import hashlib
import pandas as pd

from src.api.openalex_client import OpenAlexClient

CACHE_DIR = os.path.join("/tmp", "ai_trend_cache")
os.makedirs(CACHE_DIR, exist_ok=True)


def _safe_cache_name(name: str) -> str:
    slug = name.lower().replace(" ", "_").replace("/", "_")
    h = hashlib.md5(name.encode("utf-8")).hexdigest()[:8]
    return f"{slug}_{h}.json"


def _cache_path_for(direction_name: str, start_year: int, end_year: int) -> str:
    fname = _safe_cache_name(f"{direction_name}_{start_year}_{end_year}")
    return os.path.join(CACHE_DIR, fname)


def aggregate_all_directions(directions: List[dict], start_year: int, end_year: int) -> pd.DataFrame:
    client = OpenAlexClient()
    rows = []

    for d in directions:
        name = d.get("name", "unknown")
        cache_path = _cache_path_for(name, start_year, end_year)

        # Try cache in /tmp to save API calls during warm invocations
        counts = None
        if os.path.exists(cache_path):
            try:
                with open(cache_path, "r", encoding="utf-8") as f:
                    cached = json.load(f)
                counts = {int(k): int(v) for k, v in cached.items()}
            except Exception:
                counts = None

        if counts is None:
            try:
                counts = client.fetch_direction_counts(d, start_year, end_year)
            except Exception as e:
                print(f"[ERROR] Failed to fetch {name}: {e}")
                counts = {}
            try:
                with open(cache_path, "w", encoding="utf-8") as f:
                    json.dump(counts, f, ensure_ascii=False)
            except Exception:
                pass

        for year, count in sorted(counts.items()):
            rows.append({"year": int(year), "direction": name, "count": int(count)})

    df = pd.DataFrame(rows, columns=["year", "direction", "count"])
    return df
