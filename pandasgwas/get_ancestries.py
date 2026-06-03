from urllib.parse import quote

from pandasgwas.client import get_ancestry
from pandasgwas.Ancestry import Ancestry


BASE_URL = "https://www.ebi.ac.uk/gwas/rest/api/v2/studies"


def get_ancestries(
    accession_id: str = None,
    ancestry_id: str = None,
    cached: bool = True,
    mode: str = 'Fat'
) -> Ancestry:
    if accession_id is None or str(accession_id).strip() == "":
        raise Exception("accession_id cannot be empty")

    query_url = f"{BASE_URL}/{quote(str(accession_id), safe='')}/ancestries"
    if ancestry_id is not None and str(ancestry_id).strip() != "":
        query_url = f"{query_url}/{quote(str(ancestry_id), safe='')}"

    return Ancestry(
        data=get_ancestry(query_url, cached=cached),
        mode=mode
    )
