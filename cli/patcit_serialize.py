import asyncio
import concurrent.futures
import csv
import json
import os
import sys
from glob import glob

import numpy as np
import pandas as pd
import typer
from bs4 import BeautifulSoup
from jsonschema import validate
from smart_open import open
from tqdm import tqdm

from patcit.issues import eval_issues
from patcit.serialize import contextual_citation
from patcit.serialize.npl_citation import fetch_all_tags
from patcit.validation.npl_citation import solve_issues
from patcit.validation.schema import get_schema
from patcit.validation.shape import prep_and_pop

csv.field_size_limit(sys.maxsize)

app = typer.Typer()


# TODO: add coordinates somewhere in the in_text section
# TODO: relax assumption on file names?
# TODO: fix path. This will break with windows


@app.command()
def front_page(path: str, max_workers: int = None):
    """Serialize front page citations

    Notes: Assume original file names ('processed_' in, 'serialized_' out)"""

    def serialize_fp_file(input_file, batch_size=1000):
        def serialize_prep_validate_fp_cit(x):
            npl_publn_id, npl_grobid = x
            if npl_grobid:
                soup = BeautifulSoup(npl_grobid, "lxml")
                out = asyncio.run(fetch_all_tags(npl_publn_id, soup))

                issues = asyncio.run(eval_issues(out))
                out.update({"issues": issues})
                out = solve_issues(out, issues)
                out = prep_and_pop(out, get_schema("npl"))

                try:
                    validate(instance=out, schema=get_schema("npl"))
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
                serialize_prep_validate_fp_cit, axis=1
            ).to_list()
        np.savetxt(output_file, serialized_grobid, fmt="%s", delimiter="\n")

    files = glob(path)
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        executor.map(serialize_fp_file, files)


async def prep_validate_intext_cits(id_, ccits, flavor):
    """
    Prep and validate a list of contextual citations
    :param id_: str, e.g publication number of the originating patent
    :param ccits: list[bs4.Soup]
    :param flavor: str, in ["npl", "pat"]
    :return: list
    """

    async def prep_validate_intext_cit(id_, ccit, flavor):
        pk = contextual_citation.pk
        pk_type = "string"
        if flavor == "npl":
            ccit = prep_and_pop(ccit, get_schema(flavor, pk, pk_type))
            ccit.update({pk: id_})  # hack to make sure that we preserve UPPER in id_
        try:
            validate(instance=ccit, schema=get_schema(flavor, pk, pk_type))
        except Exception as e:
            ccit = {pk: id_, "exception": str(e), "issues": [0]}
        return json.dumps(ccit)

    assert flavor in ["npl", "pat"]
    tasks = []
    for ccit in ccits:
        task = asyncio.create_task(prep_validate_intext_cit(id_, ccit, flavor))
        tasks.append(task)
    return await asyncio.gather(*tasks)


def serialize_prep_validate_intext_cits(id_, citations):
    """
    Return a list of serialized npls and pats
    :param id_: str, e.g publication number of the originating patent
    :param citations: grobid output
    :return: (list, list), (npls, pats)
    """
    pk = contextual_citation.pk
    soup = BeautifulSoup(citations, "lxml")
    npls, pats = contextual_citation.split_pats_npls(soup)

    if npls:
        npls = asyncio.run(contextual_citation.fetch_npls(id_, npls))
        npls = asyncio.run(prep_validate_intext_cits(id_, npls, "npl"))
    else:
        npls = [json.dumps({pk: id_})]
        # we create an empty entry when there were no detected
        # citations

    if pats:
        pats = asyncio.run(contextual_citation.fetch_patents(id_, pats))
        pats = asyncio.run(prep_validate_intext_cits(id_, pats, "pat"))
    else:
        pats = [json.dumps({pk: id_})]
        # we create an empty entry when there were no detected
        # citations

    return npls, pats


@app.command()
def in_text(path: str, max_workers: int = None):
    """Serialize in-text citations

    Notes: Assume original file names ('processed_' in, 'serialized_' out)"""

    def serialize(input_file):
        root = os.path.dirname(input_file)
        f_name = (os.path.split(input_file)[-1]).split(".")[0]
        # file name w/o format extension
        out_npl_file = os.path.join(
            root, "npl_" + f_name.replace("processed_", "serialized_") + ".jsonl"
        )
        out_pat_file = os.path.join(
            root, "pat_" + f_name.replace("processed_", "serialized_") + ".jsonl"
        )

        with open(input_file, "r") as fin:
            fin_reader = csv.DictReader(
                fin,
                fieldnames=["publication_number", "citation"],
                delimiter=",",
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL,
            )
            line_count = 0
            fout_npls = open(out_npl_file, "w")
            fout_pats = open(out_pat_file, "w")
            for line in tqdm(fin_reader):
                if line_count == 0:  # header
                    pass
                else:
                    npls, pats = serialize_prep_validate_intext_cits(
                        line["publication_number"], line["citation"]
                    )
                    # print(npls)
                    fout_npls.write("\n".join(npls) + "\n")
                    fout_pats.write("\n".join(pats) + "\n")
                line_count += 1
            fout_npls.close()
            fout_pats.close()

    files = glob(path)
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        executor.map(serialize, files)


if __name__ == "__main__":
    app()