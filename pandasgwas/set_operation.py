from pandasgwas.Ancestry import Ancestry
from pandasgwas.Association import Association
from pandasgwas.Gene import Gene
from pandasgwas.GenomicContext import GenomicContext
from pandasgwas.GenomicContext import GenomicContext
from pandasgwas.Locus import Locus
from pandasgwas.Publication import Publication
from pandasgwas.Snp import Snp
from pandasgwas.Study import Study
from pandasgwas.Trait import Trait


def bind(
        a: Ancestry | Association | Gene | GenomicContext | GenomicContext | Locus | Publication | Snp | Study | Trait,
        b: Ancestry | Association | Gene | GenomicContext | GenomicContext | Locus | Publication | Snp | Study | Trait) ->Ancestry | Association | Gene | GenomicContext | GenomicContext | Locus | Publication | Snp | Study | Trait :

    return a + b


def intersect(
        a: Ancestry | Association | Gene | GenomicContext | GenomicContext | Locus | Publication | Snp | Study | Trait,
        b: Ancestry | Association | Gene | GenomicContext | GenomicContext | Locus | Publication | Snp | Study | Trait) ->Ancestry | Association | Gene | GenomicContext | GenomicContext | Locus | Publication | Snp | Study | Trait :
    return a & b


def set_diff(
        a: Ancestry | Association | Gene | GenomicContext | GenomicContext | Locus | Publication | Snp | Study | Trait,
        b: Ancestry | Association | Gene | GenomicContext | GenomicContext | Locus | Publication | Snp | Study | Trait) -> Ancestry | Association | Gene | GenomicContext | GenomicContext | Locus | Publication | Snp | Study | Trait:
    return a - b


def set_xor(
        a: Ancestry | Association | Gene | GenomicContext | GenomicContext | Locus | Publication | Snp | Study | Trait,
        b: Ancestry | Association | Gene | GenomicContext | GenomicContext | Locus | Publication | Snp | Study | Trait) -> Ancestry | Association | Gene | GenomicContext | GenomicContext | Locus | Publication | Snp | Study | Trait:
    return a ^ b


def union(
        a: Ancestry | Association | Gene | GenomicContext | GenomicContext | Locus | Publication | Snp | Study | Trait,
        b: Ancestry | Association | Gene | GenomicContext | GenomicContext | Locus | Publication | Snp | Study | Trait) -> Ancestry | Association | Gene | GenomicContext | GenomicContext | Locus | Publication | Snp | Study | Trait:
    return a | b


def set_equal(
        a: Ancestry | Association | Gene | GenomicContext | GenomicContext | Locus | Publication | Snp | Study | Trait,
        b: Ancestry | Association | Gene | GenomicContext | GenomicContext | Locus | Publication | Snp | Study | Trait) -> Ancestry | Association | Gene | GenomicContext | GenomicContext | Locus | Publication | Snp | Study | Trait:
    return a == b
