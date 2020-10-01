import re
from urllib.parse import urlparse

import spacy
import typer
from spacy.language import Doc

app = typer.Typer()


class UrlsMatcher(object):
    name = "urls_matcher"

    def __init__(self, nlp):
        pass

    def __call__(self, doc):
        # http://www.noah.org/wiki/RegEx_Python
        expression = (
            "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F]["
            "0-9a-fA-F]))+"
        )
        Doc.set_extension("urls", default=True, force=True)
        doc._.urls = re.findall(expression, doc.text)
        return doc


class UrlsHostname(object):
    name = "urls_hostname"

    def __init__(self, nlp):
        pass

    def __call__(self, doc):
        # https://docs.python.org/3/library/urllib.parse.html
        Doc.set_extension("hostnames", default=True, force=True)
        hostnames = []
        for url in doc._.urls:
            try:
                hostnames += [urlparse(url).hostname]
            except ValueError:
                pass
        doc._.hostnames = hostnames
        return doc


@app.command()
def url_components(model: str, dest: str = None):
    """Add custom component matching and parsing urls based on regex"""
    nlp = spacy.blank(model) if len(model) == 2 else spacy.load(model)
    nlp.add_pipe(UrlsMatcher, last=True)
    nlp.add_pipe(UrlsHostname, last=True)
    if dest:
        nlp.to_disk(dest)


if __name__ == "__main__":
    app()
