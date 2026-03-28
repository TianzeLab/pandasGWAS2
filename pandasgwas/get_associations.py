from urllib.parse import urlencode, quote

from pandasgwas.client import get_association
from pandasgwas.Association import Association


BASE_URL = "https://www.ebi.ac.uk/gwas/rest/api/v2/associations"


def _normalize_str(value):
    if value is None:
        return None
    value = str(value).strip()
    return value if value != "" else None


def _normalize_bool_param(value, param_name: str):
    if value is None:
        return None

    if isinstance(value, bool):
        return "true" if value else "false"

    if isinstance(value, str):
        value_std = value.strip().lower()
        if value_std in {"true", "false"}:
            return value_std
        raise ValueError(
            f"{param_name} must be None, bool, 'true' or 'false', got {value!r}"
        )

    raise TypeError(
        f"{param_name} must be None, bool, 'true' or 'false', got {type(value)}"
    )


def _build_association_query_url(
    pubmed_id=None,
    rs_id=None,
    full_pvalue_set=None,
    accession_id=None,
    efo_trait=None,
    efo_id=None,
    show_child_trait=None,
    mapped_gene=None,
    extended_geneset=None
):
    params = {
        "pubmed_id": _normalize_str(pubmed_id),
        "rs_id": _normalize_str(rs_id),
        "full_pvalue_set": _normalize_bool_param(full_pvalue_set, "full_pvalue_set"),
        "accession_id": _normalize_str(accession_id),
        "efo_trait": _normalize_str(efo_trait),
        "efo_id": _normalize_str(efo_id),
        "show_child_trait": _normalize_bool_param(show_child_trait, "show_child_trait"),
        "mapped_gene": _normalize_str(mapped_gene),
        "extended_geneset": _normalize_bool_param(extended_geneset, "extended_geneset"),
    }

    params = {k: v for k, v in params.items() if v is not None}

    if not params:
        return BASE_URL

    return f"{BASE_URL}?{urlencode(params)}"


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
    association_id = _normalize_str(association_id)

    query_url = _build_association_query_url(
        pubmed_id=pubmed_id,
        rs_id=rs_id,
        full_pvalue_set=full_pvalue_set,
        accession_id=accession_id,
        efo_trait=efo_trait,
        efo_id=efo_id,
        show_child_trait=show_child_trait,
        mapped_gene=mapped_gene,
        extended_geneset=extended_geneset
    )

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

    # 无筛选参数时，这里会直接查全部
    if not has_id or has_query_filters:
        result_by_query = Association(
            data=get_association(query_url, cached=cached),
            mode=mode
        )

    # 同时有 association_id 和普通筛选参数：取交集
    if has_id and has_query_filters:
        return result_by_id & result_by_query

    # 只有 association_id
    if has_id and not has_query_filters:
        return result_by_id

    # 只有普通筛选参数，或全部为 None 时查全部
    return result_by_query
