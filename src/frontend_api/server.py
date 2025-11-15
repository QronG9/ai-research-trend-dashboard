"""
FastAPI backend to serve AI directions trend data and orchestrate refreshes.

Endpoints:
- GET /api/directions: list available direction names
- GET /api/direction/{name}: yearly series for a single direction
- GET /api/rankings/{year}: ranking for a specific year
- GET /api/rankings/latest: ranking for the latest available year
- GET /api/heatmap: matrix (years x directions) of counts
- POST /api/refresh: re-run run_all_directions.py to refresh data/cache
"""
from __future__ import annotations

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Tuple

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Project root and data file
ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "output" / "ai_directions_counts.csv"

app = FastAPI(title="AI Research Trend API", version="1.0.0")

# CORS (allow common dev origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


_DF_CACHE: Tuple[pd.DataFrame, float] | None = None


def _invalidate_cache() -> None:
    global _DF_CACHE
    _DF_CACHE = None


def load_df() -> pd.DataFrame:
    """Load the main long-format CSV.

    Returns empty DataFrame with correct columns if the file does not exist.
    """
    global _DF_CACHE
    cols = ["direction", "year", "count"]

    # Use simple in-memory cache keyed by file mtime
    mtime = DATA_PATH.stat().st_mtime if DATA_PATH.exists() else 0.0
    if _DF_CACHE is not None:
        cached_df, cached_mtime = _DF_CACHE
        if cached_mtime == mtime:
            return cached_df.copy()

    if not DATA_PATH.exists():
        df = pd.DataFrame(columns=cols)
    else:
        try:
            df = pd.read_csv(DATA_PATH)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to read data: {e}")
    # Ensure correct columns/types
    for c in cols:
        if c not in df.columns:
            raise HTTPException(status_code=500, detail=f"Missing column in data: {c}")
    # Coerce types
    df = df.copy()
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df["count"] = pd.to_numeric(df["count"], errors="coerce").fillna(0).astype(int)
    df["direction"] = df["direction"].astype(str)
    df = df.dropna(subset=["year"]).copy()
    df["year"] = df["year"].astype(int)
    # Update cache
    _DF_CACHE = (df.copy(), mtime)
    return df


@app.get("/api/directions")
def get_directions() -> List[str]:
    """Return sorted list of unique direction names."""
    df = load_df()
    if df.empty:
        return []
    names = sorted(df["direction"].dropna().unique().tolist())
    return names


@app.get("/api/direction/{name}")
def get_direction_series(name: str) -> Dict[str, Any]:
    """Return yearly series for a single direction."""
    df = load_df()
    if df.empty:
        return {"direction": name, "years": [], "counts": []}
    sub = df[df["direction"] == name].sort_values("year")
    years = sub["year"].astype(int).tolist()
    counts = sub["count"].astype(int).tolist()
    return {"direction": name, "years": years, "counts": counts}


@app.get("/api/rankings/{year}")
def get_rankings_year(year: int) -> List[Dict[str, Any]]:
    """Return rankings for a given year sorted by count descending."""
    df = load_df()
    if df.empty:
        return []
    sub = df[df["year"] == int(year)].copy()
    sub = sub.sort_values("count", ascending=False)
    return (
        sub[["direction", "year", "count"]]
        .assign(year=lambda d: d["year"].astype(int), count=lambda d: d["count"].astype(int))
        .to_dict(orient="records")
    )


@app.get("/api/rankings/latest")
def get_rankings_latest() -> Dict[str, Any]:
    """Return rankings for the latest available year along with the year field.

    Response format:
    { "latest_year": 2025, "items": [...] , "year": 2025, "ranking": [...] }
    The duplicated keys `year` and `ranking` are provided for compatibility with optional clients.
    """
    df = load_df()
    if df.empty:
        return {"latest_year": None, "items": [], "year": None, "ranking": []}
    latest_year = int(df["year"].max())
    items = get_rankings_year(latest_year)
    return {"latest_year": latest_year, "items": items, "year": latest_year, "ranking": items}


@app.get("/api/heatmap")
def get_heatmap() -> Dict[str, Any]:
    """Return a heatmap matrix of counts with years as rows and directions as columns."""
    df = load_df()
    if df.empty:
        return {"years": [], "directions": [], "matrix": []}
    pivot = (
        df.pivot_table(index="year", columns="direction", values="count", fill_value=0)
        .sort_index()
    )
    years = pivot.index.astype(int).tolist()
    directions = pivot.columns.tolist()
    matrix = pivot.values.tolist()
    return {"years": years, "directions": directions, "matrix": matrix}


@app.get("/api/all-directions")
def get_all_directions() -> Dict[str, Any]:
    """Bulk fetch all directions and their yearly series.

    Returns keys: directions (list) and series (mapping name -> [{year, count}, ...]).
    """
    df = load_df()
    if df.empty:
        return {"directions": [], "series": {}}
    out: Dict[str, List[Dict[str, int]]] = {}
    for name, g in df.groupby("direction"):
        g = g.sort_values("year")
        out[name] = [{"year": int(r.year), "count": int(r.count)} for r in g.itertuples(index=False)]
    directions = sorted(out.keys())
    return {"directions": directions, "series": out}


@app.post("/api/refresh")
def refresh_data() -> Dict[str, Any]:
    """Re-run the data fetching pipeline by calling run_all_directions.py.

    Captures stdout/stderr and returns them. Non-zero exit codes return status="error".
    """
    script = str(ROOT / "run_all_directions.py")
    try:
        proc = subprocess.run(
            [sys.executable, script],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=60 * 60,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to execute refresh: {e}")

    # Invalidate in-memory cache immediately after run completes
    _invalidate_cache()

    status = "ok" if proc.returncode == 0 else "error"
    # Truncate very long logs
    stdout = proc.stdout[-10000:]
    stderr = proc.stderr[-10000:]
    updated_at = pd.Timestamp.utcnow().isoformat()
    return {"status": status, "returncode": proc.returncode, "stdout": stdout, "stderr": stderr, "updated_at": updated_at}
