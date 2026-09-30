#  pandasGWAS2: a Python package for Programmatic Access to GWAS Catalog RESTful API V2

## Installation
`pip install pandasgwas`
## Example
Get studies related to triple-negative breast cancer:
```Python
from pandasgwas import get_studies
studies = get_studies(disease_trait = 'triple-negative breast cancer')
studies.studies[0:2]
#                 initial_sample_size                 replication_sample_size study_id   gxe    gxg   snp_count qualifier  imputed  pooled  accession_id user_requested  pubmed_id              platforms                      disease_trait                           terms_of_license                                  full_summary_stats                  full_summary_stats_available
#0  7,178 European ancestry female cases, 94,407 E...            NA             None    False  False        NaN    None     True     False  GCST90652497      None       39753771   Affymetrix,Illumina [NR] (imputed)  Triple-negative breast cancer  https://creativecommons.org/publicdomain/zero/...                                                 NA              False           
#1  262 Bantu-speaking African female cases, 1,101...            NA             None    False  False  1.799e+07    None     True     False  GCST90551896      None       40229280        Illumina [17986095] (imputed)  Triple-negative breast cancer  https://creativecommons.org/publicdomain/zero/...  http://ftp.ebi.ac.uk/pub/databases/gwas/summar...               True
```

Aggregate queried results using mathematical symbols. In addition to using the plus sign(+), the package can also use other symbols(-, &, |, ^) to perform corresponding set operations on data objects of the same type.
```Python
from pandasgwas import get_studies
study1=get_studies(disease_trait='Suicide risk')
study2=get_studies(disease_trait="Dupuytren's disease")
study3=get_studies(disease_trait="Triglycerides")
study4=get_studies(disease_trait="Retinal vascular caliber")
study5=get_studies(disease_trait="Non-small cell lung cancer (survival)")
all_studies=study1+study2+study3+study4+study5
```
## Summary statistics
>It’s important to note that the data available on the FTP and REST API out of sync. The FTP is updated nightly with any newly ingested data. Currently, we’re unable to release more data to the REST API as it’s undergoing a complete redevelopment to help us cope with the tremendous growth in summary statistics data.

Due to the above description on the official website, pandasGWAS has established a programming interface to query summary statistics data based on FTP data.    
An example to get started is as follows:
```Python
from pandasgwas.summary_statistics import search, browser, download, parse
#Search the index based on PubMed_id, study_accession_id, and EFO_trait_id. The indexed results will be returned as a DataFrame.
search_DF = search(PubMed_id='27918534', study_accession_id='GCST003966')
#Based on the index results, view the data directory on the browser.
browser(search_DF)
#Based on index results, download summary statistics data in $Home/pandasgwas_home.
download(search_DF)
#Based on the index results, load the data from $Home/pandasgwas_home and convert it into a DataFrame. 
df = parse(search_DF)
``` 
## Documentation
See [pandasGWAS Documentation](https://caotianze.github.io/pandasgwas/)
## Licensing information
### Source code
MIT License
### Data from NHGRI-EBI GWAS Catalog
The NHGRI-EBI GWAS Catalog and all its contents are available under the general [Terms of Use for EMBL-EBI Services](https://www.ebi.ac.uk/about/terms-of-use). Summary statistics are made available under [CC0](https://creativecommons.org/publicdomain/zero/1.0/) unless [otherwise stated](https://www.ebi.ac.uk/gwas/docs/faq#faq-H7).
## Similar projects
R package [gwasrapidd](https://github.com/ramiromagno/gwasrapidd) by Ramiro Magno
## Cite this work
Cao, T., Li, A. & Huang, Y. pandasGWAS: a Python package for easy retrieval of GWAS catalog data. BMC Genomics 24, 238 (2023). https://doi.org/10.1186/s12864-023-09340-2
