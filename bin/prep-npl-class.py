import os
from glob import glob

import pandas as pd
import spacy
import typer
from tqdm import tqdm
from wasabi import Printer

VAR = ["npl_publn_id", "npl_class"]
msg = Printer()


#  Could certainly do better in terms of efficiency. Still OK -> takes around 4:30 to process
#  the full db


def get_pred_class(doc):
    cats_ = doc.cats
    pred_ = [k for k, v in cats_.items() if v > 0.5]
    out = pred_[0] if pred_ else "Unknown"
    return out


def main(
    path: str,
    spacy_model: str = typer.Option(
        default="models/npl_class/en_core_web_sm_npl-class-ensemble-1.0",
        help="Path to the spaCy model with the 'textcat' pipe",
    ),
    overwrite: bool = False,
):
    """
    Assumes that the input files have the following fields:
        - npl_biblio: raw citation
        - npl_ctype: citation type when already known, nan else
    """
    nlp = spacy.load(spacy_model)
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in ["textcat"]]
    with nlp.disable_pipes(*other_pipes):

        files = glob(path)
        existing_files = glob(
            os.path.join(os.path.dirname(path), "proc_" + path.split("/")[-1])
        )
        msg.info(f"{','.join(existing_files)} already existing. Overwrite: {overwrite}")

        for file in files:
            msg.info(f"START: {file}")
            fout = os.path.join(os.path.dirname(file), "proc_" + file.split("/")[-1])
            if fout in existing_files and not overwrite:
                pass  # we don't overwrite
            else:
                if os.path.isfile(fout):
                    os.remove(fout)  # we overwrite
                header = True
                for chunk in tqdm(pd.read_csv(file, chunksize=1e5)):
                    todo = chunk.query("npl_ctype!=npl_ctype").copy()
                    done = chunk.query("npl_ctype==npl_ctype").copy()
                    msg.info(f"{len(chunk)} rows ({len(done)} rows already assigned)")

                    done["npl_class"] = done["npl_ctype"]

                    npls = todo["npl_biblio"].astype(str).values
                    todo["docs"] = list(nlp.pipe(npls))
                    todo["npl_class"] = todo["docs"].apply(
                        lambda doc: get_pred_class(doc)
                    )

                    todo[VAR].append(done[VAR]).to_csv(
                        fout, index=False, header=header, mode="a"
                    )
                    header = False  # we don't want the header in chunk_n with n>1
            msg.good(f"DONE: {file}")


if __name__ == "__main__":
    typer.run(main)
