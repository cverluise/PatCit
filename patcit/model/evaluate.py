import json
import os
from collections import Counter

import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import spacy
import typer
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support
from wasabi import Printer

from patcit.validation.typing import to_int, to_number

msg = Printer()
app = typer.Typer()

ATTR_REF_PARSING = ["year", "volume", "issue", "title_main_a", "title_j", "title_m"]

app.command()


@app.command()
def matching_doi(gold):
    """Compute the performance metrics for the DOIs matched by Grobid/biblio-glutton based on a
    hand-labelled GOLD dataset"""
    df = pd.read_csv(gold)

    # Restrict to labeled rows
    df = df.dropna(subset=["label"])

    # Focus on eval data
    df_labels = df[["label", "version", "year_discrepancy"]]
    df_labels = df_labels.rename(
        columns={"label": "match_doc", "version": "version_discrepancy"}
    )
    df_labels = df_labels.fillna(0)

    typer.echo(df_labels.describe().loc[["count", "mean"]].to_markdown())


@app.command()
def parsing_bibref(gold, pred):
    """Compute performance metrics for Grobid PRED parsing compared to hand annotated GOLD
    dataset.

    Note: Binary measure of performance (conservative). Once sequences have been aligned,
    partial span matching is not accepted """

    def prep_gold_ref_parsing(file):
        """:param file: jsonl extract from doccano sequence labeling task"""
        df = pd.read_json(file, lines=True)

        # restrict to labeled data
        df["nb_labels"] = df["labels"].apply(lambda x: len(x))
        df = df.query("nb_labels>0").copy()
        df = df.drop("nb_labels", axis=1)

        # get texts and labels objects
        texts = df["text"].values
        labels = df["labels"].values

        # format and write gold in table style (flat json)
        fout = os.path.join(os.path.dirname(file), "prep-" + file.split("/")[-1])
        with open(fout, "w+") as fout_:

            for text, label in list(zip(texts, labels)):
                out = {"npl_biblio": text}
                for start, end, tag in label:
                    out.update({tag: text[start:end]})
                    # {"npl_biblio":"...", "title_j":"...", "issue": "...", ...}
                fout_.write(json.dumps(out) + "\n")

        msg.good(f"Gold prepared for evaluation. Saved as {fout}")
        return fout

    def get_bool(x):
        """
        Return True if the 2 are the same, else False
        :param x: (gold, pred)
        """
        gold, pred = x

        # make sure that formats are the same
        gold = str(gold).lower().strip().rstrip(".")
        pred = str(pred).lower().strip().rstrip(".")

        if gold == pred:
            out = True
        else:
            out = False
        return out

    # pred
    df_pred = pd.read_csv(pred)

    # prep and load gold
    prep_gold_file = prep_gold_ref_parsing(gold)
    df_gold = pd.read_json(prep_gold_file, lines=True)

    # prep fields for comparability, same shaping as in serialize-citations.py
    df_gold["year"] = df_gold["year"].apply(lambda x: to_int(to_number(x)))
    for var in ["volume", "issue"]:
        df_gold[var] = df_gold[var].apply(lambda x: to_int(x))
    df_gold = df_gold.rename(columns={"title_a": "title_main_a"})

    # rename gold labels
    df_gold.columns = [df_gold.columns[0]] + list("gold_" + df_gold.columns[1:])

    # align
    df_eval = pd.merge(df_gold, df_pred, on="npl_biblio")

    # compute True/False
    for attr in ATTR_REF_PARSING:
        df_eval[f"eval_{attr}"] = df_eval[[f"gold_{attr}", f"{attr}"]].apply(
            get_bool, axis=1
        )
    df_eval = df_eval.reindex(sorted(df_eval.columns), axis=1)

    # save intermediary
    prep_eval_file = prep_gold_file.replace("gold", "eval").replace(".jsonl", ".csv")
    df_eval.to_csv(prep_eval_file, index=False)
    msg.good(f"Successfully saved {prep_eval_file}")

    # nb True/False by attr (w and wo na)
    res_df = pd.DataFrame(data=[True, False], columns=["index"])
    for attr in ATTR_REF_PARSING:
        tmp_wna = (
            df_eval.groupby(f"eval_{attr}")
            .count()
            .max(1)
            .rename(f"{attr}_wna")
            .to_frame()
        )
        tmp_wona = (
            df_eval.query(f"gold_{attr}==gold_{attr}")
            .groupby(f"eval_{attr}")
            .count()
            .max(1)
            .rename(f"{attr}_wona")
            .to_frame()
        )
        tmp = pd.merge(tmp_wna, tmp_wona, right_index=True, left_index=True)
        tmp.index.name = "index"
        tmp = tmp.reset_index()
        res_df = pd.merge(res_df, tmp, on="index")
    res_df = res_df.set_index("index")

    # compute accuracy
    tmp = res_df.T
    tmp["Accuracy"] = tmp[True] / (tmp[True] + tmp[False])
    res_df = tmp.round(2)

    # save
    eval_file = prep_eval_file.replace("prep-", "")
    res_df.to_csv(eval_file)
    msg.good(f"Successfully saved {eval_file}")


