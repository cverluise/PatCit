import typer

app = typer.Typer()


@app.command()
def npl_cited_by(tls201: str = None, tls211: str = None, tls212: str = None):
    """Return the npl_cited_by src table query
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
def npl_properties(bibref: str = None, tls214: str = None):
    """Return the npl_properties src table"""
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


if __name__ == "__main__":
    app()
