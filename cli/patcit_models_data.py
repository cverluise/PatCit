import asyncio
import csv
import json
import os
import random
import re
import sys
from glob import glob

import numpy as np
import pandas as pd
import spacy
import typer
from bs4 import BeautifulSoup
from fuzzysearch import find_near_matches
from smart_open import open
from wasabi import Printer

from patcit.serialize import contextual_citation

app = typer.Typer()
msg = Printer()
csv.field_size_limit(sys.maxsize)

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


def prep_spacy_sam_patents(texts_file: str = None, citations_file: str = None):
    def prep_citations_spans(citations_file):
        with open(citations_file, "r") as fin:

            def get_text_span(patent):
                # TODO -> move to contextual_citation.fetch_patent
                span = patent.find("ptr")["target"].replace("#string-range", "")
                _, start, length = span.split(",")
                length = length.replace(")", "")
                start, end = (int(start), int(start) + int(length))
                return start, end

            reader = csv.DictReader(fin, fieldnames=["publication_number", "citations"])
            out = {}
            for l in reader:
                soup = BeautifulSoup(l["citations"], features="lxml")
                patents = soup.find_all("biblstruct", {"type": "patent"})
                spans = []
                for patent in patents:
                    start, end = get_text_span(patent)
                    span = asyncio.run(
                        contextual_citation.fetch_patent(
                            l["publication_number"], patent
                        )
                    )
                    span.update({"start": start, "end": end, "label": "PATENT"})

                    spans += [span]
                out.update({l["publication_number"]: spans})
            return out

    citations_span = prep_citations_spans(citations_file)
    with open(texts_file, "r") as fin:
        reader = csv.DictReader(fin, fieldnames=["publication_number", "text"])
        for l in reader:
            sam = {
                "publication_number": l["publication_number"],
                "text": l["text"],
                "spans": citations_span[l["publication_number"]],
            }
            typer.echo(json.dumps(sam))


def prep_spacy_sam_bibrefs(
    texts_file: str = None, citations_file: str = None, max_l_dist: int = 3
):
    citations = list(
        csv.DictReader(
            open(citations_file, "r"), fieldnames=["publication_number", "citations"]
        )
    )
    texts = list(
        csv.DictReader(open(texts_file, "r"), fieldnames=["publication_number", "text"])
    )

    stdize = lambda s: re.sub(" +", " ", s.replace("\n", "").replace("&amp;", "&"))
    # boilerplate to stdize texts "encoding" reported in raw_reference and the src text

    missed = []
    for i in range(len(citations)):
        if i == 0:
            pass  # handle header
        else:
            assert citations[i]["publication_number"] == texts[i]["publication_number"]

            # populate src objects
            citations_ = citations[i]["citations"]
            text_ = texts[i]["text"]
            sam = {"publication_number": citations[i]["publication_number"]}

            soup = BeautifulSoup(citations_, features="lxml")
            bibrefs, _ = contextual_citation.split_pats_npls(soup)

            spans = []
            for bibref in bibrefs:
                bibref_ = stdize(bibref.find("note", {"type": "raw_reference"}).text)
                text_ = stdize(text_)
                match = find_near_matches(bibref_, text_, max_l_dist=max_l_dist)
                if bibref_ and not match:
                    missed += [bibref_]
                if match:
                    start, end = match[0].start, match[0].end
                    spans += [{"start": start, "end": end, "label": "BIBREF"}]
            sam.update({"text": text_, "spans": spans})
            typer.echo(json.dumps(sam))
    typer.echo(
        json.dumps(
            {"text": "", "missed": missed, "spans": [], "nb_missed": len(missed)}
        )
    )


@app.command()
def prep_spacy_sam(
    texts_file: str = None, citations_file: str = None, flavor: str = "patents"
):
    """Prep spaCy Simple Annotation Model from Grobid citations annotation

    Expect 2 csv files
    - texts_file: publication_number, text
    - citations_file: publication_number, grobid_citations

    Nb: bibrefs requires raw_reference (not default)
    """
    assert flavor in ["patents", "bibrefs"]
    if flavor == "patents":
        prep_spacy_sam_patents(texts_file, citations_file)
    else:
        prep_spacy_sam_bibrefs(texts_file, citations_file)


