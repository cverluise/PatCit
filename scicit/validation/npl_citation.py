from dateutil.parser import parse
from scicit.validation.schema import npl_citation_schema
from scicit.validation.format import is_date_format, to_number, clean_string


def prep_number(serialized_citation: dict):
    """
    Return the serialized citation with "number" fields as int
    :param serialized_citation: dict
    :return: dict
    """
    for k in [
        k
        for k, v in npl_citation_schema["properties"].items()
        if v["type"] == "number"
    ]:
        if k in serialized_citation.keys():
            serialized_citation.update({k: to_number(serialized_citation[k])})
    return serialized_citation


def prep_string(serialized_citation: dict):
    """
    Return the serialized citation with clean "string" fields
    :param serialized_citation: dict
    :return: dict
    """
    for k in [
        k
        for k, v in npl_citation_schema["properties"].items()
        if v["type"] == "string"
    ]:
        if k in serialized_citation.keys():
            serialized_citation.update(
                {k: clean_string(serialized_citation[k])}
            )
    return serialized_citation


def solve_issue_4(serialized_citation: dict, issues: list):
    """
    Update the field "when" if "idno" is a valid date (and "when" is not)
    :param serialized_citation: dict
    :param issues: list
    :return: dict
    """
    if 4 in issues:
        if "when" in serialized_citation.keys():
            when_text = serialized_citation["when"]
            if is_date_format(when_text):
                pass
            else:
                serialized_citation.update(
                    {"when": serialized_citation["idno"]}
                )
        else:
            serialized_citation.update({"when": serialized_citation["idno"]})
    return serialized_citation


def solve_issue_5(serialized_citation: dict, issues: list):
    """
    Clean "DOI" from "doi:"
    :param serialized_citation:dict
    :param issues: list
    :return: dict
    """
    if 5 in issues:
        serialized_citation["DOI"] = (
            serialized_citation["DOI"]
            .lower()
            .replace("doi", "")
            .replace(":", "")
        )
    return serialized_citation


def solve_issue_3(serialized_citation):
    """
    Create a "year" field from a valid "when" value.
    Note: should be applied AFTER solve_issue_4
    :param serialized_citation:
    :return:
    """
    if "when" in serialized_citation.keys():
        date_string = serialized_citation["when"]
        if is_date_format(date_string):
            date = parse(serialized_citation["when"])
            serialized_citation.update({"year": date.year})
    return serialized_citation
