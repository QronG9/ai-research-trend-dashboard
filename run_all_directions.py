"""
Orchestrates fetching counts for 30 AI directions, aggregates into a long DataFrame,
saves CSV, and generates a heatmap visualization.

Usage:
    python run_all_directions.py
"""
from __future__ import annotations
import os
import pandas as pd

from src.config.directions import DIRECTIONS
from src.data.aggregate import aggregate_all_directions
from src.viz.heatmap import plot_direction_heatmap


START_YEAR = 2010
END_YEAR = 2025
OUTPUT_DIR = "output"
CSV_PATH = os.path.join(OUTPUT_DIR, "ai_directions_counts.csv")
HEATMAP_PATH = os.path.join(OUTPUT_DIR, "ai_directions_heatmap.png")


def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Aggregate all directions
    df = aggregate_all_directions(DIRECTIONS, START_YEAR, END_YEAR)

    # Save combined CSV
    df.to_csv(CSV_PATH, index=False)
    print(f"Saved combined counts to {CSV_PATH}")

    # Plot heatmap (30 x 16 expected for 2010–2025)
    plot_direction_heatmap(df, START_YEAR, END_YEAR, save_path=HEATMAP_PATH)


if __name__ == "__main__":
    main()
