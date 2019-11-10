from google.cloud import bigquery as bq
from scicit.config import Config

config = Config()
client = config.client()
query_config = bq.QueryJobConfig(write_disposition="WRITE_TRUNCATE")


def npl_cited_by_table():
    """
    Create a table mapping npl_publn_id and the publication_number of citing patents
    :return: bq.QueryJob
    """

    query = """
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
    query_config.destination = config.table_ref("npl_cited_by")
    job = client.query(query, job_config=query_config)
    return job


def add_cited_by():
    """
    Add cited_by field to the destination table (orig and publication_number)
    :return:
    """
    query = """
    SELECT
      * EXCEPT(cited_npl_publn_id)
    FROM
      `npl-parsing.patcit.beta` AS beta
    JOIN
      `npl-parsing.patcit.npl_cited_by` AS npl_cited_by
    ON
      beta.npl_publn_id=npl_cited_by.cited_npl_publn_id
    """
    query_config.destination = config.table_ref("beta")
    job = client.query(query, job_config=query_config)
    return job
