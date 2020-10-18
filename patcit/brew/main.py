import json
import re
from urllib.parse import urlparse

import spacy
import typer
from smart_open import open

from patcit.utils.tools import parse_date

app = typer.Typer()

LABEL_COLLECTION = {"WIKI": ["DATE", "ITEM"], "DATABASE": ["NAME", "DATE", "ACC_NUM"]}
URL_EXPRESSION = (
    "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),\—]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
)
TO_UPPER = {"WIKI": [], "DATABASE": ["NAME"]}
TO_LOWER = {"WIKI": [], "DATABASE": []}
TO_STRING = {"WIKI": ["ITEM"], "DATABASE": []}
PUNCTUATION = """'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'"""  # from string.punctuation


def yield_npl_biblio(file):
    with open(file, "r") as fin:
        for line in fin:
            l = json.loads(line)
            out = l.get("npl_biblio")
            if not out:
                out = l.get("text")
            yield out


def brew_date(date: list):
    date = [parse_date(date_) for date_ in date]
    date = list(set(filter(lambda x: x, date)))
    return date


def brew_url_components(doc):
    urls = re.findall(URL_EXPRESSION, doc.text.encode("utf-8").decode())
    urls = [url.encode("utf-8").decode().rstrip(PUNCTUATION) for url in urls]
    hostnames = []
    for url in urls:
        try:
            hostname = urlparse(url).hostname
            hostnames += [hostname]
        except ValueError:
            pass
    return urls, hostnames


def normalize_labels(out, category, sep="|"):
    for to_format in [TO_UPPER, TO_LOWER]:
        for var in to_format[category]:
            var = var.lower()
            if out.get(var):
                out.update({var: list(set([e.upper() for e in out.get(var)]))})
    # for var in TO_STRING[category]:  # left for later
    #     var = var.lower()
    #     if out.get(var):
    #         els = out.get(var)
    #         els.sort()  # sort to make sure that the join is always done is a consistent way
    #         out.update({var: f"{sep}".join(els)})
    return out


def brewer(doc, line, category):
    labels = LABEL_COLLECTION[category]
    out = {}

    ents = doc.ents

    # Collect labels in general
    for label in labels:
        out.update(
            {
                label.lower(): list(
                    set([ent.text for ent in ents if ent.label_ == label])
                )
            }
        )

    # Parse dates as yyyymmdd int
    if out.get("date"):
        date = brew_date(out.get("date"))
        out.update({"date": date})

    # Collect urls
    urls, hostnames = brew_url_components(doc)
    out.update({"url": urls, "hostname": hostnames})

    # Normalize vars
    out = normalize_labels(out, category)

    line.update(out)

    typer.echo(json.dumps(line))


@app.command()
def main(file: str, model: str = None, category: str = None):
    """Custom category serialization. Expect jsonl FILE {'npl_publn_id': ddd 'npl_biblio':'sss'}"""
    assert category in LABEL_COLLECTION.keys()

    nlp = spacy.load(model)

    lines = open(file, "r").readlines()
    for i, doc in enumerate(nlp.pipe(yield_npl_biblio(file))):
        line = json.loads(lines[i])
        brewer(doc, line, category)


if __name__ == "__main__":
    app()
