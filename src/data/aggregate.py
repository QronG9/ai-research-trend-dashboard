"""
Aggregation utilities for combining per-direction yearly counts into a long DataFrame.
"""
from __future__ import annotations
from typing import Dict, List
import os
import json
import hashlib

import pandas as pd

from src.api.openalex_client import OpenAlexClient

CACHE_DIR = os.path.join("cache")
os.makedirs(CACHE_DIR, exist_ok=True)


def _safe_cache_name(name: str) -> str:
    """Create a filesystem-safe cache filename for a direction name."""
    slug = name.lower().replace(" ", "_").replace("/", "_")
    # ensure bounded length
    h = hashlib.md5(name.encode("utf-8")).hexdigest()[:8]
    return f"{slug}_{h}.json"


def _cache_path_for(direction_name: str, start_year: int, end_year: int) -> str:
    fname = _safe_cache_name(f"{direction_name}_{start_year}_{end_year}")
    return os.path.join(CACHE_DIR, fname)


def aggregate_all_directions(directions: List[dict], start_year: int, end_year: int) -> pd.DataFrame:
    """
    Fetch and aggregate yearly counts for all directions.

    Uses on-disk JSON caches per direction and period to avoid redundant API calls.
    Returns a long-format DataFrame with columns ["year", "direction", "count"].
    """
    client = OpenAlexClient()
    rows = []

    for d in directions:
        name = d.get("name", "unknown")
        cache_path = _cache_path_for(name, start_year, end_year)

        if os.path.exists(cache_path):
            try:
                with open(cache_path, "r", encoding="utf-8") as f:
                    cached = json.load(f)
                counts = {int(k): int(v) for k, v in cached.items()}
                print(f"[CACHE] Loaded {name} from {cache_path}")
            except Exception:
                counts = None
        else:
            counts = None

        if counts is None:
            # Fetch via client router (concept id preferred, keywords fallback)
            try:
                counts = client.fetch_direction_counts(d, start_year, end_year)
            except Exception as e:
                print(f"[ERROR] Failed to fetch {name}: {e}")
                counts = {}
            # Save cache
            try:
                with open(cache_path, "w", encoding="utf-8") as f:
                    json.dump(counts, f, ensure_ascii=False, indent=2)
                print(f"[CACHE] Saved {name} to {cache_path}")
            except Exception as e:
                print(f"[WARN] Could not write cache for {name}: {e}")

        # Append rows
        for year, count in sorted(counts.items()):
            rows.append({
                "year": int(year),
                "direction": name,
                "count": int(count),
            })

    df = pd.DataFrame(rows, columns=["year", "direction", "count"])
    return df
