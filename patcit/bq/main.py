import typer

app = typer.Typer()

PRIMARY_KEYS = ["npl_publn_id", "patcit_id"]


@app.command()
def patstat_patent_properties(tls201: str = None, tls211: str = None):
    """Return query to create the patstat_patent_properties table.
    Table to enrich patent data based on publication number. """
    query = f"""WITH
    tls211
    AS(
        SELECT
    REPLACE(CONCAT(publn_auth, "-", publn_nr, "-", publn_kind), " ", "")
    AS
    publication_number,
    CAST(REPLACE(CAST(publn_date
    AS
    STRING), "-", "") AS
    INT64) AS
    publication_date,
    appln_id,
    pat_publn_id
    FROM
    `{tls211}`)  # usptobias.patstat.tls211
    SELECT
    tls211. *,
    tls201.docdb_family_id,
    tls201.inpadoc_family_id
    FROM
    tls211
    JOIN
    `{tls201}`  # usptobias.patstat.tls201
    AS
    tls201
    ON
    tls211.appln_id = tls201.appln_id"""

    return query


@app.command()
def front_page_cited_by(tls201: str = None, tls211: str = None, tls212: str = None):
    """Return the front_page_cited_by query
    """
    query = f"""SELECT DISTINCT * FROM (
    WITH
      tls211_212 AS (
      WITH
        tls211 AS(
        SELECT
          REPLACE(CONCAT(publn_auth, "-", publn_nr, "-", publn_kind), " ",
          "") AS publication_number,
          CAST(REPLACE(CAST(publn_date AS STRING), "-","") AS INT64) AS publication_date,
          appln_id,
          pat_publn_id
        FROM
          `{tls211}` #usptobias.patstat.tls211
        WHERE
          publn_nr IS NOT NULL
          AND publn_nr != "")
      SELECT
        tls211.* EXCEPT(pat_publn_id),
        tls212.citn_origin AS origin,
        tls212.cited_npl_publn_id AS npl_publn_id
      FROM
        `{tls212}` AS tls212 #usptobias.patstat.tls212
      JOIN
        tls211
      ON
        tls212.pat_publn_id=tls211.pat_publn_id
      WHERE
        cited_npl_publn_id!=0)
    SELECT
      tls211_212.*,
      tls201.docdb_family_id,
      tls201.inpadoc_family_id
    FROM
      tls211_212
    LEFT JOIN
      `{tls201}` AS tls201 #usptobias.patstat.tls201
    ON
      tls211_212.appln_id=tls201.appln_id
    )
    ORDER BY
      npl_publn_id"""
    typer.echo(query)


@app.command()
def front_page_properties(bibref: str = None, tls214: str = None):
    """Return the front_page_properties query"""
    query = f"""
    WITH
      tmp AS (
      SELECT
        npl_publn_id,
        "BIBLIOGRAPHICAL_REFERENCE" AS npl_cat,
        LOWER(DOI) AS patcit_id
      FROM
        `{bibref}` #npl-parsing.external.v03_front_page_bibref
      WHERE
        DOI IS NOT NULL )
    SELECT
      tls214.npl_publn_id,
      tls214.npl_biblio,
      tmp.* EXCEPT(npl_publn_id)
    FROM
      `{tls214}` AS tls214 #usptobias.patstat.tls214
    LEFT JOIN
      tmp
    ON
      tls214.npl_publn_id = tmp.npl_publn_id
      """
    typer.echo(query)


@app.command()
def front_page_meta(
    properties: str = None, cited_by: str = None, primary_key: str = None
):
    """Return the front_page_meta query"""
    assert primary_key in PRIMARY_KEYS
    query = f"""
    (SELECT
      properties.*,
      cited_by.* EXCEPT(npl_publn_id)
    FROM
      `{properties}` AS properties  #npl-parsing.external.v03_front_page_properties
    LEFT JOIN
     `{cited_by}` AS cited_by  #npl-parsing.external.v03_front_page_cited_by
    ON
      properties.npl_publn_id=cited_by.npl_publn_id)"""

    if primary_key == "patcit_id":
        query_prefix = """
        WITH
          tmp AS
          """
        query_suffix = """
        SELECT
          patcit_id,
          ARRAY_AGG(DISTINCT(npl_publn_id)) AS npl_publn_id,
          ARRAY_AGG(DISTINCT(md5)) AS md5,
          ANY_VALUE(npl_cat) AS npl_cat,
          ANY_VALUE(npl_cat_score) AS npl_cat_score,
          ANY_VALUE(npl_cat_language_flag) AS npl_cat_language_flag,
          ANY_VALUE(language_code) AS language_code,
          ANY_VALUE(language_is_reliable) AS language_is_reliable,
          COUNT(cited_by.publication_number) AS is_cited_by_count,
          ARRAY_AGG(cited_by) AS cited_by,
          ARRAY_AGG(npl_biblio) AS npl_biblio,
        FROM
          `npl-parsing.external.v03_front_page_meta`,
          UNNEST(cited_by) AS cited_by
        GROUP BY
          patcit_id
        """

        query = query_prefix + query + query_suffix

    typer.echo(query)


