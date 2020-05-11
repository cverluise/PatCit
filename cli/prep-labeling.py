import os
from glob import glob

import pandas as pd
import spacy
import typer


def main(
    path: str,
    sample_size: int = None,
    filter_bibl_ref: bool = False,
    spacy_model: str = None,
):
    """
    Prep GBQ extracts for doccano
    """
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


if __name__ == "__main__":
    typer.run(main)
