import click
from google.cloud import bigquery as bq
from wasabi import Printer

from scicit import bq_schema
from scicit.config import Config
from scicit.utils import str_to_bq_ref, ref_to_bq_path

msg = Printer()

config = Config()
client = config.client()


def npl_cited_by_table(tls211_ref, tls212_ref, citedby_ref):
    """
    Create a table mapping npl_publn_id and the publication_number of citing patents
    :return: bq.QueryJob
    """

    query = f"""
        WITH
      pat2pub AS (
      SELECT
        REPLACE(CONCAT(publn_auth, "-", publn_nr, "-", publn_kind), " ", "") AS publication_number,
        pat_publn_id
      FROM
        `{ref_to_bq_path(tls211_ref)}` 
      WHERE
        publn_nr IS NOT NULL
        AND publn_nr != "")
    SELECT
      cited_npl_publn_id,
      [STRUCT(ARRAY_AGG(DISTINCT(citn_origin)) AS origin,
        ARRAY_AGG(DISTINCT(publication_number)) AS publication_number)] AS cited_by
    FROM
      `{ref_to_bq_path(tls212_ref)}` AS tls212
    JOIN
      pat2pub
    ON
      tls212.pat_publn_id=pat2pub.pat_publn_id
    WHERE
      cited_npl_publn_id!=0
    GROUP BY
      cited_npl_publn_id"""
    query_config = bq.QueryJobConfig()
    query_config.write_disposition = "WRITE_TRUNCATE"
    query_config.destination = citedby_ref
    job = client.query(query, job_config=query_config)
    with msg.loading("Working hard ..."):
        job.result()
    msg.good("Done")
    return job


def add_cited_by(npl_ref, citedby_ref, out_ref):
    """
    Add cited_by field to <out_ref> (orig and publication_number)
    :param npl_ref: bq.TableRef
    :param citedby_ref: bq.TableRef
    :param out_ref:bq.TableRef
    :return: bq.QueryJobConfig
    """

    query = f"""
    SELECT
      * EXCEPT(cited_npl_publn_id)
    FROM (
      SELECT
        *
      FROM
        `{ref_to_bq_path(npl_ref)}` ) AS npl
    JOIN
      `{ref_to_bq_path(citedby_ref)}` AS cited_by
    ON
      npl.npl_publn_id=cited_by.cited_npl_publn_id
    """
    query_config = bq.QueryJobConfig()
    query_config.write_disposition = "WRITE_TRUNCATE"
    query_config.destination = out_ref

    job = client.query(query, job_config=query_config)
    with msg.loading("Working hard ..."):
        job.result()
    msg.good("Done")
    return job


def add_crossref(crossref_ref, in_ref, out_ref):
    """
    Add crossref data to <out_ref>
    :param crossref_ref: bq.TableRef
    :param in_ref: bq.TableRef
    :param out_ref: bq.TableRef
    :return: bq.QueryJobConfig
    """
    table = bq.Table(out_ref, schema=bq_schema.make_aug_npl_schema())
    if any(
        [
            out_ref.table_id == table.table_id
            for table in client.list_tables(out_ref.dataset_id)
        ]
    ):
        client.delete_table(table)

        msg.info(
            f"{out_ref.dataset_id}.{out_ref.table_id} already exists. Will overwrite."
        )

    client.create_table(table)
    query = f"""
    SELECT
      npl_publn_id,
      cited_by,
      tmp.doi,
      ISSN,
      ISSNe,
      PMCID,
      PMID,
      target,
      authors,
      title_j,
      title_abbrev_j,
      title_m,
      title_main_m,
      title_main_a,
      year,
      issue,
      volume,
      tmp.from,
      tmp.to,
      abstract,
      funder,
      subject,
      Issues
    FROM (
      SELECT
        * except(DOI),
        DOI as doi
      FROM
        `{ref_to_bq_path(in_ref)}`) AS tmp
    LEFT JOIN (
      SELECT
        * EXCEPT(DOI),
        DOI as doi_
      FROM
        `{ref_to_bq_path(crossref_ref)}`) AS crossref
    ON
      crossref.doi_ = tmp.doi"""

    query_config = bq.QueryJobConfig()
    query_config.write_disposition = "WRITE_APPEND"
    query_config.destination = out_ref

    job = client.query(query, job_config=query_config)
    with msg.loading("Working hard ..."):
        job.result()
    msg.good("Done")
    return job


# npl_ref = str_to_bq_ref('npl-parsing.patcit.raw')
# citedby_ref = str_to_bq_ref('npl-parsing.external.npl_cited_by')
# crossref_ref = str_to_bq_ref('npl-parsing.external.crossref')
# dest_ref = str_to_bq_ref('npl-parsing.patcit.v01')
# tmp_ref = str_to_bq_ref('npl-parsing.tmp.tmp')
# add_cited_by(npl_ref, citedby_ref, tmp_ref)
# add_crossref(crossref_ref, tmp_ref, dest_ref)


@click.command()
@click.option(
    "--npl", default="npl-parsing.patcit.raw", help="Bq path to the npl table"
)
@click.option(
    "--citedby",
    default="npl-parsing.external.npl_cited_by",
    help="Bq path to the " "citedby table",
)
@click.option(
    "--tmp", default="npl-parsing.tmp.tmp", help="Bq path to the tmp table"
)
@click.option(
    "--tls211",
    default="usptobias.patstat.tls211",
    help="Bq path to the PatStat " "tls211 table",
)
@click.option(
    "--tls212",
    default="usptobias.patstat.tls212",
    help="Bq path to the PatStat " "tls212 table",
)
def main(tls211, tls212, citedby, npl, crossref, tmp, dest):
    tls211_ref = str_to_bq_ref(tls211)
    tls212_ref = str_to_bq_ref(tls212)
    citedby_ref = str_to_bq_ref(citedby)
    npl_ref = str_to_bq_ref(npl)
    crossref_ref = str_to_bq_ref(crossref)
    tmp_ref = str_to_bq_ref(tmp)
    dest_ref = str_to_bq_ref(dest)

    npl_cited_by_table(tls211_ref, tls212_ref, citedby_ref)
    add_cited_by(npl_ref, citedby_ref, tmp_ref)
    add_crossref(crossref_ref, tmp_ref, dest_ref)
    msg.good("Done!")


if __name__ == "__main__":
    main()
