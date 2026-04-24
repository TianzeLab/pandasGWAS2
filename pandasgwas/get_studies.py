from urllib.parse import urlencode

from pandasgwas.client import get_study
from pandasgwas.Study import Study


BASE_URL = "https://www.ebi.ac.uk/gwas/rest/api/v2/studies"


def get_studies(
    accession_id: str = None,
    pubmed_id: str = None,
    disease_trait: str = None,
    full_pvalue_set: bool = None,
    efo_id: str = None,
    efo_trait: str = None,
    cohort: str = None,
    gxe: bool = None,
    ancestral_group: str = None,
    no_of_individuals: int = None,
    show_child_trait: bool = None,
    mapped_gene: str = None,
    extended_geneset: bool = None,
    cached: bool = True,
    mode: str = 'Fat'
) -> Study:
    params = {
        "accession_id": accession_id,
        "pubmed_id": pubmed_id,
        "disease_trait": disease_trait,
        "full_pvalue_set": full_pvalue_set,
        "efo_id": efo_id,
        "efo_trait": efo_trait,
        "cohort": cohort,
        "gxe": gxe,
        "ancestral_group": ancestral_group,
        "no_of_individuals": no_of_individuals,
        "show_child_trait": show_child_trait,
        "mapped_gene": mapped_gene,
        "extended_geneset": extended_geneset,
    }

    params = {k: v for k, v in params.items() if v is not None}
    query_url = BASE_URL if not params else f"{BASE_URL}?{urlencode(params)}"

    return Study(
        data=get_study(query_url, cached=cached),
        mode=mode
    )
