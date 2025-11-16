import time
import requests
from typing import Any, Dict, List, Optional


class OpenAlexClient:
    """Minimal OpenAlex API client.

    Notes:
    - For filters, use a single `filter` query param with comma-separated key:value pairs.
    - To target NLP reliably, we resolve the OpenAlex concept id for
      "natural language processing" via the concepts endpoint and then filter works with
      `concepts.id:<concept_id>`.

    Two ways to get yearly counts:
    - group_by mode: fast, aggregated counts (no pagination) using `group_by=publication_year`.
    - full mode: slow, fetches all works via cursor pagination and then counts.
    """

    BASE_URL = "https://api.openalex.org"

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or self.BASE_URL
        self.session = requests.Session()
        self._concept_cache: Dict[str, str] = {}

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request and raise for HTTP errors.

        Args:
            endpoint: API endpoint (e.g., "works").
            params: Query parameters dictionary.
        Returns:
            Parsed JSON as a dict.
        Raises:
            requests.HTTPError for non-2xx responses.
        """
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        resp = self.session.get(url, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def get_works(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Retrieve all works for given params using cursor-based pagination.

        Args:
            params: Query parameters to pass to /works.
        Returns:
            A combined list of works (results from all pages).
        """
        params = dict(params or {})
        # Ensure correct pagination params
        params.setdefault("per_page", 200)
        cursor = params.pop("cursor", "*")

        all_results: List[Dict[str, Any]] = []
        while True:
            page_params = {**params, "cursor": cursor}
            data = self.get("works", page_params)
            results = data.get("results", [])
            all_results.extend(results)
            next_cursor = data.get("meta", {}).get("next_cursor")
            if not next_cursor:
                break
            cursor = next_cursor
            # Be polite
            time.sleep(0.2)
        return all_results

    # Convenience endpoints (not used directly in the demo, but kept for completeness)
    def get_concepts(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self.get("concepts", params)

    def resolve_concept_id(self, query: str) -> str:
        """Resolve an OpenAlex concept ID from a free-text query.

        Returns the full OpenAlex ID URI (e.g., "https://openalex.org/C154945302").
        Raises a ValueError if not found.
        """
        q = query.strip().lower()
        if q in self._concept_cache:
            return self._concept_cache[q]
        data = self.get("concepts", {"search": query, "per_page": 1})
        results = data.get("results", []) if isinstance(data, dict) else []
        if not results:
            raise ValueError(f"No concept found for query: {query}")
        concept_id = results[0].get("id")
        if not concept_id:
            raise ValueError(f"Concept result missing id for query: {query}")
        self._concept_cache[q] = concept_id
        return concept_id

    def get_authors(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self.get("authors", params)

    def rate_limit_safe_get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, delay: float = 1.0) -> Dict[str, Any]:
        data = self.get(endpoint, params)
        time.sleep(delay)
        return data

    def fetch_nlp_counts_group_by(self, start_year: int, end_year: int) -> Dict[int, int]:
        """High-speed yearly counts using a single group_by query.

        - Resolves the NLP concept id once.
        - Uses /works with filter "concepts.id:<id>,publication_year:<start>-<end>"
          and group_by=publication_year.
        - Returns {year: count}. No pagination.
        """
        nlp_concept_id = self.resolve_concept_id("natural language processing")
        filter_str = f"concepts.id:{nlp_concept_id},publication_year:{start_year}-{end_year}"
        params = {
            "filter": filter_str,
            "group_by": "publication_year",
            "per_page": 200,
        }
        data = self.get("works", params)
        rows = data.get("group_by") or data.get("results") or []
        out: Dict[int, int] = {}
        for r in rows:
            try:
                year = int(r.get("key"))
            except Exception:
                continue
            count = int(r.get("count", 0))
            out[year] = count
        return out

    def fetch_nlp_counts_full_paging(self, start_year: int = 2010, end_year: int = 2025) -> Dict[int, int]:
        """Full-detail yearly counts via cursor pagination (slower).

        For each year, counts the number of works matching:
        filter = "concepts.id:<nlp_concept_id>,publication_year:YYYY"

        - Resolves the NLP concept id once.
        - Fetches all works (slow) and counts them per year.
        - Suitable when you also need to inspect detailed metadata of works.
        """
        nlp_concept_id = self.resolve_concept_id("natural language processing")

        counts: Dict[int, int] = {}
        for year in range(start_year, end_year + 1):
            try:
                filter_str = f"concepts.id:{nlp_concept_id},publication_year:{year}"
                params = {
                    "filter": filter_str,
                    "per_page": 200,
                }
                works = self.get_works(params)
                counts[year] = len(works)
                print(f"[OK] {year}: {counts[year]} works")
            except Exception as e:
                print(f"[ERROR] {year}: {e}")
                counts[year] = 0
        return counts

    def fetch_nlp_counts(self, start_year: int, end_year: int, mode: str = "group_by") -> Dict[int, int]:
        """Unified public function to fetch NLP yearly counts.

        - mode="group_by": fast, aggregated counts (recommended for trends)
        - mode="full": slow, fetches all works via pagination (for detailed metadata)
        """
        if mode == "group_by":
            return self.fetch_nlp_counts_group_by(start_year, end_year)
        elif mode == "full":
            return self.fetch_nlp_counts_full_paging(start_year, end_year)
        else:
            raise ValueError("Invalid mode. Use 'group_by' or 'full'.")

    # ---------- Multi-direction API ----------
    def fetch_counts_by_concept(self, concept_id: str, start_year: int, end_year: int) -> Dict[int, int]:
        """Fast counts by concept id using group_by=publication_year."""
        filter_str = f"concepts.id:{concept_id},publication_year:{start_year}-{end_year}"
        params = {
            "filter": filter_str,
            "group_by": "publication_year",
            "per_page": 200,
        }
        data = self.get("works", params)
        rows = data.get("group_by") or data.get("results") or []
        out: Dict[int, int] = {}
        for r in rows:
            try:
                year = int(r.get("key"))
            except Exception:
                continue
            count = int(r.get("count", 0))
            out[year] = count
        return out

    def fetch_counts_by_keywords(self, keywords: List[str], start_year: int, end_year: int) -> Dict[int, int]:
        """Fast counts by keyword search (fallback) using group_by=publication_year.

        Uses the `search` parameter across works; combines keywords with OR semantics
        by issuing one request per keyword and summing counts per year (approximate and may double-count intersections).
        """
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
                count = int(r.get("count", 0))
                combined[year] = combined.get(year, 0) + count
            time.sleep(0.15)
        return combined

    def fetch_direction_counts(self, direction: Dict[str, Any], start_year: int, end_year: int) -> Dict[int, int]:
        """Fetch counts for a given direction, preferring concept id then falling back to keywords."""
        concept_id = direction.get("concept_id")
        if concept_id:
            try:
                return self.fetch_counts_by_concept(concept_id, start_year, end_year)
            except Exception as e:
                print(f"[WARN] Concept-based query failed for {direction.get('name')}: {e}")
        keywords = direction.get("keywords") or []
        if not keywords:
            raise ValueError(f"No keywords available for direction: {direction}")
        return self.fetch_counts_by_keywords(keywords, start_year, end_year)




