import asyncio

from scicit.serialize.schema import tag_list, tag2attr


async def fetch_author(auth):
    """
    Return author attributes in dict
    :param auth: bs4.BeautifulSoup
    :return: dict
    """
    auth_ = {}
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


async def fetch_all_tags(id_, soup, id_name="npl_publn_id"):
    """
    Return grobid ouptut as a json
    :param id_: str
    :param soup: 'bs4.BeautifulSoup'
    :param id_name: str
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

    cit = {}

    for task in tasks:
        cit.update(task)
    cit.update({"authors": task_authors.result()})
    cit.update({id_name: id_})
    return cit
