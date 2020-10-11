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
