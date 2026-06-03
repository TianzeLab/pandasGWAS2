from urllib.parse import quote

from pandasgwas.client import get_locus
from pandasgwas.Locus import Locus


BASE_URL = "https://www.ebi.ac.uk/gwas/rest/api/v2/associations"


def get_loci(
    association_id: str = None,
    locus_id: str = None,
    cached: bool = True,
    mode: str = 'Fat'
) -> Locus:
    if association_id is None or str(association_id).strip() == "":
        raise Exception("association_id cannot be empty")

    query_url = f"{BASE_URL}/{quote(str(association_id), safe='')}/loci"
    if locus_id is not None and str(locus_id).strip() != "":
        query_url = f"{query_url}/{quote(str(locus_id), safe='')}"

    return Locus(
        data=get_locus(query_url, cached=cached),
        mode=mode
    )
