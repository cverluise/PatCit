[FGer8]:https://github.com/FGer8

# READ ME

## Extract

```sql
WITH
  tmp AS (
  SELECT
    npl_publn_id,
    doi
  FROM
    `npl-parsing.patcit.v01`
  WHERE
    doi IS NOT NULL
    AND RAND()<1000/11000000 )
SELECT
  tmp.npl_publn_id,
  tmp.doi,
  npl_biblio,
  concat ("https://doi.org/", tmp.doi) as doi_url
FROM
  tmp,
  `usptobias.patstat.tls214` AS tls214
WHERE
  tmp.npl_publn_id = tls214.npl_publn_id
```

## Gold

- Labeled by Francesco Gerotto ([@FGer8][FGer8])
- 300 samples

## Results

```bash
python cli/patcit-cli.py models evaluate matching-doi data/val_matching_doi.csv
```

|       |   match_doc |   version_discrepancy |   year_discrepancy |
|:------|------------:|----------------------:|-------------------:|
| count |      300    |                   300 |             300    |
| mean  |        0.99 |                     0 |               0.02 |


Nb: part of the missing match is due to issue [#5](https://github.com/cverluise/PatCit/issues/5)
