import asyncio

from glom import glom

from patcit.serialize.lib import (
    tag_list,
    tag2attr,
    BIBREF_EMPTY,
    BIBREF_CROSSREF_UPDATE,
    BIBREF_GROBID_UPDATE,
)


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
                return {tag.name + "_" + tag["type"] + "_" + tag[attr]: tag.string}
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


# To patcit bibref


async def get_issn(line, flavor):
    if "grobid" in flavor:
        issn = [line.get("ISSN"), line.get("ISSNe")]
        issn = list(filter(lambda x: x, issn))
    else:
        issn = None
    return {"ISSN": issn}


async def get_url(line, flavor):
    if "grobid" in flavor:
        url = line.get("target")
    else:
        url = None
    return {"URL": url}


async def get_author(line, flavor):
    author = []
    if "grobid" in flavor:
        if line.get("authors"):
            for author_ in line.get("authors"):
                auth = {
                    "affiliation": None,  # Nb, the data could be obtained from Grobid
                    "family": author_.get("surname"),  #
                    "given": " ".join(
                        filter(
                            lambda x: x, [author_.get("first"), author_.get("middle")]
                        )
                    ),
                    "sequence": None,
                }
                author += [auth]
    else:
        if line.get("author"):
            for author_ in line.get("author"):
                affiliation = glom(author_, ("affiliation", ["name"]))
                affiliation = "|".join(affiliation) if affiliation else None
                auth = {
                    "affiliation": affiliation,
                    "family": author_.get("family"),
                    "given": author_.get("given"),
                    "sequence": author_.get("sequence"),
                }
                author += [auth]

    return {"author": author}


async def get_title(line, flavor):
    if flavor == "crossref":
        title = line.get("title")
        if title:
            title = "|".join(title)
    else:
        title = None
    return {"title": title}


async def get_journal_title(line, flavor):
    if "grobid" in flavor:
        journal_title = line.get("title_j")
    else:
        journal_title = (
            "|".join(line.get("container-title"))
            if line.get("container-title")
            else None
        )
    return {"journal_title": journal_title}


async def get_journal_title_abbrev(line, flavor):
    if "grobid" in flavor:
        journal_title_abbrev = line.get("title_abbrev_j")
    else:
        journal_title_abbrev = (
            "|".join(line.get("short-container-title"))
            if line.get("short-container-title")
            else None
        )
    return {"journal_title_abbrev": journal_title_abbrev}


async def get_event(line, flavor):
    if "grobid" in flavor:
        name = [line.get("title_main_m"), line.get("title_m")]
        name = "|".join(filter(lambda x: x, name))
        event = {"acronym": None, "location": None, "name": name}
    else:
        event = line.get("event")
        [event.pop(k, None) for k in ["start", "end"]]
    return {"event": event}


async def get_date(line, flavor):
    if "grobid" in flavor:
        date = line.get("year")
        date = int(date * 1e4 + 101) if date else None
    else:
        date = glom(line, "issued.date-parts")
        if date:  # assume that there is always
            date = date[0]  # we take the first element of the list
            if date[0]:
                date_ = 0
                for i in range(len(date)):
                    date_ += date[i] * 10 ** (4 - 2 * i)
                date = date_
            else:
                date = None
    return {"date": date}


async def get_page(line, flavor):
    if "grobid" in flavor:
        page = list(
            map(
                lambda x: str(x),
                filter(lambda x: x, [line.get("from"), line.get("to")]),
            )
        )
        if page:
            page = "-".join(page)
        else:
            # TODO: check that page has no field in crossref
            page = None
    return {"page": page}


async def get_issue(line, flavor):
    if "grobid" in flavor:
        issue = line.get("issue")
        issue = str(issue) if issue else None
    else:
        issue = line.get("issue")
    return {"issue": issue}


async def get_volume(line, flavor):
    if "grobid" in flavor:
        volume = line.get("volume")
        volume = str(volume) if volume else None
    return {"volume": volume}


async def get_reference_doi(line, flavor):
    if flavor == "crossref":
        reference_doi = line.get("reference")
        reference_doi = (
            [ref.get("DOI") for ref in reference_doi] if reference_doi else None
        )
        if reference_doi:
            reference_doi = list(filter(lambda x: x, reference_doi))
        else:
            reference_doi = []
    return {"reference_doi": reference_doi}


async def get_funder(line, flavor):
    if flavor == "crossref":
        funder = line.get("funder")

        if funder:
            funder_ = []
            for fund_ in funder:
                award = fund_.get("award")
                award = "|".join(award) if fund_.get("award") else None
                fund_.update(
                    {"doi_asserted_by": fund_.get("doi-asserted-by"), "award": award}
                )
                funder_ += [fund_]
            funder = funder_
        else:
            funder = []
    return {"funder": funder}


async def get_attr(attr, line, flavor):
    if attr == "ISSN":
        attr_ = get_issn(line, flavor)
    elif attr == "URL":
        attr_ = get_url(line, flavor)
    elif attr == "author":
        attr_ = get_author(line, flavor)
    elif attr == "title":
        attr_ = get_title(line, flavor)
    elif attr == "journal_title":
        attr_ = get_journal_title(line, flavor)
    elif attr == "journal_title_abbrev":
        attr_ = get_journal_title_abbrev(line, flavor)
    elif attr == "event":
        attr_ = get_event(line, flavor)
    elif attr == "date":
        attr_ = get_date(line, flavor)
    elif attr == "page":
        attr_ = get_page(line, flavor)
    elif attr == "issue":
        attr_ = get_issue(line, flavor)
    elif attr == "volume":
        attr_ = get_volume(line, flavor)
    elif attr == "reference_doi":
        attr_ = get_reference_doi(line, flavor)
    elif attr == "funder":
        attr_ = get_funder(line, flavor)
    else:
        attr_ = None
    return await attr_


async def to_patcit(line, flavor):
    """Harmonize schema for grobid & crossref src jsonl input"""
    out = BIBREF_EMPTY.copy()
    [out.update({k: v}) for k, v in line.items() if k in out.keys()]
    tasks = []

    attrs = BIBREF_GROBID_UPDATE if "grobid" in flavor else BIBREF_CROSSREF_UPDATE
    for attr in attrs:
        task = asyncio.create_task(get_attr(attr, line, flavor))
        tasks.append(task)
    tasks = await asyncio.gather(*tasks)

    for task in tasks:
        out.update(task)

    if "grobid" in flavor:
        out.update({"title": line.get("title_main_a")})
        out.update({"journal_title": line.get("title_j")})
        out.update({"journal_title_abbrev": line.get("title_abbrev_j")})
        out.update({"source": "Grobid"})
        if "intext" in flavor:
            out.update({"publication_number_o": line.get("publication_number_o")})
            out.update({"bibref_score": line.get("bibref_score")})
        else:
            out.update({"npl_publn_id": line.get("npl_publn_id")})
    else:
        out.update({"reference_count": line.get("reference-count")})
        out.update({"is_referenced_by_count": line.get("is-referenced-by-count")})

    return out
