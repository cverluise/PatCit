import asyncio
from patcit.serialize.bibref import fetch_all_tags

pk = "publication_number_o"


def split_pats_npls(soup):
    """
    Split grobid context npl object in two separate lists of npl citations and patent citations
    :param soup: bs4.Soup
    :return: (list, list), (cits, pats)
    """
    cits = []
    pats = []
    if soup.find_all("biblstruct"):
        cits = soup.find_all("biblstruct")
    if soup.find_all("biblstruct", {"type": "patent"}):
        pats = soup.find_all("biblstruct", {"type": "patent"})
    if cits and pats:
        for pat in pats:
            cits.remove(pat)
    return cits, pats


async def fetch_npls(id_, npls):
    """
    Return the list of serialized npls
    :param npls: List[bs4.element.Tag]
    :return: List[dict]
    """
    npls = [fetch_all_tags(id_, npl, pk) for npl in npls]
    return await asyncio.gather(*npls)


async def fetch_patent(id_, patent):
    """
    Return grobid output as a dict
    :param id_: str, id of the originating document
    :param patent: bs4.Soup
    :return: dict
    """
    pat = {}
    pat.update(patent.attrs)
    pat.update({"orgname": patent.find("orgname").string})
    for idno in patent.find_all("idno"):
        pat.update({idno["subtype"]: idno.string})
    pat.update({pk: id_})
    return pat


async def fetch_patents(id_, patents):
    """
    Return the list of serialized patents
    :param id_: str, id of the originating document
    :param patents: List[bs4.element.Tag]
    :return:
    """
    pats = [fetch_patent(id_, pat) for pat in patents]
    return await asyncio.gather(*pats)
