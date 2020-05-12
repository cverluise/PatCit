import json
import os
import random
from glob import glob

import pandas as pd
import spacy
import typer
from wasabi import Printer

app = typer.Typer()
msg = Printer()

NPL_LABELS = {
    4: "BIBLIOGRAPHICAL_REFERENCE",
    5: "SEARCH_REPORT",
    6: "OFFICE_ACTION",
    7: "DATABASE",
    8: "WEBPAGE",
    9: "PATENT",
    10: "OTHERS",
    11: "NA",
    12: "PRODUCT_DOCUMENTATION",
    1752: "NORM_STANDARD",
    1773: "LITIGATION",
}

NPL_CATS = [
    cat for cat in list(NPL_LABELS.values()) if cat != "OTHERS"
]  # we skip OTHERS


@app.command()
def sample(path: str, n: int = 400):
    """Sample randomly the files in PATH

    Note: expect the input file(s) to be a JSON file and to have a _lg  suffix. The output file(s)
    have _sm suffix.
    """
    files = glob(path)
    for file in files:
        root, ext = os.path.splitext(file)
        fdest = root.replace("_lg", "") + "_sm" + ext
        with open(fdest, "w") as fout:
            with open(file, "r") as fin:
                lin = json.loads(fin.read())
                if len(lin) < n:
                    typer.secho(
                        f"The input file already contains {len(lin)} objects. No "
                        f"sub-sampling required.",
                        fg=typer.colors.YELLOW,
                    )
                    typer.Exit()
                else:
                    lout = random.choices(lin, k=n)
                    fout.write(json.dumps(lout))
                    typer.secho(f"{fdest}", fg=typer.colors.GREEN)


@app.command()
def prep_textcat4doccano(
    path: str,
    sample_size: int = None,
    filter_bibl_ref: bool = False,
    spacy_model: str = None,
):
    """Prep GBQ extracts for doccano"""
    files = glob(path)
    for file in files:
        fout = os.path.join(os.path.dirname(file), f"prep-{os.path.basename(file)}")
        df = pd.read_csv(file, index_col=0)
        if sample_size is not None:
            df = df.sample(sample_size)["npl_biblio"].to_frame()
            fout = os.path.join(
                os.path.dirname(file), f"sample-prep-{os.path.basename(file)}"
            )
        if filter_bibl_ref:
            # we filter out non bibliographical ref npls - based on spacy_model textcat
            fout = fout.replace(".csv", ".txt")
            nlp = spacy.load(spacy_model)
            texts = df["npl_biblio"].values
            docs = list(nlp.pipe(texts))
            cats = [doc.cats for doc in docs]
            bibl_ref = [
                True if cat["BIBLIOGRAPHICAL_REFERENCE"] > 0.5 else False
                for cat in cats
            ]
            df.loc[bibl_ref]["npl_biblio"].to_string(fout, index=False, header=False)
        else:
            df = df.set_index("npl_biblio")
            df.index.name = "text"
            df.to_csv(fout)
        typer.secho(f"{fout} successfully saved.", fg=typer.colors.GREEN)


@app.command()
def prep_doccano4spacy(path: str, train_share: float = 0.8):
    """
    Boiler-plate to prepare Doccano npl-cat data for spaCy multi-class textCategorizer training

    Notes:
        - Expect a CSV file with a text and label field
        - See dicussion here https://github.com/explosion/spaCy/issues/1997
        - Output train_texts.json, train_cats.json, dev_texts.json, dev_gold.json in dir(PATH)
    """

    def load_data(path):
        files = glob(path)

        l = []
        for file in files:
            tmp = pd.read_csv(file).reset_index()
            tmp["label"] = tmp["label"].apply(lambda x: NPL_LABELS[x])
            l.append(tmp)
        df = pd.concat(l, axis=0, ignore_index=True)
        df = df.drop("index", axis=1)
        print(df.groupby("label").count().sort_values("text", ascending=False)["text"])
        tmp = df.query("label not in ['OTHERS']")
        msg.info(title=f"Loaded data: {len(tmp)} rows (excl 'OTHERS')")
        return df

    def dump_data(path, data):
        """data (train_texts, train_cats, dev_texts, dev_gold)"""
        out_dir = os.path.dirname(path)

        for name, dat in list(
            zip(["train_texts", "train_cats", "dev_texts", "dev_gold"], data)
        ):
            file = os.path.join(out_dir, name + ".json")
            with open(file, "w") as fout:
                fout.write(json.dumps(dat))
                typer.secho(f"{file}", fg=typer.colors.GREEN)

    df = load_data(path)
    tmp = df.query("label not in ['OTHERS']")
    tmp = tmp.sample(frac=1, random_state=42)  # shuffle

    n = int(len(tmp) * train_share)

    texts = tmp["text"].values.tolist()
    gold = tmp["label"].values.tolist()

    cats = [{k: False for k in NPL_CATS} for _ in range(len(gold))]
    for i in range(len(gold)):
        cats[i].update({gold[i]: True})

    # We format the cats as
    # {'BIBLIOGRAPHICAL_REFERENCE':False, 'SEARCH_REPORT': False, 'OFFICE_ACTION': True, ...}
    # where the value True is the gold label. Nb, gold is a list of the gold labels
    # ['OFFICE_ACTION', ..]
    # see discussion here https://github.com/explosion/spaCy/issues/1997
    train_texts = texts[:n]
    dev_texts = texts[n:]
    train_cats = cats[:n]
    dev_gold = gold[n:]

    msg.info(f"{n} training samples and {len(tmp) - n} dev samples.")

    dump_data(path, (train_texts, train_cats, dev_texts, dev_gold))
    # return train_texts, train_cats, dev_texts, dev_gold


if __name__ == "__main__":
    app()