# TODO: deprecate in favor of spaCy.Scorer


@app.command(deprecated=True)
def textcat(
    gold: str,
    texts: str,
    model: str = typer.Option(
        None, help="spaCy model with the textcat pipeline to be tested"
    ),
    save_dir: str = typer.Option(None, help="Directory for saving performance metrics"),
):
    """
    Save a series of evaluation objects (confusion matrix, multi-class
    precision-recall-f1-support, average accuracy-precision-recall-f1) to --save-dir

    Note: Expect GOLD and TEXTS to be JSON files with a list of cats and a list of texts resp.
    The --model predictions are compared to GOLD.
    """

    def load_data(file):
        with open(file, "r") as fin:
            return json.loads(fin.read())

    def get_pred(dev_texts, nlp, threshold=0.5):
        """
        Return the predicted labels for the texts in dev_texts
        :param dev_texts: ["3GPP, Third Generation...", "US Application ...."]
        """

        def clip_score(score, threshold=0.5):
            bool = True if score > threshold else False
            return bool

        # TODO: use nlp.pipe
        pred = []
        for text in dev_texts:
            doc = nlp(text)
            pred_cats = {k: clip_score(v, threshold) for k, v in doc.cats.items()}
            pred_cat = [k for k, v in pred_cats.items() if v]
            # TODO: report score
            pred += pred_cat if pred_cat else ["None"]
        return pred

    def plot_confusion(confusion_matrix, labels, file):
        """
        Wrapper for plotly ff.create_annotated_heatmap
        """
        fig = ff.create_annotated_heatmap(
            z=np.matrix.round(confusion_matrix, 1),
            x=labels,
            y=labels,
            colorscale="RdBu",
            reversescale=True,
            font_colors=["white", "black"],
        )
        fig.write_image(file)

    gold = load_data(gold)
    texts = load_data(texts)

    nlp = spacy.load(model)
    pred = get_pred(texts, nlp)

    cats_ = set(gold) | set(pred)

    for normalize in ["pred", "true", None]:
        file = os.path.join(
            save_dir, f"confusion{'_norm-' + normalize if normalize else ''}.png"
        )
        confusion_norm = np.matrix.round(
            confusion_matrix(gold, pred, labels=cats_, normalize=normalize), 2
        )
        plot_confusion(confusion_norm, cats_, file)
        msg.good(f"{file} saved")

    # Multiclass precision recall f1 support
    multi_prfs = precision_recall_fscore_support(gold, pred, labels=cats_)
    df_multi_prfs = pd.DataFrame(
        multi_prfs, columns=cats_, index=["precision", "recall", "f1", "support"]
    ).round(decimals=2)
    file = os.path.join(save_dir, f"multi_prfs.csv")
    df_multi_prfs.to_csv(file)
    msg.good(f"{file} saved")

    # Average accuracy precision recall f1
    file = os.path.join(save_dir, f"aprf.csv")
    confusion = confusion_matrix(gold, pred, labels=cats_)
    accuracy = sum([confusion[i, i] for i in range(len(confusion))]) / np.sum(confusion)
    prfs = precision_recall_fscore_support(gold, pred, labels=cats_, average="weighted")
    aprf = [accuracy] + list(prfs[:-1])
    df_aprf = pd.DataFrame(data=aprf, index=["accuracy", "precision", "recall", "f1"]).T
    df_aprf.to_csv(file, index=False)
    msg.good(f"{file} saved")


