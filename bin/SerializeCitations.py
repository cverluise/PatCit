import asyncio
import concurrent.futures
import glob

import click
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from jsonschema import validate
import json
from tqdm import tqdm

from scicit.issues import eval_issues
from scicit.serialize.npl_citation import fetch_all_tags
from scicit.validation.npl_citation import solve_issues
from scicit.validation.schema import npl_citation_schema
from scicit.validation.shape import prep_and_pop


def serialize_prep_validate_npl(x):
    npl_publn_id, npl_grobid = x
    if npl_grobid:
        soup = BeautifulSoup(npl_grobid, "lxml")
        out = asyncio.run(fetch_all_tags(npl_publn_id, soup))

        issues = asyncio.run(eval_issues(out))
        out.update({"issues": issues})
        out = solve_issues(out, issues)
        out = prep_and_pop(out, npl_citation_schema)

        try:
            validate(instance=out, schema=npl_citation_schema)
        except Exception as e:
            out = {
                "npl_publn_id": out["npl_publn_id"],
                "exception": str(e),
                "issues": [0],
            }
    else:
        out = {
            "npl_publn_id": npl_publn_id,
            "exception": "GrobidException",
            "issues": [0],
        }
    return json.dumps(out)


def serialize(input_file, batch_size=1000):
    tmp = input_file.split("/")
    output_file = "/".join(tmp[:-1]) + "/" + tmp[-1].split(".")[0] + ".jsonl"
    output_file = output_file.replace("processed_", "serialized_")
    data = pd.read_csv(input_file, compression="gzip")[
        ["npl_publn_id", "npl_grobid"]
    ]

    serialized_grobid = []
    for i in tqdm(np.arange(0, len(data), batch_size)):
        tmp = data.iloc[i : i + batch_size]
        serialized_grobid += tmp.apply(
            serialize_prep_validate_npl, axis=1
        ).to_list()
    np.savetxt(output_file, serialized_grobid, fmt="%s", delimiter="\n")


if __name__ == "__main__":

    @click.command()
    @click.option(
        "--path", type=str, help="File or folder path. Wildcard '*' enabled"
    )
    @click.option(
        "--flavor",
        type=str,
        help="Type of files to be processed. Currently "
        "supported: 'tls_214'.",
    )
    @click.option(
        "--max_workers",
        type=int,
        default=5,
        help="Maximum number of threads running in parallel'",
    )
    def main(path, flavor, max_workers):
        assert flavor in ["tls214"]
        files = glob.glob(path)
        with concurrent.futures.ProcessPoolExecutor(
            max_workers=max_workers
        ) as executor:
            executor.map(serialize, files)

    main()

# python bin/SerializeCitations.py --path /Volumes/HD_CyrilVerluise/patstat18b/small_chunks/
# --pattern "proc" --flavor "tls214"
