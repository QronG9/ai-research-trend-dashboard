from src.api.openalex_client import OpenAlexClient
from src.data.process import nlp_dict_to_dataframe
from src.viz.charts import plot_nlp_trend


def main():
    client = OpenAlexClient()
    # Use fast aggregated counts via group_by (single API call, ~1s)
    year_counts = client.fetch_nlp_counts(2010, 2025, mode="group_by")
    df = nlp_dict_to_dataframe(year_counts)
    print(df.head())
    plot_nlp_trend(df)


if __name__ == "__main__":
    main()