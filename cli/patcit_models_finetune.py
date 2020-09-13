import json

import numpy as np
import spacy
import typer
from scipy.stats import gmean
from sklearn.metrics import roc_curve, precision_recall_curve

app = typer.Typer()


@app.command()
def get_best_threshold(
    gold: str,
    model: str,
    label: str = None,
    exante_prec: float = None,
    exante_rec: float = None,
):
    """Return the best threshold based on the (opt. ex-post) f1-score for a given label.

    GOLD is expected to be a spaCy JSON file"""

    nlp = spacy.load(model)

    with open(gold, "r") as golds:
        golds_ = json.loads(golds.read())
        preds = []
        golds = []
        for gold in golds_:
            preds += [nlp(gold["paragraphs"][0]["raw"]).cats[label]]
            golds += [
                d["value"] for d in gold["paragraphs"][0]["cats"] if d["label"] == label
            ]

    if exante_prec and exante_rec:  # used for bibref-cat
        fpr, tpr, thresholds = roc_curve(golds, preds)

        prec = exante_prec * tpr / ((1 - exante_prec) * fpr + exante_prec * tpr)
        rec = exante_rec * tpr
        prec_rec = list(zip(rec, prec))

        f1 = [gmean(pr) for pr in prec_rec]
        best_threshold_idx = np.nanargmax(f1)

    else:
        prec, rec, thresholds = precision_recall_curve(golds, preds)
        prec_rec = list(zip(rec, prec))
        f1 = [gmean(pr) for pr in prec_rec]
        best_threshold_idx = np.nanargmax(f1)

    best_threshold = thresholds[best_threshold_idx]
    best_f1 = f1[best_threshold_idx]
    rec_ = rec[best_threshold_idx]
    prec_ = prec[best_threshold_idx]
    out = {"recall": rec_, "precision": prec_, "f1": best_f1}

    typer.secho(f"Best threshold:{best_threshold}", fg=typer.colors.GREEN)
    typer.echo(
        f"Best threshold based on the {'ex-post' if exante_rec else ''} f1 score.\n"
        f"{json.dumps(out)}"
    )


if __name__ == "__main__":
    app()
