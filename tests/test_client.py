from pandasgwas.client import get_association, get_study, get_trait


def test_get_association():
    a = get_association("https://www.ebi.ac.uk/gwas/rest/api/v2/associations")


def test_get_study():
    a = get_study("https://www.ebi.ac.uk/gwas/rest/api/v2/studies")


def test_get_trait():
    a = get_trait("https://www.ebi.ac.uk/gwas/rest/api/v2/efo-traits")
    a_one = get_trait("https://www.ebi.ac.uk/gwas/rest/api/v2/efo-traits/EFO_0009713")
