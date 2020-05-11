import json
import os
import random
from glob import glob

import typer

app = typer.Typer()


@app.command()
def main(path: str, n: int = 400):
    """Sample the files in PATH"""
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


if __name__ == "__main__":
    app()
