import json
import os
from pathlib import Path
from typing import Dict, List

# Ensure we can import project modules
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
import sys
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from src.api.openalex_client import OpenAlexClient
from src.config.directions import DIRECTIONS as LEGACY_DIRECTIONS_LIST

# Convert legacy list-of-dicts DIRECTIONS (src/config/directions.py) to
# a flat mapping of name -> concept_id/keywords

def normalize_directions() -> List[Dict[str, object]]:
    out: List[Dict[str, object]] = []
    for d in LEGACY_DIRECTIONS_LIST:
        out.append({
            "name": d.get("name"),
            "concept_id": d.get("concept_id"),
            "keywords": d.get("keywords", []),
        })
    return out


def main(start_year: int = 2010, end_year: int = 2025) -> None:
    client = OpenAlexClient()
    directions = normalize_directions()

    cache_dir = ROOT / "cache"
    cache_dir.mkdir(exist_ok=True)

    for d in directions:
        name = d["name"]
        concept_id = d.get("concept_id")
        keywords = d.get("keywords", [])

        # Use concept-id fast path when available; otherwise fallback to keywords
        if concept_id:
            counts = client.fetch_counts_by_concept(concept_id, start_year, end_year)
        else:
            counts = client.fetch_counts_by_keywords(keywords, start_year, end_year)

        # Sort keys descending by year and cast to int->int mapping first
        years_sorted = sorted(counts.keys(), reverse=True)
        ordered = {str(y): int(counts.get(y, 0)) for y in years_sorted}

        # Normalize filename: lowercase, replace spaces and slashes
        slug = name.lower().replace(" ", "_").replace("/", "_").replace("(", "").replace(")", "")
        filename = f"{slug}_{start_year}_{end_year}.json"
        out_path = cache_dir / filename
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(ordered, f, ensure_ascii=False, indent=0)
        print(f"[OK] Wrote {out_path}")


if __name__ == "__main__":
    main()
