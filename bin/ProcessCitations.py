import concurrent.futures
import os

import click

from pnpl.io import process_biblio_tls214


@click.command()
@click.argument("path", required=False, type=str)
def main(path):
    """
    Process all files in <path> (if "sub" in file name).
    MultiThreaded, max_workers=10 (restricted by nbr of engines supported by grobid service)
    :param path: str
    :return:
    """
    input_files = [path + file for file in os.listdir(path) if "sub" in file]

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(process_biblio_tls214, input_files)


if __name__ == "__main__":
    main()
