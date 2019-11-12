from dateutil.parser import parse
from scicit.validation.shape import is_date_format


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


def solve_issues(serialized_citation, issues):
    """

    :param serialized_citation: dict
    :param issues: list
    :return: dict
    """
    serialized_citation = solve_issue_5(serialized_citation, issues)
    serialized_citation = solve_issue_4(serialized_citation, issues)
    serialized_citation = solve_issue_3(serialized_citation)
    return serialized_citation
