import os

import pandas as pd
import pyperclip
import typer

ORDERED_VAR = ["table", "name", "description", "type"]
TEXTTT_VAR = ["table", "name"]
to_texttt = lambda x: "`" + x + "`"


def main(json_schema_file: str):
    if not os.path.isfile(json_schema_file):
        typer.echo(f"{json_schema_file} does not seem to exist.")
        raise typer.Abort()

    df = pd.read_json(json_schema_file)
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

    pyperclip.copy(df.set_index(ORDERED_VAR[0]).to_markdown())
    typer.secho(message="Table (.md) copied to clip-board", fg=typer.colors.BLUE)


if __name__ == "__main__":
    typer.run(main)
