"""Query to create the npl_cited_by table"""

"""
WITH
  pat2pub AS (
  SELECT
    REPLACE(CONCAT(publn_auth, "-", publn_nr, "-", publn_kind), " ", "") AS publication_number,
    pat_publn_id
  FROM
    `usptobias.patstat.tls211`
  WHERE
    publn_nr IS NOT NULL
    AND publn_nr != "")
SELECT
  cited_npl_publn_id,
  STRUCT(ARRAY_AGG(citn_origin) AS origin,
    ARRAY_AGG(publication_number) AS publication_number) AS cited_by
FROM
  `usptobias.patstat.tls212` AS tls212
JOIN
  pat2pub
ON
  tls212.pat_publn_id=pat2pub.pat_publn_id
WHERE
  cited_npl_publn_id!=0
GROUP BY
  cited_npl_publn_id"""

"""Query to add cited_by(orig and publication_number)"""
"""
SELECT
  * EXCEPT(cited_npl_publn_id)
FROM
  `npl-parsing.patcit.beta` AS beta
JOIN
  `npl-parsing.patcit.npl_cited_by` AS npl_cited_by
ON
  beta.npl_publn_id=npl_cited_by.cited_npl_publn_id
"""
