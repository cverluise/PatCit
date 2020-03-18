[DOCDB]:https://www.epo.org/searching-for-patents/data/bulk-data-sets/docdb.html#tab-1
[bq-patcit]:https://console.cloud.google.com/bigquery?project=brv-patent&p=npl-parsing&d=patcit&page=dataset
[gs-patcit]:https://console.cloud.google.com/storage/browser/patcit?forceOnBucketsSortingFiltering=false&project=npl-parsing&userProject=npl-parsing
[zen-patcit]:https://zenodo.org/record/3710994#.Xm_uE5NKhEI
[v0.2-npl-release]:https://github.com/cverluise/PatCit/releases

!!! warning "Versioning"

    Zenodo versioning starts with `v0.2-npl` and `v0.1-intext`.

    Prior versions of the dataset are only available on BigQuery at this point.


## Front-page NPL citations ![](https://img.shields.io/badge/-npl-lightgrey)

|Version| Date| Features| Access|
|----|----|----|----|
|`v0.2`|March 2020 | [`v0.2-npl` release page][v0.2-npl-release]|[BigQuery][bq-patcit], [G-Storage][gs-patcit], [Zenodo][zen-patcit]|
|`v0.1`|November 2019|Parse and consolidate *all* (40 million) NPL citations reported in the DOCDB database.|[BigQuery][bq-patcit]|
|`beta`|October 2019| Parse and consolidate 100k NPL citations reported in the DOCDB database. Sandbox for data tests and user feedback.|[BigQuery][bq-patcit]|

## In-text citations ![](https://img.shields.io/badge/-in--text-lightgrey)

|Version| Date| Features| Access|
|----|----|----|----|
|`v0.1`| December 2019 | Extract, parse and consolidate patent and bibliographical reference citations for *all* USPTO patents.| [BigQuery][bq-patcit], [G-Storage][gs-patcit], [Zenodo][zen-patcit]|
|`beta`| November 2019 | Extract, parse and consolidate patent and bibliographical reference citations for 250k US patents. Sandbox for data tests and user feedback. | [BigQuery][bq-patcit]|
