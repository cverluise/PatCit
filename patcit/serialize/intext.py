import asyncio

import requests

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


def get_text_span(patent):
    """
    Return the start end of the extracted patent (actually the patent number, which is the only
    stable anchor) based on Grobid output
    :param patent: bs4.tag
    :return: int, int
    """
    span = patent.find("ptr")["target"].replace("#string-range", "")
    _, start, length = span.split(",")
    length = length.replace(")", "")
    start, end = (int(start), int(start) + int(length))
    return start, end


async def fetch_patent(id_, patent):
    """
    Return grobid output as a dict
    :param id_: str, id of the originating document
    :param patent: bs4.Soup
    :return: dict
    """
    pat = {}
    pat.update(patent.attrs)
    if patent.find("orgname"):
        pat.update({"orgname": patent.find("orgname").string})
    if patent.find("classcode"):
        pat.update({"kindcode": patent.find("classcode").string})

    for idno in patent.find_all("idno"):
        pat.update({idno["subtype"]: idno.string})
    pat.update({pk: id_})

    char_start, char_end = get_text_span(patent)
    pat.update({"char_start": char_start, "char_end": char_end})
    pubnum_components = filter(
        lambda x: x, [pat.get("orgname"), pat.get("original"), pat.get("kindcode")]
    )
    pat.update({"pubnum": "-".join(pubnum_components)})
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


def get_publication_number(pubnum, service):
    """Return the publication_number based on the country code and original number using the
    google patents linking api"""
    assert service in ["pubnum", "appnum"]
    root = "https://patents.google.com/api/match?"

    if pubnum:
        r = requests.get(f"{root}{service}={pubnum}")
        if r.status_code == 200:
            publication_number = r.text
            publication_number = (
                publication_number if publication_number != "notfound" else None
            )
        else:
            publication_number = None
    else:
        publication_number = None
    return publication_number
