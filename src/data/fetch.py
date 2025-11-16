"""Functions for fetching data from the OpenAlex API.

- fetch yearly paper counts per concept
- fetch top venues per field
- fetch top authors per field
"""

from src.api.openalex_client import OpenAlexClient

client = OpenAlexClient()

def fetch_yearly_paper_counts_per_concept(concept, years):
    """Fetch yearly paper counts for a given concept.

    Args:
        concept (str): The concept to query.
        years (list): List of years to fetch data for.

    Returns:
        dict: Yearly paper counts.
    """
    # TODO: Implement the logic to fetch yearly paper counts per concept using the OpenAlex API.
    # Example:
    # counts = {}
    # for year in years:
    #     params = {"filter": {"concept.id": concept, "publication_year": year}}
    #     result = client.get_works(params)
    #     counts[year] = result['meta']['count']
    # return counts
    pass

def fetch_top_venues_per_field(field, n=10):
    """Fetch the top N venues for a given field.

    Args:
        field (str): The field to query.
        n (int, optional): Number of venues to fetch. Defaults to 10.

    Returns:
        list: Top N venues.
    """
    # TODO: Implement the logic to fetch top venues per field using the OpenAlex API.
    pass

def fetch_top_authors_per_field(field, n=10):
    """Fetch the top N authors for a given field.

    Args:
        field (str): The field to query.
        n (int, optional): Number of authors to fetch. Defaults to 10.

    Returns:
        list: Top N authors.
    """
    # TODO: Implement the logic to fetch top authors per field using the OpenAlex API.
    pass