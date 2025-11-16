import time
import requests
from typing import Any, Dict, List, Optional


class OpenAlexClient:
    BASE_URL = "https://api.openalex.org"

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or self.BASE_URL
        self.session = requests.Session()
        self._concept_cache: Dict[str, str] = {}

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        resp = self.session.get(url, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def fetch_counts_by_concept(self, concept_id: str, start_year: int, end_year: int) -> Dict[int, int]:
        filter_str = f"concepts.id:{concept_id},publication_year:{start_year}-{end_year}"
        params = {"filter": filter_str, "group_by": "publication_year", "per_page": 200}
        data = self.get("works", params)
        rows = data.get("group_by") or data.get("results") or []
        out: Dict[int, int] = {}
        for r in rows:
            try:
                year = int(r.get("key"))
            except Exception:
                continue
            out[year] = int(r.get("count", 0))
        return out

    def fetch_counts_by_keywords(self, keywords: List[str], start_year: int, end_year: int) -> Dict[int, int]:
        combined: Dict[int, int] = {}
        for kw in keywords:
            params = {
                "search": kw,
                "filter": f"publication_year:{start_year}-{end_year}",
                "group_by": "publication_year",
                "per_page": 200,
            }
            data = self.get("works", params)
            rows = data.get("group_by") or data.get("results") or []
            for r in rows:
                try:
                    year = int(r.get("key"))
                except Exception:
                    continue
                combined[year] = combined.get(year, 0) + int(r.get("count", 0))
            time.sleep(0.15)
        return combined

    def fetch_direction_counts(self, direction: Dict[str, Any], start_year: int, end_year: int) -> Dict[int, int]:
        concept_id = direction.get("concept_id")
        if concept_id:
            try:
                return self.fetch_counts_by_concept(concept_id, start_year, end_year)
            except Exception:
                pass
        keywords = direction.get("keywords") or []
        return self.fetch_counts_by_keywords(keywords, start_year, end_year)
