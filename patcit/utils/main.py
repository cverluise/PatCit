import json
import lzma
from glob import glob
from pprint import pprint

import pandas as pd
import smart_open
import typer
from tqdm import tqdm

ORDERED_VAR = ["table", "name", "description", "type"]
TEXTTT_VAR = ["table", "name"]

app = typer.Typer()


@app.command()
def sniff(path: str, tar: bool = True, examples: bool = False, break_after: int = None):
    """Print the schema of a JSON file to stdout

    Notes:
        --tar: for .xz files
        --examples/--no-examples: report example for each var
        --break-after: number of iterations after which sniffing stops
    """
    key_val = {}
    i = 0
    for file in tqdm(glob(path)):
        if tar:
            _open = lzma.open
        else:
            _open = smart_open.open
        with _open(file) as f:
            for l in tqdm(f):
                i += 1
                for k, v in json.loads(l).items():
                    if k in key_val.keys():
                        if examples:
                            key_val.update(
                                {k: (key_val[k][0] + 1, key_val[k][1], key_val[k][2])}
                            )
                        else:
                            key_val.update({k: (key_val[k][0] + 1, key_val[k][1])})
                    else:
                        if examples:
                            key_val.update({k: (1, type(v), v)})
                        else:
                            key_val.update({k: (1, type(v))})
                if break_after:
                    if i > break_after:
                        break

    pprint(key_val)


@app.command()
def json2md(file: str):
    """Transform a Json schema to Markdown - Copy to clip-board"""
    to_texttt = lambda x: "`" + x + "`"
    df = pd.read_json(file)
    table = True if "fields" in df.columns else False

    if table:
        df["table"] = "bibl"

        for name, field in df[["name", "fields"]].query("fields==fields").values:
            tmp = pd.DataFrame.from_dict(field)
            tmp["table"] = name
            df = df.append(tmp, sort=False)

        df = df[df["fields"].isna()]
    # df = df.drop(["mode", "fields"], axis=1)

    if not table:
        ORDERED_VAR.remove("table")
        TEXTTT_VAR.remove("table")

    df = df[ORDERED_VAR]
    for var in TEXTTT_VAR:
        df[var] = df[var].apply(to_texttt)

    typer.echo(f"{df.set_index(ORDERED_VAR[0])}")
    # typer.secho(message="Table (.md) copied to clip-board", fg=typer.colors.BLUE)


if __name__ == "__main__":
    app()
