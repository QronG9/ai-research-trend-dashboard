import os
from typing import Optional

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def plot_nlp_trend(df: pd.DataFrame, save_path: Optional[str] = "output/nlp_trend.png") -> None:
    """
    df: DataFrame with columns ["year", "count"]. Plots a basic line chart.
    """
    if df is None or df.empty:
        print("No data to plot.")
        return

    if save_path:
        output_dir = os.path.dirname(save_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

    plt.figure(figsize=(10, 6))
    sns.lineplot(x="year", y="count", data=df, marker="o")
    plt.title("NLP Works Per Year (OpenAlex)")
    plt.xlabel("Year")
    plt.ylabel("Number of works")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
    plt.show()


def plot_nlp_heatmap(df: pd.DataFrame) -> None:
    """
    df: DataFrame with columns ["field", "year", "count"].
    """
    if df is None or df.empty:
        print("No data to plot.")
        return

    pivot = df.pivot_table(index="year", columns="field", values="count", fill_value=0)
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot, cmap="Blues")
    plt.title("Works per Year by Field (OpenAlex)")
    plt.xlabel("Field")
    plt.ylabel("Year")
    plt.tight_layout()
    plt.show()
