[DOCDB]:https://www.epo.org/searching-for-patents/data/bulk-data-sets/docdb.html#tab-1
[bq-patcit-old]:https://console.cloud.google.com/bigquery?project=brv-patent&p=npl-parsing&d=patcit&page=dataset
[bq-patcit]:https://console.cloud.google.com/bigquery?project=patcit-public-data&p=patcit-public-data&page=project
[v0.3-release]:https://github.com/cverluise/PatCit/releases/tag/0.3.0
[gs-patcit]:https://console.cloud.google.com/storage/browser/patcit?forceOnBucketsSortingFiltering=false&project=npl-parsing&userProject=npl-parsing
[zen-patcit]:https://zenodo.org/record/3710994#.Xm_uE5NKhEI
[v0.2-npl-release]:https://github.com/cverluise/PatCit/releases


## Front-page NPL citations

|Version| Date| Features| Access|
|----|----|----|----|
|`v0.3`| November 2020 | See [`v0.3` release page][v0.3-release].|[BigQuery][bq-patcit], [Zenodo][zen-patcit]|
|`v0.2`|March 2020 | See [`v0.2-npl` release page][v0.2-npl-release].|[BigQuery][bq-patcit-old], [Zenodo][zen-patcit]|
|`v0.1`|November 2019|Parse and consolidate *all* (40 million) NPL citations reported in the DOCDB database.|[BigQuery][bq-patcit-old]|
|`beta`|October 2019| Parse and consolidate 100k NPL citations reported in the DOCDB database. Sandbox for data tests and user feedback.|[BigQuery][bq-patcit-old]|

## In-text citations

|Version| Date| Features| Access|
|----|----|----|----|
|`v0.3`| November 2020 | See [`v0.3` release page][v0.3-release].| [BigQuery][bq-patcit], [Zenodo][zen-patcit]|
|`v0.1`| December 2019 | Extract, parse and consolidate patent and bibliographical reference citations for *all* USPTO patents.| [BigQuery][bq-patcit-old], [Zenodo][zen-patcit]|
|`beta`| November 2019 | Extract, parse and consolidate patent and bibliographical reference citations for 250k US patents. Sandbox for data tests and user feedback. | [BigQuery][bq-patcit-old]|

!!! note "Versioning"

    Zenodo versioning starts with `v0.2-npl` and `v0.1-intext`.

    Prior versions of the dataset are available on BigQuery at this point.
