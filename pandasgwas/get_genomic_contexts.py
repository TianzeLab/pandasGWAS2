from urllib.parse import quote

from pandasgwas.client import get_genomicContext
from pandasgwas.GenomicContext import GenomicContext


BASE_URL = "https://www.ebi.ac.uk/gwas/rest/api/v2/single-nucleotide-polymorphisms"


def get_genomic_contexts(
    rs_id: str = None,
    genomicContext_id: str = None,
    cached: bool = True,
    mode: str = 'Fat'
) -> GenomicContext:
    if rs_id is None or str(rs_id).strip() == "":
        raise Exception("rs_id cannot be empty")

    query_url = f"{BASE_URL}/{quote(str(rs_id), safe='')}/genomic-contexts"
    if genomicContext_id is not None and str(genomicContext_id).strip() != "":
        query_url = f"{query_url}/{quote(str(genomicContext_id), safe='')}"

    return GenomicContext(
        data=get_genomicContext(query_url, cached=cached),
        mode=mode
    )