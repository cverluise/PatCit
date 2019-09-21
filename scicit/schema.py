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

auth_schema = {"first": None, "middle": None, "surname": None, "genname": None}

cit_schema = {
    "DOI": None,
    "ISSN": None,
    "ISSNe": None,
    "PMCID": None,
    "PMID": None,
    "authors": [auth_schema],
    "from": None,
    "idno": None,
    "issue": None,
    "page": None,
    "target": None,
    "title_abbrev_j": None,
    "title_j": None,
    "title_m": None,
    "title_main_a": None,
    "title_main_m": None,
    "to": None,
    "type": None,
    "unit": None,
    "volume": None,
    "when": None,
}
