import asyncio
import concurrent.futures
import json
import os

import click
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm

from scicit.serialize import fetch_all_tags


# TODO: type checkingn: main issues on volume and page (use jsonschema for example)


async def fetch_batch(npl_publn_id_list, npl_grobid_list):
    tasks = []
    for id, npl in zip(npl_publn_id_list, npl_grobid_list):
        soup = BeautifulSoup(npl, "lxml")
        task = asyncio.create_task(fetch_all_tags(id, soup))
        tasks.append(task)
    batch = await asyncio.gather(*tasks)
    return batch


def serialize(input_file):
    tmp = input_file.split("/")
    output_file = (
        "/".join(tmp[:-1])
        + "/processed_"
        + "."
        + tmp[-1].split(".")[0]
        + ".jsonl"
    )
    output_file = output_file.replace("processed_", "serialized_")
    npl_grobid_list = pd.read_csv(input_file, compression="gzip")[
        "npl_grobid"
    ].tolist()
    npl_publn_id_list = pd.read_csv(input_file, compression="gzip")[
        "npl_publn_id"
    ].tolist()
    by = 1000
    serialized_grobid = []
    for i in tqdm(np.arange(0, len(npl_grobid_list), by)):
        serialized_grobid += asyncio.run(
            fetch_batch(
                npl_publn_id_list[i : i + by], npl_grobid_list[i : i + by]
            )
        )

    with open(output_file, "w") as fout:
        fout.write(
            "\n".join(list(map(lambda x: json.dumps(x), serialized_grobid)))
        )


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
    help="Type of files to be processed. Currently " "supported: 'tls_214'.",
)
@click.option(
    "--max_workers",
    type=int,
    default=5,
    help="Maximum number of threads running in parallel'",
)
def main(path, pattern, flavor, max_workers):
    assert flavor in ["tls214"]
    input_files = [path + file for file in os.listdir(path) if pattern in file]
    with concurrent.futures.ProcessPoolExecutor(
        max_workers=max_workers
    ) as executor:
        executor.map(serialize, input_files)


if __name__ == "__main__":
    main()

# python bin/SerializeCitations.py --path /Volumes/HD_CyrilVerluise/patstat18b/small_chunks/
# --pattern "proc" --flavor "tls214"
