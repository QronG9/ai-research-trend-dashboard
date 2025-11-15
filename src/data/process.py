"""
Data processing utilities for transforming OpenAlex counts into DataFrames.

This module keeps things minimal and beginner-friendly. The primary utility turns a
{year: count} dictionary into a tidy pandas DataFrame ready for plotting.
"""

from typing import Dict, Tuple
import pandas as pd


def nlp_dict_to_dataframe(year_counts: Dict[int, int]) -> pd.DataFrame:
    """
    Convert {year: count} into a DataFrame with columns ["year", "count"],
    sorted by year ascending. Ensures appropriate dtypes.
    """
    if not year_counts:
        return pd.DataFrame(columns=["year", "count"]).astype({"year": "int64", "count": "int64"})

    df = pd.DataFrame(list(year_counts.items()), columns=["year", "count"]).sort_values("year")
    # Enforce types
    df["year"] = df["year"].astype(int)
    df["count"] = pd.to_numeric(df["count"], errors="coerce").fillna(0).astype(int)
    df = df.reset_index(drop=True)
    return df


def multi_field_to_dataframe(stats: Dict[Tuple[str, int], int]) -> pd.DataFrame:
    """
    Convert {("natural language processing", 2015): 123, ...}
    into a DataFrame with columns ["field", "year", "count"].
    """
    if not stats:
        return pd.DataFrame(columns=["field", "year", "count"]).astype({"field": "string", "year": "int64", "count": "int64"})

    rows = [(field, year, count) for (field, year), count in stats.items()]
    df = pd.DataFrame(rows, columns=["field", "year", "count"]).sort_values(["field", "year"]) 
    df["field"] = df["field"].astype("string")
    df["year"] = df["year"].astype(int)
    df["count"] = pd.to_numeric(df["count"], errors="coerce").fillna(0).astype(int)
    df = df.reset_index(drop=True)
    return df
