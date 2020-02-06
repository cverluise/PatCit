import asyncio
from scicit.validation.shape import is_date_format

titles = ["title_j", "title_m", "title_main_a"]


async def eval_issue_1(serialized_citation):
    """
    Return 1 if the `npl_publn_id` is in the `when`field, else None
    See: https://github.com/cverluise/SciCit/issues/1
    :param serialized_citation: dict
    :return: int or None
    """
    if "when" in serialized_citation.keys():
        return (
            1
            if str(serialized_citation["npl_publn_id"]) in serialized_citation["when"]
            else None
        )


async def eval_issue_4(serialized_citation):
    """
    Return 4 if idno has a valid date format, else None
    See: https://github.com/cverluise/SciCit/issues/4
    :param serialized_citation: dict,
    :return: int or none
    """
    if "idno" in serialized_citation.keys():
        idno_str = serialized_citation["idno"]
        return 4 if is_date_format(idno_str) else None


async def eval_issue_5(serialized_citation):
    """
    Return 5 if 'doi' or ':' in DOI, else None
    See: https://github.com/cverluise/SciCit/issues/5
    :param serialized_citation: dict
    :return: int or None
    """
    if "DOI" in serialized_citation.keys():
        doi = serialized_citation["DOI"].lower()
        return 5 if (("doi" in doi) or (":" in doi)) else None


async def eval_issue_14(serialized_citation):
    """
    Return 14 if the serialized citation has not any title field
    See: https://github.com/cverluise/SciCit/issues/14
    :param serialized_citation: dict
    :return: int or None
    """
    return (
        14
        if not any([title in serialized_citation.keys() for title in titles])
        else None
    )


async def eval_issue_15(serialized_citation):
    """
    Return 15 if the serialized citation title_j is "Pages"
    See: https://github.com/cverluise/SciCit/issues/15
    :param serialized_citation: dict
    :return: int or None
    """
    if "title_j" in serialized_citation.keys():
        return 15 if serialized_citation["title_j"].lower() == "pages" else None


async def eval_issues(serialized_citation):
    """
    Return the list of issues found in the serialized citation
    :param serialized_citation: dict
    :return: list
    """
    tasks = []
    for func in [v for k, v in globals().items() if "eval_issue_" in k]:
        task = asyncio.create_task(func(serialized_citation))
        tasks.append(task)
    issues = await asyncio.gather(*tasks)
    issues = list(filter(lambda x: x, issues))
    return issues


# TODO: report test
#  asyncio.run(eval_issues({"npl_publn_id":1, 'idno': "2012-1009", 'DOI': "Doi:",
#  'when': "XP0000001"})) --> [1, 5, 14]
