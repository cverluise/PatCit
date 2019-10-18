import asyncio
import re

from scicit.schema import tag_list, tag2attr, cit_schema

regex = re.compile(r"[\n\r\t]")


async def fetch_author(auth):
    """
    Return author attributes in dict
    :param auth: bs4.BeautifulSoup
    :return: dict
    """
    auth_ = {"first": None, "middle": None, "surname": None, "genname": None}
    for name_part in ["first", "middle"]:
        if auth.find("forename", {"type": name_part}):
            name = auth.find("forename", {"type": name_part}).get_text()
            auth_.update({name_part: name})
    for name_part in ["surname", "genname"]:
        if auth.find(name_part):
            name = auth.find(name_part).get_text()
            auth_.update({name_part: name})
    return auth_


async def fetch_authors(soup):
    """
    Return the list of author dict
    :param soup: bs4.element.Tag
    :return: List[dict]
    """
    if soup.find_all("author"):
        authors = [fetch_author(auth) for auth in soup.find_all("author")]
        return await asyncio.gather(*authors)


async def fetch_tag(tag):
    """
    Return a dict for each tag with k the name of the tag and v the string of the tag
    :param tag: bs4.element.Tag
    :return: dict
    """
    assert tag.name in tag_list
    attr = tag2attr[tag.name]
    if attr and tag.string:
        if tag.name == "title":
            try:
                return {
                    tag.name + "_" + tag["type"] + "_" + tag[attr]: tag.string
                }
            except KeyError:
                return {tag.name + "_" + tag[attr]: tag.string}
        else:
            try:
                return {tag[attr]: tag.string}
            except KeyError:  # handles cases like <idno>Pages 15 - 20</idno>
                return {tag.name: tag.string}
    else:
        return tag.attrs


def clean_value(value):
    """
    Return the value without string control characters. Nb: Only strings are actually modified
    :param value:
    :return:
    """
    if value and isinstance(value, str):
        value = regex.sub("", str(value))
        value = value
    return value


async def fetch_all_tags(npl_publn_id, soup):
    """
    Return grobid ouptut as a json
    :param npl_publn_id: str
    :param soup: 'bs4.BeautifulSoup'
    :return: dict
    """
    tasks = []
    for tag_ in tag_list:
        for tag in soup.find_all(tag_):
            task = asyncio.create_task(fetch_tag(tag))
            tasks.append(task)
    task_authors = asyncio.create_task(fetch_authors(soup))

    tasks = await asyncio.gather(*tasks)
    await task_authors

    # TODO rename keys ?
    # The schema is hard written because if we call it from scicit.schema,
    # there is an overwrite issue. Every parsed objects have the same values
    cit = {
        "DOI": None,
        "ISSN": None,
        "ISSNe": None,
        "PMCID": None,
        "PMID": None,
        "authors": [
            {"first": None, "middle": None, "surname": None, "genname": None}
        ],
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
    for task in tasks:
        cit.update(task)
    cit.update({"authors": task_authors.result()})
    cit = {
        k: clean_value(v)
        for k, v in cit.items()
        if k in list(cit_schema.keys())
    }
    cit.update({"npl_publn_id": npl_publn_id})
    return cit