@app.command()
def spacy_model(model: str, pipes: str = "ner"):
    """Evaluate model"""

    scores = json.loads(open(os.path.join(model, "meta.json"), "r").read())["accuracy"]

    pipes = pipes.split(",")
    if "ner" in pipes:
        p, r, f = scores["ents_p"], scores["ents_r"], scores["ents_f"]
        typer.secho("NER Scores", fg=typer.colors.BLUE)
        typer.secho(
            f"{pd.DataFrame.from_dict(scores['ents_per_type']).T.round(2).to_markdown()}"
        )
        typer.echo("-" * 37)
        typer.echo(f"ALL   %.2f  %.2f  %.2f" % (p, r, f))

    if "textcat" in pipes:
        f = scores["textcat_score"]
        typer.secho("Textcat scores", fg=typer.colors.BLUE)
        typer.secho(
            f""
            f"{pd.DataFrame.from_dict(scores['textcats_per_cat']).T.round(2).to_markdown()}"
        )
        typer.echo("-" * 37)
        typer.echo(f"ALL   %.2f" % (f))


@app.command()
def grobid_intext(pred: str, gold: str, leniency: int = 0):
    """Evaluate grobid predictions for in-text citations (BIBREF and PATENTS)."""

    def get_index(file: str, key: str = "publication_number", value: str = "spans"):
        """Return an index {publication_number: spans} from a jsonl where each line is as follows
         {'publication_number':publication_number, 'spans': spans}"""

        index = {}
        with open(file, "r") as lines:
            for line in lines:
                line = json.loads(line)
                key_ = line[key]  # e.g. key_ "US-1234-A"
                if index.get(
                    key_
                ):  # in case there are more than 1 line with a given key
                    index[key_] = index[key_] + line[value]
                else:
                    index.update({key_: line[value]})

            index = {
                k: list(set([(v["start"], v["end"]) for v in vals]))
                for k, vals in index.items()
            }
        return index

    def has_sibling(dot, arr, leniency):
        """Return a boolean with value True if there is 'at least' 1 element of arr which distance
        wrt to dot is less than leniency. Dist is defined by sum(abs((dot[0]-arr_[0], dot[1]-arr_[
        1]))). Else False. """
        is_sibling = list(map(lambda a: sum(np.abs(dot - a)) <= leniency, arr))
        return any(is_sibling)

    gold_index = get_index(gold)
    pred_index = {k: v for k, v in get_index(pred).items() if k in gold_index.keys()}
    # we restrict the pred_index to the keys of the docs which were actually hand-labelled
    # ie the keys which can be found in gold_index

    pos_types = []
    for k, golds in gold_index.items():
        preds = pred_index[k]
        for pred_ in preds:  # true/false positives
            pos_types += [has_sibling(np.array(pred_), np.array(golds), leniency)]

    pos_types = Counter(pos_types)  # Now of the form {True:int, False:int}

    n_preds = sum(list(map(lambda x: len(x), pred_index.values())))
    n_golds = sum(list(map(lambda x: len(x), gold_index.values())))

    precision = pos_types[True] / (pos_types[True] + pos_types[False])
    recall = pos_types[True] / n_golds  # nb golds is the number of actual positives

    out = {
        "n_keys": len(gold_index.keys()),
        "n_preds": n_preds,
        "n_golds": n_golds,
        "true_positives": pos_types[True],
        "false_positives": pos_types[False],
        "false_negatives": n_golds - pos_types[True],
        "precision": precision,
        "recall": recall,
        "leniency": leniency,
    }

    res = pd.DataFrame.from_dict(out, orient="index")
    res.to_clipboard()

    typer.secho(res.T.to_string(), fg=typer.colors.BLUE)
    typer.secho(f"Results copied to clipboard!", fg=typer.colors.YELLOW)


if __name__ == "__main__":
    app()