@app.command()
def front_page_meta_public(meta: str = None):
    query = f"""
    SELECT
      * EXCEPT(npl_biblio,
        md5),
      md5 AS hash_id
    FROM
      `{meta}`"""  # npl-parsing.external.v03_front_page_meta_future
    typer.echo(query)


@app.command()
def front_page_bibref(
    meta: str = None, bibref_grobid: str = None, bibref_crossref: str = None
):
    query = f"""WITH
      tmp AS (
      SELECT
        meta.*  EXCEPT(npl_biblio),
        meta.npl_publn_id[
      OFFSET
        (0)] AS npl_publn_id_join
      FROM
        `{meta}` AS meta  #npl-parsing.external.v03_front_page_meta_future
      LEFT JOIN
        `{bibref_crossref}` AS bibref_crossref  #npl-parsing.external.patcit_crossref
      ON
        LOWER(meta.patcit_id) = LOWER(bibref_crossref.DOI)
      WHERE
        bibref_crossref.DOI IS NULL
        AND meta.npl_cat = "BIBLIOGRAPHICAL_REFERENCE")
    SELECT
      tmp.* EXCEPT(npl_publn_id_join),
      bibref_grobid.* EXCEPT(npl_publn_id)
    FROM
      tmp
    JOIN
      `{bibref_grobid}` AS bibref_grobid  #npl-parsing.external.v03_front_page_bibref
    ON
      tmp.npl_publn_id_join = bibref_grobid.npl_publn_id
    UNION ALL
    SELECT
      meta.* EXCEPT(npl_biblio),
      bibref_crossref.* EXCEPT(npl_publn_id)
    FROM
      `{meta}` AS meta  #npl-parsing.external.v03_front_page_meta_future
    INNER JOIN
      `{bibref_crossref}` AS bibref_crossref  #npl-parsing.external.patcit_crossref
    ON
      LOWER(meta.patcit_id) = LOWER(bibref_crossref.DOI)
    """

    typer.echo(query)


@app.command()
def update_front_page_bibref(bibref: str = None, bibref_grobid: str = None):
    query = f"""
    UPDATE
  `{bibref}` AS bibref  #npl-parsing.external.v03_front_page_bibref_future
    SET
      bibref.PMCID = bibref_grobid.PMCID,
      bibref.PMID = bibref_grobid.PMID
    FROM (
      SELECT
        DOI,
        ANY_VALUE(PMID) as PMID,
        ANY_VALUE(PMCID) as PMCID
      FROM
        `{bibref_grobid}`  #npl-parsing.external.v03_front_page_bibref
      GROUP BY
      DOI) bibref_grobid
    WHERE
      LOWER(bibref.DOI) = LOWER(bibref_grobid.DOI)"""

    typer.echo(query)


@app.command()
def front_page_cat(meta: str = None, cat: str = None, text_name: str = "npl_biblio"):
    query = f"""
    SELECT
      meta.* EXCEPT(
        npl_biblio,
        md5,
        npl_cat),
      cat.* EXCEPT(patcit_id,
      {text_name}),
    FROM
      `{meta}` AS meta  # npl-parsing.external.v03_front_page_meta_future
    RIGHT JOIN
      `{cat}` AS cat  # npl-parsing.external.v03_front_page_wiki
    ON
      meta.patcit_id=cat.patcit_id"""

    typer.echo(query)


def intext_patent_add_publication_number(
    grobid_intext_patent: str = None, pubnum2publication_number: str = None
):
    """Query to add publication_number to grobid_intext_patent based on CONCAT(orgname, original) (
    aka pubnum)"""
    query = f"""
    WITH
      tmp AS(
      SELECT
        *,
        CONCAT(orgname, original) AS pubnum
      FROM
        `{grobid_intext_patent}`)  # npl-parsing.patcit.v01_UScontextualPat
    SELECT
      tmp.* EXCEPT(status, epodoc),
      crossover.* EXCEPT(pubnum)
    FROM
      tmp
    LEFT JOIN
      `{pubnum2publication_number}` AS crossover  # npl-parsing.external.v03_intext_pat_pubnum
    ON
      tmp.pubnum=crossover.pubnum"""
    return query


def intext_patent(
    grobid_intext_patent: str = None, patstat_patent_properties: str = None
):
    """Return query to create the intext_patent table"""
    query = f"""
    WITH
      tmp AS (
      SELECT
        intext_patent.*,
        patent_properties.* EXCEPT(publication_number)
      FROM
        `{grobid_intext_patent}` AS intext_patent  # npl-parsing.external.v03_intext_pat
      LEFT JOIN
        `{patstat_patent_properties}` AS patent_properties
        # npl-parsing.external.patstat_patent_properties
      ON
        intext_patent.publication_number =patent_properties.publication_number)
    SELECT
      patent_properties.publication_date AS publication_date_o,
      patent_properties.appln_id AS appln_id_o,
      patent_properties.pat_publn_id AS pat_publn_id_o,
      patent_properties.docdb_family_id AS docdb_family_id_o,
      patent_properties.inpadoc_family_id AS inpadoc_family_id_o,
      tmp.*
    FROM
      tmp
    LEFT JOIN
      `npl-parsing.external.patstat_patent_properties` AS patent_properties
    ON
      tmp.publication_number_o= patent_properties.publication_number
    """
    return query


if __name__ == "__main__":
    app()
