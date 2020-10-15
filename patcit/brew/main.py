import json

import spacy
import typer
from smart_open import open
from spacy.language import Language

from patcit.model.add_component import UrlsMatcher, UrlsHostname
from patcit.utils.tools import parse_date

app = typer.Typer()


def yield_npl_biblio(file):
    with open(file, "r") as fin:
        for line in fin:
            l = json.loads(line)
            out = l.get("npl_biblio")
            if not out:
                out = l.get("text")
            yield out


def brew_database(doc, line=None):
    # TODO add date parsing -> or should it be a custom pipeline?
    labels = ["NAME", "DATE", "ACC_NUM"]
    out = {}
    ents = doc.ents
    for label in labels:
        out.update({label.lower(): [ent.text for ent in ents if ent.label_ == label]})
    out.update({"url": [tok.text for tok in doc if tok.like_url]})
    if line:
        out.update(line)
        # assert out["npl_biblio"] == doc.text
    typer.echo(json.dumps(out))


def brew_wiki(doc, line=None):
    labels = ["DATE", "ITEM"]
    out = {}
    ents = doc.ents
    for label in labels:
        out.update({label.lower(): [ent.text for ent in ents if ent.label_ == label]})
    date_ = []
    for date in out["date"]:
        date_ += [parse_date(date)]
    out.update({"date_num": date_})

    out.update({"url": doc._.urls})
    out.update({"hostname": doc._.hostnames})

    if line:
        out.update(line)
    typer.echo(json.dumps(out))


CAT_SERIALIZER = {"DATABASE": brew_database, "WIKI": brew_wiki}


@app.command()
def main(file: str, model: str = None, category: str = None):
    """Custom category serialization. Expect jsonl FILE {'npl_publn_id': ddd 'npl_biblio':'sss'}"""
    assert category in CAT_SERIALIZER.keys()
    if category == "WIKI":
        Language.factories["urls_matcher"] = lambda nlp, **cfg: UrlsMatcher(nlp, **cfg)
        Language.factories["urls_hostname"] = lambda nlp, **cfg: UrlsHostname(
            nlp, **cfg
        )
    nlp = spacy.load(model)

    serializer = CAT_SERIALIZER[category]
    lines = open(file, "r").readlines()
    for i, doc in enumerate(nlp.pipe(yield_npl_biblio(file))):
        serializer(doc, json.loads(lines[i]))


if __name__ == "__main__":
    app()
