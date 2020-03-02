import click
from google.cloud import bigquery as bq
from wasabi import Printer

from patcit import bq_schema
from patcit.config import Config
from patcit.utils import str_to_bq_ref, ref_to_bq_path

msg = Printer()

config = Config()
client = config.client()


def create_table_with_schema(out_ref, flavor):
    table = bq.Table(out_ref, schema=bq_schema.make_aug_npl_schema(flavor))
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
    create_table_with_schema(out_ref, "v01")

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


def add_npl_class(src_ref, npl_class_ref, out_ref):
    create_table_with_schema(out_ref, "v02")
    query = f"""
    SELECT
      src.npl_publn_id,
      npl_c.npl_class,
      src.* EXCEPT (npl_publn_id)
    FROM
      `{ref_to_bq_path(src_ref)}` as src
      LEFT OUTER JOIN(
      SELECT * FROM
      `{ref_to_bq_path(npl_class_ref)}`) as npl_c
    ON
      src.npl_publn_id = npl_c.npl_publn_id"""

    query_config = bq.QueryJobConfig()
    query_config.write_disposition = "WRITE_APPEND"
    query_config.destination = out_ref

    job = client.query(query, job_config=query_config)
    with msg.loading("Working hard ..."):
        job.result()
    msg.good("Done")
    return job


def propagate_issn(out_ref):
    query = f"""
    UPDATE
      `{ref_to_bq_path(out_ref)}` AS dest_npl
    SET
      dest_npl.issn = issn_update.issn_imputed
    FROM (
      WITH
        restriction AS (
        WITH
          expansion AS (
          WITH
            title2issn AS (
            SELECT
              DISTINCT(title_j) AS title_j_ambiguous,
              issn AS issn_imputed
            FROM
              `{ref_to_bq_path(out_ref)}`
            WHERE
              issn IS NOT NULL)
          SELECT
            npl_publn_id,
            title_j,
            issn_imputed
          FROM
            `{ref_to_bq_path(out_ref)}` AS src_npl,
            title2issn
          WHERE
            src_npl.title_j=title2issn.title_j_ambiguous
            AND src_npl.issn IS NULL)
          #
        SELECT
          npl_publn_id,
          SPLIT(STRING_AGG(issn_imputed), ",")[
        OFFSET
          (0)] AS issn_imputed,
          SPLIT(STRING_AGG(title_j), ",")[
        OFFSET
          (0)] AS title_j,
          COUNT(npl_publn_id) AS nb_dupl
          #
        FROM
          expansion
        GROUP BY
          npl_publn_id)
      SELECT
        npl_publn_id,
        issn_imputed
      FROM
        restriction
      WHERE
        nb_dupl = 1) AS issn_update
            #
    WHERE
      dest_npl.npl_publn_id=issn_update.npl_publn_id
      AND dest_npl.issn IS NULL
    """
    # ISSUE: at this point, there are ambiguous titles (e.g. P, Pp, Pages,etc) which have
    # nb_dupl spots ambiguous titles which cause the ISSUE
    # we restrict to ambiguous titles which have only 1 ISSN to avoid the ISSUE
    job = client.query(query)
    with msg.loading("Working hard ..."):
        job.result()
    msg.good("Done")
    return job


@click.command()
@click.option("--flavor", help="Flavor of the table. E.g. v01, v02, etc")
@click.option("--dest", help="Bq path to the dest table")
@click.option(
    "--src", default="npl-parsing.patcit.raw", help="Bq path to the npl table"
)
@click.option(
    "--tls211",
    default="usptobias.patstat.tls211",
    help="Bq path to the PatStat tls211 table",
)
@click.option(
    "--tls212",
    default="usptobias.patstat.tls212",
    help="Bq path to the PatStat tls212 table",
)
@click.option(
    "--citedby",
    default="npl-parsing.external.npl_cited_by",
    help="Bq path to the " "citedby table",
)
@click.option(
    "--crossref",
    default="npl-parsing.external.crossref",
    help="Bq path to the crossref table",
)
@click.option(
    "--npl_class",
    default="npl-parsing.external.npl_class",
    help="Bq path to the npl_class table",
)
@click.option("--tmp", default="npl-parsing.tmp.tmp", help="Bq path to the tmp table")
def main(dest, src, flavor, tls211, tls212, citedby, crossref, npl_class, tmp):
    assert flavor in ["v01", "v02"]
    tls211_ref = str_to_bq_ref(tls211)
    tls212_ref = str_to_bq_ref(tls212)
    citedby_ref = str_to_bq_ref(citedby)
    src_ref = str_to_bq_ref(src)
    crossref_ref = str_to_bq_ref(crossref)
    npl_class_ref = str_to_bq_ref(npl_class)
    tmp_ref = str_to_bq_ref(tmp)
    dest_ref = str_to_bq_ref(dest)

    if flavor == "v01":
        npl_cited_by_table(tls211_ref, tls212_ref, citedby_ref)
        add_cited_by(src_ref, citedby_ref, tmp_ref)
        add_crossref(crossref_ref, tmp_ref, dest_ref)
    else:
        add_npl_class(src_ref, npl_class_ref, dest_ref)
        propagate_issn(dest_ref)
    msg.good("Done!")


if __name__ == "__main__":
    main()
