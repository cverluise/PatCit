import json

import spacy
import typer
from smart_open import open

app = typer.Typer()


def yield_npl_biblio(file):
    with open(file, "r") as fin:
        for line in fin:
            l = json.loads(line)
            yield l["npl_biblio"]


def serialize_database(doc, line=None):
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


CAT_SERIALIZER = {"DATABASE": serialize_database}


@app.command()
def serialize(file: str, model: str = None, category: str = None):
    """Custom category serialization. Expect jsonl FILE {'npl_publn_id': ddd 'npl_biblio':'sss'}"""
    nlp = spacy.load(model)
    assert category in CAT_SERIALIZER.keys()
    serializer = CAT_SERIALIZER[category]
    lines = open(file, "r").readlines()
    for i, doc in enumerate(nlp.pipe(yield_npl_biblio(file))):
        serializer(doc, json.loads(lines[i]))


if __name__ == "__main__":
    app()
