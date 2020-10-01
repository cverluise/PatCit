def get_schema(flavor, primary_key="npl_publn_id", pk_type="number"):
    assert flavor in ["npl", "pat", "crossref"]
    if flavor == "npl":
        schema = {
            "type": "object",
            "properties": {
                primary_key: {"type": pk_type},
                "DOI": {"type": "string"},
                "ISSN": {"type": "string"},
                "ISSNe": {"type": "string"},
                "PMCID": {"type": "string"},
                "PMID": {"type": "string"},
                "authors": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "first": {"type": "string"},
                            "middle": {"type": "string"},
                            "surname": {"type": "string"},
                            "genname": {"type": "string"},
                        },
                    },
                },
                "target": {"type": "string"},
                "title_j": {"type": "string"},
                "title_abbrev_j": {"type": "string"},
                "title_m": {"type": "string"},
                "title_main_m": {"type": "string"},
                "title_main_a": {"type": "string"},
                "year": {"type": "number"},
                "issue": {"type": "string"},
                "volume": {"type": "number"},
                "from": {"type": "string"},
                "to": {"type": "string"},
                "issues": {"type": "array"}
                # 'page': {"type": "string"},
                # 'type': {"type": "string"},
                # 'unit': {"type":},
                # 'when': {"type": "string"}
                # 'idno': {"type":},
            },
            "required": [primary_key],
        }
    elif flavor == "pat":
        schema = {
            "type": "object",
            "properties": {
                primary_key: {"type": pk_type},
                "epodoc": {"type": "string"},
                "orgname": {"type": "string"},
                "status": {"type": "string"},
            },
        }
    else:
        schema = {
            "type": "object",
            "properties": {
                "DOI": {"type": "string"},
                "PMID": {"type": "string"},
                "PMCID": {"type": "string"},
                "ISBN": {"type": "array", "items": {"type": "string"}},
                "ISSN": {"type": "array", "items": {"type": "string"}},
                "URL": {"type": "string"},
                "abstract": {"type": "string"},
                "accepted": {"type": "string"},
                "article-number": {"type": "string"},
                "author": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "affiliation": {"type": "string"},
                            "family": {"type": "string"},
                            "given": {"type": "string"},
                            "sequence": {"type": "string"},
                        },
                    },
                },
                "container-title": {"type": "array", "items": {"type": "string"}},
                "edition-number": {"type": "string"},
                "editor": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "affiliation": {"type": "string"},
                            "family": {"type": "string"},
                            "given": {"type": "string"},
                            "sequence": {"type": "string"},
                        },
                    },
                },
                "event": {
                    "type": "object",
                    "properties": {
                        "acronym": {"type": "string"},
                        "end": {"type": "number"},
                        "location": {"type": "string"},
                        "name": {"type": "string"},
                        "start": {"type": "number"},
                    },
                },
                "funder": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "DOI": {"type": "string"},
                            "award": {"type": "string"},
                            "doi-asserted-by": {"type": "string"},
                            "name": {"type": "string"},
                        },
                    },
                },
                "institution": {
                    "type": "object",
                    "properties": {
                        "acronym": {"type": "array", "items": {"type": "string"}},
                        "name": {"type": "string"},
                        "place": {"type": "array", "items": {"type": "string"}},
                    },
                },
                "is-referenced-by-count": {"type": "number"},
                "issue": {"type": "string"},
                "issued": {"type": "number"},
                "journal-issue": {"type": "string"},
                "original-title": {"type": "array", "items": {"type": "string"}},
                "page": {"type": "string"},
                "prefix": {"type": "string"},
                "publisher": {"type": "string"},
                "publisher-location": {"type": "string"},
                "reference-count": {"type": "number"},
                "short-container-title": {"type": "array", "items": {"type": "string"}},
                "short-title": {"type": "array", "items": {"type": "string"}},
                "source": {"type": "string"},
                "standards-body": {"type": "string"},
                "subject": {"type": "array", "items": {"type": "string"}},
                "title": {"type": "array", "items": {"type": "string"}},
                "volume": {"type": "string"},
            },
            "required": [],
        }
    return schema


BIBREF_EMPTY = {
    "DOI": None,
    # "PMID": None,
    # "PMCID": None,
    "ISBN": [],
    "ISSN": [],
    "URL": None,
    "abstract": None,
    "accepted": None,
    "article-number": None,
    "author": [{"affiliation": None, "family": None, "given": None, "sequence": None}],
    "container-title": [],
    "edition-number": None,
    "editor": [{"affiliation": None, "family": None, "given": None, "sequence": None}],
    "event": [
        {"acronym": None, "end": None, "location": None, "name": None, "start": None}
    ],
    "funder": [{"DOI": None, "award": None, "doi-asserted-by": None, "name": None}],
    "institution": {"acronym": [], "name": None, "place": []},
    "is-referenced-by-count": None,
    "issue": None,
    "issued": None,
    "journal-issue": None,
    "original-title": {"type": "array", "items": None},
    "page": None,
    "prefix": None,
    "publisher": None,
    "publisher-location": None,
    "reference-count": None,
    "short-container-title": [],
    "short-title": [],
    "source": None,
    "standards-body": None,
    "subject": [],
    "title": [],
    "volume": None,
}

GROBID_TO_CROSSREF = {
    "DOI": "DOI",
    "ISSN": "ISSN",  # to list
    "ISSNe": "ISSN",  # to list
    "PMCID": "PMCID",
    "PMID": "PMID",
    "authors": "author",
    "target": "URL",
    "title_j": "container-title",  # to list
    "title_abbrev_j": "short-container-title",  # to list
    "title_m": "event.name",  # decide priority
    "title_main_m": "event.name",  # decide priority
    "title_main_a": {"type": "string"},
    "year": {"type": "number"},
    "issue": "journal-issue",  # to str
    "volume": "volume",  # to str
    "from": "page",  # to str, merge with to
    "to": "page",
    "issues": {"type": "array"},
}
