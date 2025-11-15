"""
Direction heatmap plotting utilities.
"""
from __future__ import annotations
from typing import Optional
import os

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def plot_direction_heatmap(df: pd.DataFrame, start_year: int, end_year: int, save_path: Optional[str] = "output/ai_heatmap.png") -> None:
    """
    Plot a heatmap for direction-year counts.

    Expects a long DataFrame with columns ["year", "direction", "count"].
    Produces a year (rows) x direction (columns) heatmap.
    """
    if df is None or df.empty:
        print("No data provided for heatmap.")
        return

    pivot = df.pivot_table(index="year", columns="direction", values="count", fill_value=0)
    # Reindex years to ensure a full range
    years = list(range(start_year, end_year + 1))
    pivot = pivot.reindex(years, fill_value=0)

    plt.figure(figsize=(max(12, len(pivot.columns) * 0.5), 10))
    sns.heatmap(pivot, cmap="YlGnBu")
    plt.title("AI Directions - Works per Year (OpenAlex)")
    plt.xlabel("Direction")
    plt.ylabel("Year")
    plt.tight_layout()

    if save_path:
        out_dir = os.path.dirname(save_path)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir)
        plt.savefig(save_path, dpi=150)
    plt.show()


def compute_log_heatmap(df: pd.DataFrame, start_year: int, end_year: int) -> pd.DataFrame:
    """
    Compute a log1p-transformed pivot for display in notebooks.
    Returns a pivot DataFrame with index=year and columns=direction.
    """
    if df is None or df.empty:
        return pd.DataFrame()
    pivot = df.pivot_table(index="year", columns="direction", values="count", fill_value=0)
    years = list(range(start_year, end_year + 1))
    pivot = pivot.reindex(years, fill_value=0)
    return (pivot + 1).applymap(lambda x: float(np.log1p(x)))
