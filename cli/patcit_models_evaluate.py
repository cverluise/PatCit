import json
import os

import pandas as pd
import typer
from wasabi import Printer

from patcit.validation.shape import to_int, to_number

msg = Printer()

ATTR_REF_PARSING = ["year", "volume", "issue", "title_main_a", "title_j", "title_m"]


def eval_doi_matching(gold):
    df = pd.read_csv(gold)

    # Restrict to labeled rows
    df = df.dropna(subset=["label"])

    # Focus on eval data
    df_labels = df[["label", "version", "year_discrepancy"]]
    df_labels = df_labels.rename(
        columns={"label": "match_doc", "version": "version_discrepancy"}
    )
    df_labels = df_labels.fillna(0)

    # Export aggregate data
    fout = os.path.join(
        os.path.dirname(gold), gold.split("/")[-1].replace("labels", "eval")
    )
    df_labels.describe().loc[["count", "mean"]].to_csv(fout)
    msg.good(f"{fout} saved")


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


def eval_ref_parsing(gold, pred):
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
    prep_eval_file = prep_gold_file.replace("gold", "eval").replace(".json", ".csv")
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


def main(
    gold: str = typer.Option(default=None, help="File with gold data"),
    pred: str = typer.Option(default=None, help="File with pred data"),
    flavor: str = typer.Option(
        default=None, help="Task, in ['doi_matching','ref_parsing']"
    ),
):
    assert flavor in ["doi_matching", "ref_parsing"]
    if flavor == "doi_matching":
        eval_doi_matching(gold)
    else:
        assert pred
        eval_ref_parsing(gold, pred)


if __name__ == "__main__":
    typer.run(main)
