# Recipes

## front-page

### `front-page.meta`

#### `cited_by_`

1. Generate query
   ```bash
    QUERY=$(python cli/patcit_bq_lib.py front-page-cited-by --tls201 <tls201-table> --tls211 <tls211-table> --tls212 <tls201-table>)
   ```

1. Run query and create bq table
   ```bash
    bq query --destination_table <tmp-table> --replace --use_legacy_sql=false $QUERY
   ```

    !!! warning
        When writing those lines, the query step did not work using `bq` CLI (`Resources exceeded during query execution: The query could not be executed in the allotted memory.` which seems to be due to the ordering stage). This step can be executed from the UI nevertheless.


1. Export to Google Storage in JSONL
   ```bash
    bq extract --compression=GZIP --destination_format=NEWLINE_DELIMITED_JSON <tmp-table> <cited_by-uris>
   ```

1. Import data on a compute engine (local, vmm, etc) and unzip
   ```bash
    gsutil -m cp <cited_by-uris> <dest>
    gunzip <cited_by-files>
   ```

1. Check that there is no overlap between the shards (w.r.t `npl_publn_id`)
   ```bash
   for file in $(find <cited_by*.jsonl>); do head -n 1 ${file} | jq '.npl_publn_id'  && tail -n 1 ${file}| jq '.npl_publn_id' ; done | sort | uniq -d
   ```

1. Group by `npl_publn_id` and format table:
   ```bash
   for file in $(find cited_by*.jsonl); do jq -s -c 'group_by(.npl_publn_id)[] | {npl_publn_id: (.[0].npl_publn_id)|tonumber , cited_by: [ .[] | {publication_number: .publication_number, publication_date: (.publication_date)|tonumber, origin:.origin, appln_id: (.appln_id)|tonumber, docdb_family_id: (.docdb_family_id)| tonumber, inpadoc_family_id: (.inpadoc_family_id)|tonumber }],  is_cited_by_count: length}' ${file} >> "${file}_prep" ; done;
   # or in parallel - recommended. NB: could include the decompression step
   # ls *.jsonl | cut -d. -f1 | paralell -j+0 --eta "jq -s -c 'group_by(.npl_publn_id)[] | {npl_publn_id: (.[0].npl_publn_id)|tonumber , cited_by: [ .[] | {publication_number: .publication_number, publication_date: (.publication_date)|tonumber, origin:.origin, appln_id: (.appln_id)|tonumber, docdb_family_id: (.docdb_family_id)| tonumber, inpadoc_family_id: (.inpadoc_family_id)|tonumber }],  is_cited_by_count: length} {}.jsonl.gz' >> {}_prep.jsonl && gzip {}_prep.jsonl"
   ```

1. Send back to G-storage and Load table to bq
   ```bash
   gsutil -m cp ...
   bq load --source_format NEWLINE_DELIMITED_JSON --replace --autodetect <cited_by-table> <*_prep.jsonl.gz> <schema>
   ```

#### `properties_`

1. Generate query
   ```bash
    QUERY=$(python cli/patcit_bq_lib.py  front-page-properties --bibref <bibref-table> --tls214 <tls214-table>)
   ```

1. Run query and create bq table
   ```bash
    bq query --destination_table <dest-table> --replace --use_legacy_sql=false $QUERY
   ```

1. Export to Google Storage in JSONL
   ```bash
    bq extract --compression=GZIP --destination_format=NEWLINE_DELIMITED_JSON <cited_by-table> <cited_by-uris>
   ```

1. Process files
   ```bash
    ls *.jsonl.gz | cut -d. -f1 | parallel -j+0 --eta 'python cli/patcit-cli.py serialize npl-properties {}.jsonl.gz --cat-model models/en_cat_npl_sm/ >> {}_prep.jsonl && gzip {}_prep.jsonl'
   ```

