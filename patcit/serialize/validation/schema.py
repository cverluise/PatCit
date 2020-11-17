def get_schema(flavor, primary_key="npl_publn_id", pk_type="number"):
    assert flavor in ["npl", "pat", "bibref"]
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
                "original": {"type": "string"},
                "pubnum": {"type": "string"},
            },
        }
    else:
        schema = {
            "type": "object",
            "properties": {
                "DOI": {"type": ["string", "null"]},
                "ISSN": {"type": "array", "items": {"type": ["string", "null"]}},
                "ISBN": {"type": "array", "items": {"type": ["string", "null"]}},
                "PMCID": {"type": ["string", "null"]},
                "PMID": {"type": ["string", "null"]},
                "URL": {"type": ["string", "null"]},
                "author": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "affiliation": {"type": ["string", "null"]},
                            "family": {"type": ["string", "null"]},
                            "given": {"type": ["string", "null"]},
                            "sequence": {"type": ["string", "null"]},
                        },
                    },
                },
                "title": {"type": ["string", "null"]},
                "journal_title": {"type": ["string", "null"]},
                "journal_title_abbrev": {"type": ["string", "null"]},
                "event": {
                    "type": "object",
                    "properties": {
                        "name": {"type": ["string", "null"]},
                        "acronym": {"type": ["string", "null"]},
                        "location": {"type": ["string", "null"]},
                    },
                },
                "date": {"type": ["number", "null"]},
                "page": {"type": ["string", "null"]},
                "issue": {"type": ["string", "null"]},
                "volume": {"type": ["string", "null"]},
                "abstract": {"type": ["string", "null"]},
                "subject": {"type": "array", "items": {"type": ["string", "null"]}},
                "institution": {
                    "type": "object",
                    "properties": {
                        "acronym": {
                            "type": "array",
                            "items": {"type": ["string", "null"]},
                        },
                        "name": {"type": ["string", "null"]},
                        "place": {
                            "type": "array",
                            "items": {"type": ["string", "null"]},
                        },
                    },
                },
                "reference_count": {"type": ["number", "null"]},
                "is_referenced_by_count": {"type": ["number", "null"]},
                "reference_doi": {
                    "type": "array",
                    "items": {"type": ["string", "null"]},
                },
                "funder": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "DOI": {"type": ["string", "null"]},
                            "award": {"type": ["string", "null"]},
                            "doi_asserted_by": {"type": ["string", "null"]},
                            "name": {"type": ["string", "null"]},
                        },
                    },
                },
                "source": {"type": ["string", "null"]},
            },
            # "required": [],
            "default": {},
        }
    return schema
