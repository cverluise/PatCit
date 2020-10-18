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
    "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
)


def yield_npl_biblio(file):
    with open(file, "r") as fin:
        for line in fin:
            l = json.loads(line)
            out = l.get("npl_biblio")
            if not out:
                out = l.get("text")
            yield out


def brew_date(date: list):
    print(date)
    date = [parse_date(date_) for date_ in date]
    date = list(set(filter(lambda x: x, date)))
    return date


def brew_url_components(doc):
    urls = re.findall(URL_EXPRESSION, doc.text)
    hostnames = [urlparse(url).hostname for url in urls]
    return urls, hostnames


def brewer(doc, line, category):
    labels = LABEL_COLLECTION[category]
    out = {}

    ents = doc.ents

    # Collect labels in general
    for label in labels:
        out.update({label.lower(): [ent.text for ent in ents if ent.label_ == label]})

    # Parse dates as yyyymmdd int
    if out.get("date"):
        date = brew_date(out.get("date"))
        out.update({"date": date})

    # Collect urls
    urls, hostnames = brew_url_components(doc)
    out.update({"url": urls, "hostnames": hostnames})

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