1. Send back to G-storage and Load table to bq
   ```bash
   gsutil -m cp ...
   bq load --source_format NEWLINE_DELIMITED_JSON --replace --autodetect <properties-table> <*_prep.jsonl.gz>
   ```

#### `meta - the final word

1. Generate query
   ```bash
    QUERY=$(python cli/patcit_bq_lib.py front-page-meta --properties <properties-table> --cited-by <cited_by-table> --primary_key <primary_key>)
   ```

    !!! info "primary_key"
        You can set the `primary_key` argument to `patcit_id` (recommended) or `npl_publn_id` (deprecated). In the first case, `npl_publn_id` with the same `patcit_id` will be grouped together. Otherwise, the `npl_publn_id` remains the primary key.


1. Run query and create bq table
   ```bash
     bq query --replace --use_legacy_sql=false --destination_table <meta-table> --destination_schema schema/frontpage_meta_<primary_key>bq.json $QUERY
   ```

### `frontpage.bibref`

#### `grobid/crossref_bibref_`

1. Serialize grobid raw output
   ```bash
   python cli/patcit_serialize.py grobid-npl <path> --max-workers <max_workers> >> <dest-file>.jsonl
   ```

1. Harmonize schema with `patcit_bibref`
   ```bash
   ls <dest-file>*.jsonl | parallel -j+0 --eta 'python cli/patcit_serialize.py patcit-bibref {} --src-flavor <grobid/crossref> >> patcit_{.}.jsonl && gzip patcit_{.}.jsonl'
   ```

1. Load to BQ
   ```bash
   bq load --source_format NEWLINE_DELIMITED_JSON --replace --ignore_unknown_values patcit_*.jsonl.gz schema/patcit_bibref.json
   ```

### `bibref`

1. Generate query
    ```bash
    QUERY=$(python cli/patcit_bq_lip.py front-page-bibref --meta <mate-table> --bibref-grobid <table-grobid-bibref> --bibref-crossref <table-crossref-bibref> )
    ```

1. Run query and create bq table
    ```bash
    bq query --replace --use_legacy_sql=false --destination_table <bibref-table> --destination_schema schema/frontpage_bibref.json $QUERY
    ```

1. Update table (PMID and PMCID)
   ```bash
   # TODO
   ```

## cat

```bash
bq load --source_format=NEWLINE_DELIMITED_JSON --max_bad_records=100 --ignore_unknown_values --replace --autodetect npl-parsing:external.v03_front_page_wiki gs://patcit_dev/frontpage/wiki_03.jsonl.gz
```

```
QUERY=$(python patcit/main.py bq front-page-cat --meta npl-parsing.external.v03_front_page_meta_future --cat npl-parsing.external.v03_front_page_wiki)
```

```
 bq query --replace --use_legacy_sql=false --replace --destination_table patcit-public-data:frontpage.wiki --destination_schema schema/frontpage_wiki.json $QUERY
```


## In text

### Patent


- Add `publication_number`

- Add patent properties

- Make sure it is ordered along the primary key

- Extract table to gs
    ```sql
    SELECT
      DISTINCT(CONCAT(orgname,original)) AS pubnum
    FROM
      `npl-parsing.patcit.v01_UScontextualPat`
    ```

- prep table

```bash
ls intext_patent_flat_0000000000*.jsonl | parallel -j +0 --eta "sort {} | uniq >> distinct_{}"
ls distinct_intext_patent_flat_0000000000*.jsonl | parallel -j +0 --eta "jq -s -c 'group_by(.publication_number_o)[] | {publication_number: .[0].publication_number_o, publication_date: .[0].publication_date_o, appln_id: .[0].appln_id_o, pat_publn_id: .[0].pat_publn_id_o, docdb_family_id: .[0].docdb_family_id_o, inpadoc_family_id: .[0].inpadoc_family_id_o, citation: [ .[] | {country_code: .orgname, original_number: .original, publication_number: .publication_number, publication_date: .publication_date, appln_id: .appln_id, pat_publn_id: .pat_publn_id, docdb_family_id: .docdb_family_id, inpadoc_family_id: .inpadoc_family_id} ]}' {} >> $(sed -e 's/_flat//g') && gzip $(sed -e 's/_flat//g')"
bq load --source_format=NEWLINE_DELIMITED_JSON --max_bad_records=100 --ignore_unknown_values --replace patcit-public-data:intext.patent "gs://patcit_dev/intext/intext_patent*.jsonl.gz" schema/intext_patent.json
```


