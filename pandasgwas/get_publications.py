from urllib.parse import urlencode

from pandasgwas.client import get_publication
from pandasgwas.Publication import Publication


BASE_URL = "https://www.ebi.ac.uk/gwas/rest/api/v2/publications"


def get_publications(
    pubmed_id: str = None,
    title: str = None,
    first_author: str = None,
    cached: bool = True,
    mode: str = 'Fat'
) -> Publication:
    params = {
        "pubmed_id": pubmed_id,
        "title": title,
        "first_author": first_author,
    }

    params = {k: v for k, v in params.items() if v is not None}
    query_url = BASE_URL if not params else f"{BASE_URL}?{urlencode(params)}"

    return Publication(
        data=get_publication(query_url, cached=cached),
        mode=mode
    )
