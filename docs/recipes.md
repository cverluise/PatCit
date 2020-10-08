# Recipes

## front-page

## `front-page.meta`

### `cited_by`

1. Generate query
   ```bash
    QUERY=$(python cli/patcit_bq_lib.py --tls201 <tls201-table> --tls211 <tls211-table> --tls212 <tls201-table>)
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
   # ls *.jsonl | paralell -j+0 --eta "jq -s -c 'group_by(.npl_publn_id)[] | {npl_publn_id: (.[0].npl_publn_id)|tonumber , cited_by: [ .[] | {publication_number: .publication_number, publication_date: (.publication_date)|tonumber, origin:.origin, appln_id: (.appln_id)|tonumber, docdb_family_id: (.docdb_family_id)| tonumber, inpadoc_family_id: (.inpadoc_family_id)|tonumber }],  is_cited_by_count: length} {}' >> {.}_prep.jsonl && gzip {.}_prep.jsonl"
   ```

1. Send back to G-storage and Load table to bq
   ```bash
   gsutil -m cp ...
   bq load --source_format NEWLINE_DELIMITED_JSON ----replace <cited_by-table> <*_prep.jsonl.gz> <schema>
   ```

### `properties`

1. Generate query
   ```bash
    QUERY=$(python cli/patcit_bq_lib.py  npl-properties --bibref <bibref-table> --tls214 <tls214-table>)
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
   ls *.jsonl.gz | parallel -j+0 --eta 'python cli/patcit-cli.py serialize npl-properties {} --cat-model models/en_cat_npl_sm >> {.}_prep.jsonl && gzip {.}_prep.jsonl'
   ````

1. Send back to G-storage and Load table to bq
   ```bash
   gsutil -m cp ...
   bq load --source_format NEWLINE_DELIMITED_JSON --replace <properties-table> <*_prep.jsonl.gz> <schema>
   ```
