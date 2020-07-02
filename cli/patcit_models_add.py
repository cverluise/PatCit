import re

import spacy
import typer
from spacy.language import Doc

app = typer.Typer()


# model = "en"
# dest = ""
# nlp = spacy.blank(model)
#
# text = "IEEE 802.11-Wikipedia, the free encyclopedia, http://en.wikipedia.org/wiki/IEEE-802.11,
# " \
#        "pp. 13."


def urls_matcher_(doc):
    """Add custom component matching urls based on regex"""
    # http://www.noah.org/wiki/RegEx_Python
    expression = (
        "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    )
    urls = re.findall(expression, doc.text)
    Doc.set_extension("urls", default=True, force=True)
    doc._.urls = re.findall(expression, doc.text)
    return doc


@app.command()
def urls_matcher(model: str, dest: str = None):
    nlp = spacy.blank(model) if len(model) == 2 else spacy.load(model)
    nlp.add_pipe(urls_matcher_, name="urls_matcher", last=True)
    if dest:
        nlp.to_disk(dest)
