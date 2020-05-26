# READ ME


## Pred

`results-20200222-221204.csv`

```sql
WITH
  tmp AS (
  SELECT
    npl_publn_id AS npl_publn_id_,
    title_abbrev_j,
    title_j,
    title_m,
    title_main_a,
    title_main_m,
    year,
    issue,
    volume
  FROM
    `npl-parsing.patcit.v01`
  WHERE
    14 NOT IN UNNEST(issues)
    AND RAND()<1000/16000000
    AND doi IS NULL)
SELECT
  npl_publn_id,
  npl_biblio,
  title_abbrev_j,
  title_j,
  title_m,
  title_main_a,
  title_main_m,
  year,
  issue,
  volume
FROM
  tmp,
  `usptobias.patstat.tls214`
WHERE
  tmp.npl_publn_id_ = npl_publn_id
```

## Gold

- Tech: Doccano
- Labeled by hand by Francesco Gerotto
- 150 bibliographical references

## Results


```
 python bin/eval-results.py --gold validation/ref_parsing/gold-20200222-221204.json --pred validation/ref_parsing/results-20200222-221204.csv --flavor "ref_parsing"
```


||True|False|Accuracy
---|---|---|---
`year_wna`|138|12|0.92
`year_wona`|136|6|0.96
`volume_wna`|135|15|0.9
`volume_wona`|102|7|0.94
`issue_wna`|132|18|0.88
`issue_wona`|38|13|0.75
`title_main_a_wna`|116|34|0.77
`title_main_a_wona`|58|28|0.67
`title_j_wna`|107|43|0.71
`title_j_wona`|88|33|0.73
`title_m_wna`|120|30|0.8
`title_m_wona`|12|16|0.43

- `wna`: with na
- `wona`: without na

From `eval-20200222-221204.csv`
