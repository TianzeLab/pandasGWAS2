from urllib.parse import urlencode

from pandasgwas.client import get_snp
from pandasgwas.Snp import Snp


BASE_URL = "https://www.ebi.ac.uk/gwas/rest/api/v2/single-nucleotide-polymorphisms"


def get_snps(
    rs_id: str = None,
    bp_location: int = None,
    bp_start: int = None,
    bp_end: int = None,
    pubmed_id: str = None,
    chromosome: str = None,
    mapped_gene: str = None,
    extended_geneset: bool = None,
    cached: bool = True,
    mode: str = 'Fat'
) -> Snp:
    params = {
        "rs_id": rs_id,
        "bp_location": bp_location,
        "bp_start": bp_start,
        "bp_end": bp_end,
        "pubmed_id": pubmed_id,
        "chromosome": chromosome,
        "mapped_gene": mapped_gene,
        "extended_geneset": extended_geneset,
    }

    params = {k: v for k, v in params.items() if v is not None}
    query_url = BASE_URL if not params else f"{BASE_URL}?{urlencode(params)}"

    return Snp(
        data=get_snp(query_url, cached=cached),
        mode=mode
    )
