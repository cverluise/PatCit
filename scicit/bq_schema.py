from google.cloud.bigquery import SchemaField

from scicit.config import Config

client = Config().client()

npl_citation = client.schema_from_json("schema/npl_citation_schema.json")

cited_by = [
    SchemaField(
        "cited_by",
        "RECORD",
        "REPEATED",
        "",
        (
            SchemaField(
                "origin",
                "STRING",
                "REPEATED",
                "Origin of the citation (e.g. APPlicant, SEArch report, etc)",
                (),
            ),
            SchemaField(
                "publication_number",
                "STRING",
                "REPEATED",
                "DOCDB publication number of citing patent(s)",
                (),
            ),
        ),
    )
]

crossref = [
    SchemaField("abstract", "STRING", "NULLABLE", "Abstract", ()),
    SchemaField("subject", "STRING", "REPEATED", "Subject", ()),
    SchemaField(
        "funder",
        "RECORD",
        "REPEATED",
        None,
        (
            SchemaField("DOI", "STRING", "NULLABLE", "Funder DOI", ()),
            SchemaField(
                "award", "STRING", "REPEATED", "Funding award identifier", ()
            ),
            SchemaField("name", "STRING", "NULLABLE", "Funder name", ()),
        ),
    ),
]


# nb: we could get it directly from crossref_schema.json but more variables at this point


def _get_index(bq_schema, name):
    for i, sf in enumerate(bq_schema):
        if isinstance(sf, SchemaField):
            if sf.name == name:
                return i


def make_aug_npl_schema():
    tmp = npl_citation.copy()

    idx_DOI = _get_index(tmp, "DOI")
    schema_DOI = tmp[idx_DOI]
    schema_doi = SchemaField(
        "doi", schema_DOI.field_type, schema_DOI.mode, schema_DOI.description
    )
    tmp.pop(idx_DOI)
    tmp.insert(idx_DOI, schema_doi)

    idx_citedby = _get_index(tmp, "npl_publn_id") + 1
    [
        tmp.insert(idx_citedby, cited_by[i])
        for i in reversed(range(len(cited_by)))
    ]

    idx_crossref = _get_index(tmp, "Issues")
    [
        tmp.insert(idx_crossref, crossref[i])
        for i in reversed(range(len(crossref)))
    ]
    return tmp
