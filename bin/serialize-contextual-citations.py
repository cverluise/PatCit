import asyncio
import concurrent.futures
import csv
import json
import os
import sys
from glob import glob

import click
from bs4 import BeautifulSoup
from jsonschema import validate
from smart_open import open
from tqdm import tqdm

from patcit.serialize import contextual_citation
from patcit.validation.schema import get_schema
from patcit.validation.shape import prep_and_pop

csv.field_size_limit(sys.maxsize)

# TODO: add coordinates somewhere?


async def prep_validate_ccit(id_, ccit, flavor):
    """
    Prep and validate contextual citation (npl or pat)
    :param id_: str, e.g publication number of the originating patent
    :param ccit: bs4.Soup
    :param flavor: str, in ["npl", "pat"]
    :return:str, json like
    """
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


async def prep_validate_ccits(id_, ccits, flavor):
    """
    Prep and validate a list of contextual citations
    :param id_: str, e.g publication number of the originating patent
    :param ccits: list[bs4.Soup]
    :param flavor: str, in ["npl", "pat"]
    :return: list
    """
    assert flavor in ["npl", "pat"]
    tasks = []
    for ccit in ccits:
        task = asyncio.create_task(prep_validate_ccit(id_, ccit, flavor))
        tasks.append(task)
    return await asyncio.gather(*tasks)


def serialize_prep_validate_ccits(id_, citations):
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
        npls = asyncio.run(prep_validate_ccits(id_, npls, "npl"))
    else:
        npls = [
            json.dumps({pk: id_})
        ]  # we create an empty entry when there were no detected
        # citations

    if pats:
        pats = asyncio.run(contextual_citation.fetch_patents(id_, pats))
        pats = asyncio.run(prep_validate_ccits(id_, pats, "pat"))
    else:
        pats = [
            json.dumps({pk: id_})
        ]  # we create an empty entry when there were no detected
        # citations

    return npls, pats


def serialize(input_file):
    """
    :param input_file: str, file
    :return:
    """
    root = os.path.dirname(input_file)
    f_name = (os.path.split(input_file)[-1]).split(".")[
        0
    ]  # file name w/o format extension
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
                npls, pats = serialize_prep_validate_ccits(
                    line["publication_number"], line["citation"]
                )
                # print(npls)
                fout_npls.write("\n".join(npls) + "\n")
                fout_pats.write("\n".join(pats) + "\n")
            line_count += 1


if __name__ == "__main__":

    @click.command()
    @click.option("--path", type=str, help="File or folder path. Wildcard '*' enabled")
    @click.option(
        "--max_workers",
        type=int,
        default=5,
        help="Maximum number of threads running in parallel'",
    )
    def main(path, max_workers):
        files = glob(path)
        with concurrent.futures.ProcessPoolExecutor(
            max_workers=max_workers
        ) as executor:
            executor.map(serialize, files)

    main()
