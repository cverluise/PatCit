import concurrent.futures
from glob import glob

import typer

from patcit.grobid.io import process_biblio_tls214, process_full_text

app = typer.Typer()


# TODO test multiprocessing


@app.command()
def main(path: str, max_workers: int = None, flavor: str = None):
    """
    Python wrapper for grobid - Multithreaded

    Notes:
        --max-workers: restricted by nbr of engines supported by grobid service (i.e. 10)
        --flavor: "front-page" (leg tls214) or "in-text" (leg full-text)
    """
    assert flavor in ["tls214", "full-text"]
    input_files = glob(path)

    if flavor == "tls214":
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(process_biblio_tls214, input_files)
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(process_full_text, input_files)


if __name__ == "__main__":
    app()
