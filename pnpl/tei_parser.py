import asyncio

from bs4 import BeautifulSoup


async def fetch_author(auth):
    """
    Return author attributes in dict
    :param auth: bs4.element.Tag
    :return: dict
    """
    auth_ = {}
    if auth.find("forename", {"type": "first"}):
        first = auth.find("forename", {"type": "first"}).get_text()
        auth_.update({"first": first})
    if auth.find("forename", {"type": "middle"}):
        middle = auth.find("forename", {"type": "middle"}).get_text()
        auth_.update({"middle": middle})
    if auth.find("surname"):
        last = auth.find("surname").get_text()
        auth_.update({"last": last})
    return auth_


async def fetch_authors(analytic):
    """

    :param analytic: bs4.element.Tag
    :return: List[dict]
    """
    if analytic.find_all("author"):
        authors = [fetch_author(auth) for auth in analytic.find_all("author")]
        return await asyncio.gather(*authors)


async def fetch_doi(analytic):
    """

    :param analytic: bs4.element.Tag
    :return: str
    """
    if analytic.find("idno"):
        return analytic.find("idno").get_text()


async def fetch_art_title(analytic):
    """

    :param analytic: bs4.element.Tag
    :return: str
    """
    if analytic.find("title", {"level": "a", "type": "main"}):
        return analytic.find(
            "title", {"level": "a", "type": "main"}
        ).get_text()


async def fetch_analytic(analytic):
    """

    :param analytic: bs4.element.Tag
    :return: dict
    """
    task_authors = asyncio.create_task(fetch_authors(analytic))
    task_title_art = asyncio.create_task(fetch_art_title(analytic))
    task_doi = asyncio.create_task(fetch_doi(analytic))

    await task_authors
    await task_title_art
    await task_doi

    return {
        "authors": task_authors.result(),
        "title_art": task_title_art.result(),
        "doi": task_doi.result(),
    }


async def fetch_journ_title(monogr):
    """

    :param monogr: bs4.element.Tag
    :return: str
    """
    if monogr.find("title", {"level": "j"}):
        return monogr.find("title", {"level": "j"}).get_text()


async def fetch_imprint(monogr):
    """

    :param monogr: bs4.element.Tag
    :return: dict
    """
    imprint_ = {}
    if monogr.find("imprint").find_all("biblscope"):
        for tag in monogr.find("imprint").find_all("biblscope"):
            if tag.contents:
                imprint_.update(dict(zip(tag.attrs.values(), tag.contents)))
            else:
                imprint_.update(tag.attrs)
        return imprint_


async def fetch_monogr(monogr):
    """

    :param monogr: bs4.element.Tag
    :return: dict
    """
    task_title = asyncio.create_task(fetch_journ_title(monogr))
    task_imprint = asyncio.create_task(fetch_imprint(monogr))

    await task_title
    await task_imprint

    return {
        "title_journ": task_title.result(),
        "imprint": task_imprint.result(),
    }


async def fetch_all(response: str):
    """

    :param response: str
    :return: dict
    """
    all_ = {}
    soup_ = BeautifulSoup(response, "lxml")
    if soup_.find("analytic"):
        task_analytic = asyncio.create_task(
            fetch_analytic(soup_.find("analytic"))
        )
        await task_analytic
        all_.update(task_analytic.result())
    if soup_.find("monogr"):
        task_monogr = asyncio.create_task(fetch_monogr(soup_.find("monogr")))
        await task_monogr
        all_.update(task_monogr.result())

    return all_