### bibref

- Harmonize format

````shell script
patcit serialize patcit-bibref gold_npl_serialized_us_description_post1976_000000000000.jsonl --src-flavor grobid-intext
````


- Add bibref score

- Select bibref score above a given threshold
```shell script
ls npl_*.jsonl | parallel -j 1 --eta " patcit data bibref-silver-to-gold {} --model ../models/en_cat_bibref_sm >> score_{} && jq -c 'select(.bibref_score>.55)' score_{} >> gold_{}"
```

- Add identifiers

````shell script
ls patcit_gold_npl_serialized_us_description_pre1976_*.jsonl | parallel -j+0 --eta "mv {} {}_depr && patcit serialize add-identifier {}_depr >> {}"
````
- Load in BQ. take care to apply excatly the same schema as for `patcit_crossref

- Add patent properties & order

```sql
WITH
  bibref AS (
  SELECT
    tmp.*
  FROM
    `npl-parsing.tmp.tmp_` AS tmp
  LEFT JOIN
    `npl-parsing.external.patcit_crossref` AS crossref
  ON
    tmp.DOI=crossref.DOI
  WHERE
    crossref.DOI IS NULL
  UNION ALL
  SELECT
    tmp.patcit_id,
    tmp.publication_number_o,
    1 AS bibref_score,
    crossref.* EXCEPT(npl_publn_id)
  FROM
    `npl-parsing.tmp.tmp_` AS tmp
  INNER JOIN
    `npl-parsing.external.patcit_crossref` AS crossref
  ON
    tmp.DOI=crossref.DOI)
SELECT
  bibref.*,
  patstat.* EXCEPT(publication_number)
FROM
  bibref
LEFT JOIN
  `npl-parsing.external.patstat_patent_properties` AS patstat
ON
  bibref.publication_number_o = patstat.publication_number
```

- Order on the grouping key (e.g. patcit_id)

- Group
```shell script
ls *intext_patcit_bibref*.jsonl.gz | parallel -j 4 --eta "gunzip {} && jq -s -c 'group_by(.patcit_id)[] | {patcit_id: .[0].patcit_id , bibref_score: .[0].bibref_score, DOI: .[0].DOI, PMCID: .[0].PMCID, PMID: .[0].PMID, ISSN: .[0].ISSN, ISBN: .[0].ISBN, URL: .[0].URL, author: .[0].author, title: .[0].title, journal_title: .[0].journal_title, journal_title_abbrev: .[0].journal_title_abbrev, issue: .[0].issue, volume: .[0].volume, page: .[0].page, date: .[0].date, event: .[0].event, subject: .[0].subject, abstract: .[0].abstract, is_referenced_by_count: .[0].is_referenced_by_count, reference_count: .[0].reference_count, reference_doi: .[0].reference_doi, funder: .[0].funder, institution: .[0].institution, source: .[0].source, cited_by: [ .[] | {publication_number: .publication_number_o, publication_date: .publication_date, appln_id: .appln_id, pat_publn_id: .pat_publn_id, docdb_family_id: .docdb_family_id, inpadoc_family_id: .inpadoc_family_id }],  is_cited_by_count: length}' {.} >> prep_{.} && gzip {.} prep_{.}"
```

- load data

````shell script
 bq load --source_format=NEWLINE_DELIMITED_JSON --max_bad_records=1000 --replace patcit-public-data:intext.bibliographical_reference "gs://patcit_dev/intext/prep_*.jsonl" schema/intext_bibref.json
````
