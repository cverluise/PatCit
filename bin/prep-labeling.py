import os
from glob import glob

import pandas as pd
import typer


def main(path: str, sample_size: int = None):
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

        df = df.set_index("npl_biblio")
        df.index.name = "text"
        df.to_csv(fout)
        typer.secho(f"{fout} successfully saved.", fg=typer.colors.GREEN)


if __name__ == "__main__":
    typer.run(main)
