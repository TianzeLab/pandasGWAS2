import requests
import json
import progressbar
from typing import List, Dict
from requests.adapters import HTTPAdapter
from cachetools import TTLCache

fields = ['Association', 'Study', 'Trait', 'Snp', 'Ancestry', 'Publication', 'GenomicContext', 'Gene', 'Locus']
fields_and_all = ['All', 'Association', 'Study', 'Trait', 'Snp', 'Ancestry', 'Publication', 'GenomicContext', 'Gene',
                  'Locus']
association_cache = TTLCache(maxsize=2 * 1024, ttl=60 * 60 * 24)
study_cache = TTLCache(maxsize=2 * 1024, ttl=60 * 60 * 24)
trait_cache = TTLCache(maxsize=2 * 1024, ttl=60 * 60 * 24)
snp_cache = TTLCache(maxsize=2 * 1024, ttl=60 * 60 * 24)
ancestry_cache = TTLCache(maxsize=2 * 1024, ttl=60 * 60 * 24)
publication_cache = TTLCache(maxsize=2 * 1024, ttl=60 * 60 * 24)
genomicContext_cache = TTLCache(maxsize=2 * 1024, ttl=60 * 60 * 24)
gene_cache = TTLCache(maxsize=2 * 1024, ttl=60 * 60 * 24)
locus_cache = TTLCache(maxsize=2 * 1024, ttl=60 * 60 * 24)


def get_association(url: str, cached=True) -> List[Dict]:
    return get_data(url, cache_impl=association_cache, cached=cached, type='associations')


def get_study(url: str, cached=True) -> List[Dict]:
    return get_data(url, cache_impl=study_cache, cached=cached, type='studies')


def get_trait(url: str, cached=True) -> List[Dict]:
    return get_data(url, cache_impl=trait_cache, cached=cached, type='efo_traits')


def get_snp(url: str, cached=True) -> List[Dict]:
    return get_data(url, cache_impl=snp_cache, cached=cached, type='snps')


def get_ancestry(url: str, cached=True) -> List[Dict]:
    return get_data(url, cache_impl=ancestry_cache, cached=cached, type='ancestries')


def get_publication(url: str, cached=True) -> List[Dict]:
    return get_data(url, cache_impl=publication_cache, cached=cached, type='publications')


def get_genomicContext(url: str, cached=True) -> List[Dict]:
    return get_data(url, cache_impl=genomicContext_cache, cached=cached, type='genomic_contexts')


def get_gene(url: str, cached=True) -> List[Dict]:
    return get_data(url, cache_impl=gene_cache, cached=cached, type='genes')


def get_locus(url: str, cached=True) -> List[Dict]:
    return get_data(url, cache_impl=locus_cache, cached=cached, type='loci')


def reinit_cache(field: str = 'All', maxsize: int = 2 * 1024, ttl: int = 60 * 60 * 24) -> None:
    global association_cache
    global study_cache
    global trait_cache
    global snp_cache
    global ancestry_cache
    global publication_cache
    global genomicContext_cache
    global gene_cache
    global locus_cache
    if field not in fields_and_all:
        raise Exception('The field must one of %s' % str(fields_and_all))
    if field == "Association":
        association_cache = TTLCache(maxsize=maxsize, ttl=ttl)
    elif field == "Study":
        study_cache = TTLCache(maxsize=maxsize, ttl=ttl)
    elif field == "Trait":
        trait_cache = TTLCache(maxsize=maxsize, ttl=ttl)
    elif field == "Snp":
        snp_cache = TTLCache(maxsize=maxsize, ttl=ttl)
    elif field == "Ancestry":
        ancestry_cache = TTLCache(maxsize=maxsize, ttl=ttl)
    elif field == "Publication":
        publication_cache = TTLCache(maxsize=maxsize, ttl=ttl)
    elif field == "GenomicContext":
        genomicContext_cache = TTLCache(maxsize=maxsize, ttl=ttl)
    elif field == "Gene":
        gene_cache = TTLCache(maxsize=maxsize, ttl=ttl)
    elif field == "Locus":
        locus_cache = TTLCache(maxsize=maxsize, ttl=ttl)
    else:
        association_cache = TTLCache(maxsize=maxsize, ttl=ttl)
        study_cache = TTLCache(maxsize=maxsize, ttl=ttl)
        trait_cache = TTLCache(maxsize=maxsize, ttl=ttl)
        snp_cache = TTLCache(maxsize=maxsize, ttl=ttl)
        ancestry_cache = TTLCache(maxsize=maxsize, ttl=ttl)
        publication_cache = TTLCache(maxsize=maxsize, ttl=ttl)
        genomicContext_cache = TTLCache(maxsize=maxsize, ttl=ttl)
        gene_cache = TTLCache(maxsize=maxsize, ttl=ttl)
        locus_cache = TTLCache(maxsize=maxsize, ttl=ttl)


def clear_cache(field: str = 'All') -> None:
    if field not in fields_and_all:
        raise Exception('The field must one of %s' % str(fields_and_all))
    if field == 'All':
        for s in fields:
            eval(s.lower() + '_cache.clear()')
    else:
        eval(field.lower() + '_cache.clear()')


def get_data(url: str, cache_impl=None, cached=True, type=None) -> List[Dict]:
    with requests.Session() as s:
        s.mount('https://', HTTPAdapter(max_retries=5))
        if url in cache_impl and cached:
            r = cache_impl[url]
        else:
            r = s.get(url)
        if r.status_code == 200:
            if len(json.loads(r.text)) == 0:
                return []
            cache_impl[url] = r
            parsed_data = json.loads(r.text)
            if parsed_data.get('_embedded') is not None:
                results_list = parsed_data.get('_embedded').get(type)
                if parsed_data.get('_links') is not None:
                    bar = progressbar.ProgressBar(max_value=parsed_data.get('page').get('totalElements')).start()
                    progress = len(parsed_data.get('_embedded').get(type))
                    bar.update(progress)
                    next = parsed_data.get('_links').get('next')
                    while next is not None:
                        next_url = next.get('href')
                        if (next_url in cache_impl) and cached:
                            r = cache_impl[next_url]
                        else:
                            r = s.get(next_url)
                            if r.status_code == 200:
                                cache_impl[next_url] = r
                            elif r.status_code == 404:
                                return []
                            else:
                                raise Exception('The request for %s failed: response code was %d, content was \n%s' % (
                                    next_url, r.status_code, r.text))
                        parsed_data = json.loads(r.text)
                        results_list.extend(parsed_data.get('_embedded').get(type))
                        progress = progress + len(parsed_data.get('_embedded').get(type))
                        bar.update(progress)
                        next = parsed_data.get('_links').get('next')
                    bar.finish()
                return results_list
            else:
                return [parsed_data]
        elif r.status_code == 404:
            return []
        else:
            raise Exception(
                'The request for %s failed: response code was %d, content was \n%s' % (url, r.status_code, r.text))


def ask_yes_no_question(question: str) -> str:
    yes_no_answer = ""
    while yes_no_answer != "YES" and yes_no_answer != "NO":
        yes_no_answer = input(question).upper()
    return yes_no_answer