def align_spans_(sam, nlp):
    # TODO implement tests
    def remove_space(start, end, text):
        label_span = text[start:end]
        tmp = label_span.lstrip()
        start = start + (len(label_span) - len(tmp))
        tmp = label_span.rstrip()
        end = end - (len(label_span) - len(tmp))
        return start, end

    tmp = sam.copy()

    tokens = nlp(tmp["text"]).to_json()["tokens"]
    spacy_starts = np.array([tok["start"] for tok in tokens])
    spacy_ends = np.array([tok["end"] for tok in tokens])
    text = tmp["text"]

    spans = []
    for span in tmp["spans"]:
        start, end = (span["start"], span["end"])
        start, end = remove_space(start, end, text)

        center_starts = start - spacy_starts
        i_start = np.where(
            center_starts == np.min(list(filter(lambda x: x >= 0, center_starts)))
        )[0][0]
        center_ends = spacy_ends - end
        i_end = np.where(
            center_ends == np.min(list(filter(lambda x: x >= 0, center_ends)))
        )[0][0]
        start_aligned = int(spacy_starts[i_start])
        end_aligned = int(spacy_ends[i_end])

        span.update(
            {
                "start": start_aligned,
                "end": end_aligned,
                "label": span["label"],
                "start_o": start,
                "end_o": end,
            }
        )

        spans += [span]
    return spans


def contextualize_spans_(sam, nlp, context_window=10, attr=None):
    tmp = sam.copy()
    text = tmp["text"]
    tokens = nlp(tmp["text"]).to_json()["tokens"]
    spacy_starts = np.array([tok["start"] for tok in tokens])
    spacy_ends = np.array([tok["end"] for tok in tokens])
    for span in tmp["spans"]:
        span_ = span.copy()
        i_start = max(
            np.where(span_["start"] == spacy_starts)[0][0] - context_window, 0
        )
        i_end = min(
            np.where(span_["end"] == spacy_ends)[0][0] + context_window, len(spacy_ends)
        )

        context_start = int(spacy_starts[i_start])
        context_end = int(spacy_ends[i_end])

        out = {"text": text[context_start:context_end].replace("\n", "")}
        span_.update(
            {
                "start": span_["start"] - context_start,
                "end": span_["end"] - context_start,
            }
        )

        assert span_["start"] in list(map(int, spacy_starts - context_start))
        assert span_["end"] in list(map(int, spacy_ends - context_start))

        out.update({"spans": [span_]})
        if attr:
            out.update({"label": span_[attr]})
        typer.echo(json.dumps(out))


@app.command()
def align_spans(file: str, model: str = "en"):
    """Align spans with MODEL tokenizer. Required for prodigy

    Expect a jsonl file where each line is consistent with spaCy Simple Annotation Model (SAM)"""
    with open(file, "r") as fin:
        if len(model) == 2:
            nlp = spacy.blank(model)
        else:
            nlp = spacy.load(model)

        for line in fin:
            sam = json.loads(line)
            aligned_spans = align_spans_(sam, nlp)
            sam.update({"spans": aligned_spans})
            typer.echo(json.dumps(sam))


@app.command()
def report_alignment(file: str, context_window: int = 10):
    """Prepare alignment report

    Expect output from align-spans as input"""
    typer.echo(f"Aligned|Orig Span|Aligned Span")
    typer.echo(f"---|---|---")
    with open(file, "r") as fin:
        for line in fin:
            sam = json.loads(line)
            text = sam["text"]
            spans = sam["spans"]
            for span in spans:
                label = span["label"]
                start_o, end_o = (span["start_o"], span["end_o"])
                start, end = (span["start"], span["end"])
                before_, after_ = (start - context_window, end + context_window)
                contextualized_span_o = (
                    text[before_:start_o]
                    + "`"
                    + text[start_o:end_o]
                    + f" {label}`"
                    + text[end_o:after_]
                ).replace("\n", "")
                contextualized_span = (
                    text[before_:start]
                    + "`"
                    + text[start:end]
                    + f" {label}`"
                    + text[end:after_]
                ).replace("\n", "")
                aligned = start != start_o or end != end_o
                typer.echo(f"{aligned}|{contextualized_span_o}|{contextualized_span}")


@app.command()
def contextualize_spans(file: str, model: str = "en", attr: str = None):
    """Contextualize spans

    Expect jsonl with Simple Annotation Model lines
    Return one json object by span to stdout"""
    if len(model) == 2:
        nlp = spacy.blank(model)
    else:
        nlp = spacy.load(model)
    with open(file, "r") as fin:
        for line in fin:
            sam = json.loads(line)
            contextualize_spans_(sam, nlp, attr=attr)


if __name__ == "__main__":
    app()
