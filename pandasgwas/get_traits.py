from urllib.parse import urlencode

from pandasgwas.client import get_trait
from pandasgwas.Trait import Trait


BASE_URL = "https://www.ebi.ac.uk/gwas/rest/api/v2/efo-traits"


def get_traits(
    efo_trait: str = None,
    uri: str = None,
    efo_id: str = None,
    pubmed_id: str = None,
    mapped_gene: str = None,
    extended_geneset: bool = None,
    cached: bool = True,
    mode: str = 'Fat'
) -> Trait:
    params = {
        "efo_trait": efo_trait,
        "uri": uri,
        "efo_id": efo_id,
        "pubmed_id": pubmed_id,
        "mapped_gene": mapped_gene,
        "extended_geneset": extended_geneset,
    }

    params = {k: v for k, v in params.items() if v is not None}
    query_url = BASE_URL if not params else f"{BASE_URL}?{urlencode(params)}"

    return Trait(
        data=get_trait(query_url, cached=cached),
        mode=mode
    )
