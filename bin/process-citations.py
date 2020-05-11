import concurrent.futures
import os

import click

from patcit.io import process_biblio_tls214, process_full_text


@click.command()
@click.option(
    "--path", type=str, help="Path of folder containing files to be processed"
)
@click.option(
    "--pattern",
    type=str,
    help="Sequence of characters which will be used to filter "
    "files of interest. E.g. 'sub', 'us_'",
)
@click.option(
    "--flavor",
    type=str,
    help="Refers to the type of files to be processed. Currently "
    "supported: 'tls_214' and 'full-text'",
)
@click.option(
    "--max_workers",
    type=int,
    default=10,
    help="Maximum number of threads running in parallel'",
)
@click.option(
    "--consolidate",
    type=int,
    default=1,
    help="Consolidation argument (tls214 only). 0: no consolidation, 1: consolidation against "
    "Crossref, "
    "2: consolidation against Crossref for DOI only",
)
@click.option(
    "--capitalize",
    type=bool,
    default=True,
    help="Capitalize citation (tls214 only), ie .title().",
)
def main(path, pattern, flavor, max_workers, consolidate, capitalize):
    """
    Process all files in <path> (if "<pattern>" in file name).
    MultiThreaded, <max_workers> restricted by nbr of engines supported by grobid service
    :param path: str
    :param pattern: str
    :param flavor: str
    :param max_workers: int
    :param consolidate: int
    :param capitalize: bool
    :return:
    """
    assert flavor in ["tls214", "full-text"]
    input_files = [path + file for file in os.listdir(path) if pattern in file]

    args = ((input_file, consolidate, capitalize) for input_file in input_files)
    if flavor == "tls214":
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(process_biblio_tls214, args)
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(process_full_text, input_files)


if __name__ == "__main__":
    main()
