import concurrent.futures
import csv
import json
from glob import glob
from itertools import repeat

import pycld2 as cld2
import typer
from smart_open import open

app = typer.Typer()


@app.command()
def detect_language(
    path: str, max_workers: int = None, id_field: str = None, text_field: str = None
):
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
        typer.secho(f"{json.dumps(out)}")

    def fetch_blob(file, id_field, text_field):
        with open(file, "r") as fin:
            reader = csv.DictReader(fin)
            for row in reader:
                detect_language_from_text(row[id_field], row[text_field])

    files = glob(path)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(fetch_blob, files, repeat(id_field), repeat(text_field))


if __name__ == "__main__":
    app()
