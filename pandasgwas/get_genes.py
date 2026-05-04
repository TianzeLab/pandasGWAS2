from pandasgwas.client import get_gene
from pandasgwas.Gene import Gene


BASE_URL = "https://www.ebi.ac.uk/gwas/rest/api/v2/genes"


def get_genes(
    gene_name: str = None,
    cached: bool = True,
    mode: str = 'Fat'
) -> Gene:
    query_url = BASE_URL if gene_name is None else f"{BASE_URL}/{gene_name}"

    return Gene(
        data=get_gene(query_url, cached=cached),
        mode=mode
    )
