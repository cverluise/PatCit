import os

import pandas as pd
import typer
from wasabi import Printer

msg = Printer()


def eval_doi_matching(file):
    df = pd.read_csv(file)

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
        os.path.dirname(file), file.split("/")[-1].replace("labels", "eval")
    )
    df_labels.describe().loc[["count", "mean"]].to_csv(fout)
    msg.good(f"{fout} saved")


def main(file: str, flavor: str):
    assert flavor in ["doi_matching", "ref_parsing"]
    if flavor == "doi_matching":
        eval_doi_matching(file)
    else:
        pass


if __name__ == "__main__":
    typer.run(main)
