from urllib.parse import urlencode, quote

from pandasgwas.client import get_association
from pandasgwas.Association import Association


BASE_URL = "https://www.ebi.ac.uk/gwas/rest/api/v2/associations"


def get_associations(
    association_id: str = None,
    pubmed_id: str = None,
    rs_id: str = None,
    full_pvalue_set: bool = None,
    accession_id: str = None,
    efo_trait: str = None,
    efo_id: str = None,
    show_child_trait: bool = None,
    mapped_gene: str = None,
    extended_geneset: bool = None,
    cached: bool = True,
    mode: str = 'Fat'
) -> Association:
    # normalize string params
    association_id = None if association_id is None else str(association_id).strip()
    if association_id == "":
        association_id = None

    pubmed_id_norm = None if pubmed_id is None else str(pubmed_id).strip()
    if pubmed_id_norm == "":
        pubmed_id_norm = None

    rs_id_norm = None if rs_id is None else str(rs_id).strip()
    if rs_id_norm == "":
        rs_id_norm = None

    accession_id_norm = None if accession_id is None else str(accession_id).strip()
    if accession_id_norm == "":
        accession_id_norm = None

    efo_trait_norm = None if efo_trait is None else str(efo_trait).strip()
    if efo_trait_norm == "":
        efo_trait_norm = None

    efo_id_norm = None if efo_id is None else str(efo_id).strip()
    if efo_id_norm == "":
        efo_id_norm = None

    mapped_gene_norm = None if mapped_gene is None else str(mapped_gene).strip()
    if mapped_gene_norm == "":
        mapped_gene_norm = None

    # normalize boolean-like params
    if full_pvalue_set is None:
        full_pvalue_set_norm = None
    elif isinstance(full_pvalue_set, bool):
        full_pvalue_set_norm = "true" if full_pvalue_set else "false"
    elif isinstance(full_pvalue_set, str):
        full_pvalue_set_norm = full_pvalue_set.strip().lower()
        if full_pvalue_set_norm not in {"true", "false"}:
            raise ValueError("full_pvalue_set must be None, bool, 'true' or 'false', got %r" % full_pvalue_set)
    else:
        raise TypeError("full_pvalue_set must be None, bool, 'true' or 'false', got %r" % type(full_pvalue_set))

    if show_child_trait is None:
        show_child_trait_norm = None
    elif isinstance(show_child_trait, bool):
        show_child_trait_norm = "true" if show_child_trait else "false"
    elif isinstance(show_child_trait, str):
        show_child_trait_norm = show_child_trait.strip().lower()
        if show_child_trait_norm not in {"true", "false"}:
            raise ValueError("show_child_trait must be None, bool, 'true' or 'false', got %r" % show_child_trait)
    else:
        raise TypeError("show_child_trait must be None, bool, 'true' or 'false', got %r" % type(show_child_trait))

    if extended_geneset is None:
        extended_geneset_norm = None
    elif isinstance(extended_geneset, bool):
        extended_geneset_norm = "true" if extended_geneset else "false"
    elif isinstance(extended_geneset, str):
        extended_geneset_norm = extended_geneset.strip().lower()
        if extended_geneset_norm not in {"true", "false"}:
            raise ValueError("extended_geneset must be None, bool, 'true' or 'false', got %r" % extended_geneset)
    else:
        raise TypeError("extended_geneset must be None, bool, 'true' or 'false', got %r" % type(extended_geneset))

    params = {
        "pubmed_id": pubmed_id_norm,
        "rs_id": rs_id_norm,
        "full_pvalue_set": full_pvalue_set_norm,
        "accession_id": accession_id_norm,
        "efo_trait": efo_trait_norm,
        "efo_id": efo_id_norm,
        "show_child_trait": show_child_trait_norm,
        "mapped_gene": mapped_gene_norm,
        "extended_geneset": extended_geneset_norm,
    }

    params = {k: v for k, v in params.items() if v is not None}
    query_url = BASE_URL if not params else f"{BASE_URL}?{urlencode(params)}"

    has_id = association_id is not None
    has_query_filters = query_url != BASE_URL

    result_by_id = None
    result_by_query = None

    if has_id:
        id_url = f"{BASE_URL}/{quote(association_id)}"
        result_by_id = Association(
            data=get_association(id_url, cached=cached),
            mode=mode
        )

    if not has_id or has_query_filters:
        result_by_query = Association(
            data=get_association(query_url, cached=cached),
            mode=mode
        )

    if has_id and has_query_filters:
        return result_by_id & result_by_query
    if has_id and not has_query_filters:
        return result_by_id
    return result_by_query
