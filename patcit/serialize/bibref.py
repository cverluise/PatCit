import asyncio

from patcit.serialize.lib import tag_list, tag2attr, BIBREF_EMPTY
from glom import glom


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


def get_issn(line, flavor):
    if flavor == "grobid":
        issn = [line.get("ISSN"), line.get("ISSNe")]
        issn = list(filter(lambda x: x, issn))
    return issn


def get_url(line, flavor):
    if flavor == "grobid":
        url = line.get("target")
    return url


def get_author(line, flavor):
    author = []
    if flavor == "grobid":
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

    return author


def get_title(line, flavor):
    if flavor == "crossref":
        title = line.get("title")
        if title:
            title = "|".join(title)
    return title


def get_journal_title(line, flavor):
    if flavor == "grobid":
        journal_title = line.get("title_j")
    else:
        journal_title = (
            "|".join(line.get("container-title"))
            if line.get("container-title")
            else None
        )
    return journal_title


def get_journal_title_abbrev(line, flavor):
    if flavor == "grobid":
        journal_title_abbrev = line.get("title_abbrev_j")
    else:
        journal_title_abbrev = (
            "|".join(line.get("short-container-title"))
            if line.get("short-container-title")
            else None
        )
    return journal_title_abbrev


def get_event(line, flavor):
    if flavor == "grobid":
        name = [line.get("title_main_m"), line.get("title_m")]
        name = "|".join(filter(lambda x: x, name))
        event = {"acronym": None, "location": None, "name": name}
    else:
        event = line.get("event")
        [event.pop(k, None) for k in ["start", "end"]]
    return event


def get_date(line, flavor):
    if flavor == "grobid":
        date = line.get("year")
        date = int(date * 1e4 + 101) if date else None
    else:
        date = glom(line, "issued.date-parts")
        if date:  # assume that there is always
            date = date[0]  # we take the first element of the list
            if date[0]:
                date_ = 0
                for i in range(len(date)):
                    date_ += date[i] * 10 ^ (4 - 2 * i)
                date = date_
            else:
                date = None
    return date


def get_page(line, flavor):
    if flavor == "grobid":
        page = list(filter(lambda x: x, [line.get("from"), line.get("to")]))
        if page:
            page = "-".join(page)
        else:
            page = None
    return page


def get_volume(line, flavor):
    if flavor == "grobid":
        volume = line.get("volume")
        volume = str(volume) if volume else None
    return volume


def get_reference_doi(line, flavor):
    if flavor == "crossref":
        reference_doi = line.get("reference")
        reference_doi = (
            [ref.get("DOI") for ref in reference_doi] if reference_doi else None
        )
        if reference_doi:
            reference_doi = list(filter(lambda x: x, reference_doi))
        else:
            reference_doi = []
    return reference_doi


def get_funder(line, flavor):
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
    return funder


def to_patcit(line, flavor):
    assert flavor in ["grobid", "crossref"]
    out = BIBREF_EMPTY.copy()
    [out.update({k: v}) for k, v in line.items() if k in out.keys()]
    if flavor == "grobid":
        out.update({"ISSN": get_issn(line, flavor)})
        out.update({"URL": get_url(line, flavor)})
        out.update({"author": get_author(line, flavor)})
        out.update({"title": line.get("title_main_a")})
        out.update({"journal_title": line.get("title_j")})
        out.update({"journal_title_abbrev": line.get("title_abbrev_j")})
        out.update({"event": get_event(line, flavor)})
        out.update({"date": get_date(line, flavor)})
        out.update({"page": get_page(line, flavor)})
        out.update({"volume": get_volume(line, flavor)})
        out.update({"npl_publn_id": line.get("npl_publn_id")})
        out.update({"source": "grobid"})
    else:
        out.update({"author": get_author(line, flavor)})
        out.update({"title": get_title(line, flavor)})
        out.update({"journal_title": get_journal_title(line, flavor)})
        out.update({"journal_title_abbrev": get_journal_title_abbrev(line, flavor)})
        out.update({"date": get_date(line, flavor)})
        out.update({"reference_count": line.get("reference-count")})
        out.update({"is_referenced_by_count": line.get("is-referenced-by-count")})
        out.update({"reference_doi": get_reference_doi(line, flavor)})
        out.update({"funder": get_funder(line, flavor)})

    return out


test = [{"name": "Clinic for Plastic and Reconstructive Germany"}]
