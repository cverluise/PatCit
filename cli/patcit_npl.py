import concurrent.futures
import csv
import json
import os
from glob import glob
from itertools import repeat

import pandas as pd
import pycld2 as cld2
import spacy
import typer
from smart_open import open
from tqdm import tqdm
from wasabi import Printer

msg = Printer()
app = typer.Typer()


@app.command()
def detect_language(
    path: str, max_workers: int = None, id_field: str = None, text_field: str = None
):
    """
    Detect language and return dict to stdout - Supported for front-page only

    Expect a TLS214-like CSV file with id_field and text_field where:
        - id_field: id
        - text_field: raw citation

    E.g. python cli/patcit-cli.py npl detect-language PATH --max-workers 4 --id-field
    "npl_publn_id" --text-field "npl_biblio" > npl_language.jsonl
    """

    def detect_language_from_text(id, text):
        is_reliable, bytes, details = cld2.detect(text)

        language, language_code, percent, score = details[0]
        out = {
            "npl_publn_id": int(id),
            "is_reliable": is_reliable,
            "bytes": bytes,
            "language": language,
            "language_code": language_code,
            "percent": percent,
            "score": score,
        }
        typer.echo(f"{json.dumps(out)}")

    def fetch_blob(file, id_field, text_field):
        with open(file, "r") as fin:
            reader = csv.DictReader(fin)
            for row in reader:
                detect_language_from_text(row[id_field], row[text_field])

    files = glob(path)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(fetch_blob, files, repeat(id_field), repeat(text_field))


@app.command()
def get_category(
    path: str,
    spacy_model: str,
    max_workers: int = None,
    id_field: str = None,
    text_field: str = None,
    cat_field: str = None,
    cat_name: str = None,
    overwrite: bool = False,
):
    """
    Get the NPL category - Supported for front-page only

    Notes:
        Expect a TLS214-like CSV file with id_field, text_field and type_field where:
            --id_field: id
            --text_field: raw citation
            --cat_field: category of the citation if already known
        --cat_field is the name of the category field in the src file while --cat-name is the
        name of the category field in the dest file

    E.g. python cli/patcit-cli.py npl get-category PATH MODEL --max-workers 4 --id-field
    "npl_publn_id" --text-field "npl_biblio"
    """

    def process_file(file, nlp):
        """
        :param file: str
        :param nlp: spacy.lang
        """

        def get_pred_cat(doc):
            """:param doc: spacy.Doc"""
            cats_ = doc.cats
            pred_ = [k for k, v in cats_.items() if v > 0.5]
            out = pred_[0] if pred_ else "Unknown"
            return out

        msg.info(f"START: {file}")
        other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in ["textcat"]]
        fout = os.path.join(os.path.dirname(file), "proc_" + os.path.basename(file))

        with nlp.disable_pipes(*other_pipes):
            if os.path.isfile(fout):
                os.remove(fout)  # we overwrite
            header = True
            for chunk in tqdm(pd.read_csv(file, chunksize=1e5)):
                todo = chunk.query(f"{cat_field}!={cat_field}").copy()
                done = chunk.query(f"{cat_field}=={cat_field}").copy()
                msg.info(f"{len(chunk)} rows ({len(done)} rows already assigned)")

                done[cat_name] = done[cat_field]

                npls = todo[text_field].astype(str).values
                todo["docs"] = list(nlp.pipe(npls))
                todo[cat_name] = todo["docs"].apply(lambda doc: get_pred_cat(doc))

                todo[vars].append(done[vars]).to_csv(
                    fout, index=False, header=header, mode="a"
                )
                header = False  # we don't want the header in chunk_n with n>1
        msg.good(f"DONE: {file}")

    vars = [id_field, cat_name]
    nlp = spacy.load(spacy_model)

    files = glob(path)
    existing_files = glob(os.path.join(os.path.dirname(path), "proc_*"))
    if existing_files:
        msg.warn(
            f"{','.join(existing_files)} already existing. Overwrite value: {overwrite}"
        )
        if not overwrite:  # we keep only files which are not in the proc_ pool
            files = filter(
                lambda x: os.path.join(
                    os.path.dirname(x), "proc_" + os.path.basename(x)
                )
                not in existing_files,
                files,
            )

    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        executor.map(process_file, files, repeat(nlp))


if __name__ == "__main__":
    app()
