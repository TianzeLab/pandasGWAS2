from pandasgwas.client import get_association

def test_get_association():
    a = get_association("https://www.ebi.ac.uk/gwas/rest/api/v2/associations")
    from pandasgwas.client import association_cache
    b=association_cache['https://www.ebi.ac.uk/gwas/rest/api/v2/associations']
