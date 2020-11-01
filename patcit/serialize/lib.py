tag2attr = {
    "addrline": None,
    "author": None,
    "biblscope": "unit",
    "date": None,
    "editor": None,
    "idno": "type",
    "note": None,
    "ptr": "type",
    "publisher": None,
    "pubplace": None,
    "title": "level",
}

tag_list = list(tag2attr.keys())

BIBREF_EMPTY = {
    "DOI": None,
    "ISBN": [],
    "ISSN": [],
    "PMID": None,
    "PMCID": None,
    "URL": None,
    "author": [{"affiliation": None, "family": None, "given": None, "sequence": None}],
    "title": None,
    "journal_title": None,
    "journal_title_abbrev": None,
    "event": {"acronym": None, "location": None, "name": None},
    "date": None,
    "page": None,
    "issue": None,
    "volume": None,
    "abstract": None,
    "subject": [],
    "institution": {"acronym": [], "name": None, "place": []},
    "reference_count": None,
    "is_referenced_by_count": None,
    "reference_doi": [],
    "funder": [{"DOI": None, "award": None, "doi_asserted_by": None, "name": None}],
    "source": None,
}

BIBREF_GROBID_UPDATE = [
    "ISSN",
    "URL",
    "author",
    "event",
    "date",
    "page",
    "issue",
    "volume",
]
BIBREF_CROSSREF_UPDATE = [
    "author",
    "date",
    "title",
    "journal_title",
    "journal_title_abbrev",
    "reference_doi",
    "funder",
]
