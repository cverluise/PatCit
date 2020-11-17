import asyncio
import concurrent.futures
import csv
import json
import lzma
import operator
import sys
from glob import glob
from hashlib import md5

import pycld2 as cld2
import spacy
import typer
from bs4 import BeautifulSoup
from jsonschema import validate
from smart_open import open, register_compressor

from patcit.serialize import intext, bibref
from patcit.serialize.validation.issues import eval_issues
from patcit.serialize.validation.resolve import solve_issues
from patcit.serialize.validation.schema import get_schema
from patcit.serialize.validation.typing import prep_and_pop

csv.field_size_limit(sys.maxsize)

app = typer.Typer()


# TODO: relax assumption on file names?

# add support for xz compressed files
def _handle_xz(file_obj, mode):
    return lzma.LZMAFile(filename=file_obj, mode=mode, format=lzma.FORMAT_XZ)


register_compressor(".xz", _handle_xz)


def serialize_prep_validate_grobid_npl(line):
    npl_publn_id, npl_grobid = line.get("npl_publn_id"), line.get("npl_grobid")
    if npl_grobid:
        soup = BeautifulSoup(npl_grobid, "lxml")
        out = asyncio.run(bibref.fetch_all_tags(npl_publn_id, soup))

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
    typer.echo(json.dumps(out))


@app.command()
def grobid_npl(path: str, max_workers: int = None):
    """Serialize npl citations from GROBID parsing
    """
    # TODO add md5 somewhere
    files = glob(path)
    for file in files:
        with open(file, "r") as fin:
            lines = csv.DictReader(
                fin, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=max_workers
            ) as executor:
                executor.map(serialize_prep_validate_grobid_npl, lines)


async def prep_validate_intext_cits(id_, ccits, flavor):
    """
    Prep and validate a list of contextual citations
    :param id_: str, e.g publication number of the originating patent
    :param ccits: list[bs4.Soup]
    :param flavor: str, in ["npl", "pat"]
    :return: list
    """

    async def prep_validate_intext_cit(id_, ccit, flavor):
        pk = intext.pk
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


def serialize_prep_validate_intext_cits(id_, citations, flavor: str):
    """
    Return a list of serialized npls and pats
    :param id_: str, e.g publication number of the originating patent
    :param citations: grobid output
    :return: (list, list), (npls, pats)
    """
    pk = intext.pk
    soup = BeautifulSoup(citations, "lxml")
    npls, pats = intext.split_pats_npls(soup)

    if flavor == "npl":
        if npls:
            npls = asyncio.run(intext.fetch_npls(id_, npls))
            npls = asyncio.run(prep_validate_intext_cits(id_, npls, "npl"))
        else:
            npls = [json.dumps({pk: id_})]
            # we create an empty entry when there were no detected
            # citations
        cits = npls
    else:
        if pats:
            pats = asyncio.run(intext.fetch_patents(id_, pats))
            pats = asyncio.run(prep_validate_intext_cits(id_, pats, "pat"))
        else:
            pats = [json.dumps({pk: id_})]
            # we create an empty entry when there were no detected
            # citations
        cits = pats

    return cits


@app.command()
def grobid_intext(file: str, flavor: str = None, skip_header: bool = True):
    """Serialize in-text citations

    Notes: Assume original file names ('processed_' in, 'serialized_' out)"""
    assert flavor in ["npl", "pat"]

    with open(file, "r") as fin:
        lines = csv.DictReader(
            fin,
            fieldnames=["publication_number", "citation"],
            delimiter=",",
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL,
        )
        header = 0
        for line in lines:
            if header == 0 and skip_header:  # header
                header += 1
                pass
            else:
                cits = serialize_prep_validate_intext_cits(
                    line["publication_number"], line["citation"], flavor
                )

                for cit in cits:
                    typer.echo(cit)


@app.command()
def patcit_bibref(path, src_flavor: str = None):
    """Serialize bibref from grobid or crossref to a common schema

    Expect JSONL input"""

    def patcit_bibref_(line, src_flavor):
        try:
            line = json.loads(line)
            format_ok = True
        except Exception as e:
            format_ok = False
            out = {"exception": str(e), "line": line}
            pass

        if format_ok:
            out = asyncio.run(bibref.to_patcit(line, src_flavor))
            try:
                validate(instance=out, schema=get_schema("bibref"))
            except Exception as e:
                out = out.update({"exception": str(e), "issues": [0]})
        typer.echo(json.dumps(out))

    files = glob(path)
    for file in files:
        with open(file) as lines:
            for line in lines:
                patcit_bibref_(line, src_flavor)


@app.command()
def npl_properties(path, cat_model: str = None, language_codes: str = "en,un"):
    """Return the serialized properties

    Expect JSONL input"""

    async def get_cat(text, nlp):
        """"""
        if "wiki" in text.lower():
            cat, score = "WIKI", 1  # by convention
        else:
            doc = nlp(text)
            cat, score = max(doc.cats.items(), key=operator.itemgetter(1))
            score = round(score, 2)  # 2 digits only
        return {"npl_cat": cat, "npl_cat_score": score}

    async def get_md5(text):
        return {"md5": md5(text.lower().encode("utf-8")).hexdigest()}

    async def get_language(text):
        is_reliable, _, details = cld2.detect(text)

        _, language_code, _, _ = details[0]
        out = {
            "language_is_reliable": is_reliable,
            # "language": language,
            "language_code": language_code,
            # "language_percent": percent,
            # "language_score": score,
        }
        return out

    def get_npl_cat_language_flag(line, language_codes):
        if not line.get("language_code") in language_codes:
            npl_cat_language_flag = True
        else:
            npl_cat_language_flag = False
        return {"npl_cat_language_flag": npl_cat_language_flag}

    async def get_properties(line, nlp, language_codes):
        npl_biblio = line.get("npl_biblio")
        known_cat = bool(line.get("npl_cat"))

        md5_task = asyncio.create_task(get_md5(npl_biblio))
        language_task = asyncio.create_task(get_language(npl_biblio))

        tasks = [md5_task, language_task]
        if not known_cat:
            cat_task = asyncio.create_task(get_cat(npl_biblio, nlp))
            tasks += [cat_task]
        else:  # 1 by convention
            line.update({"npl_cat_score": 1})

        tasks = await asyncio.gather(*tasks)

        for task in tasks:
            line.update(task)

        line.update(get_npl_cat_language_flag(line, language_codes))
        if not line.get("patcit_id"):
            line.update({"patcit_id": line.get("md5")})

        typer.echo(json.dumps(line))
        # return line

    files = glob(path)
    nlp_ = spacy.load(cat_model)
    language_codes_ = language_codes.split(",")

    for file in files:
        with open(file) as lines:
            for line_ in lines:
                out = json.loads(line_)
                asyncio.run(get_properties(out, nlp_, language_codes_))
                # typer.echo(json.dumps(out))
                # out = None


def add_publication_number(line):
    line = json.loads(line)
    pubnum = line.get("pubnum")

    publication_number = intext.get_publication_number(pubnum)
    line.update({"publication_number": publication_number})

    typer.echo(json.dumps(line))


@app.command()
def pat_add_pubnum(file, max_workers: int = 10):
    """Add a publication number to patents detected in the text itself based on serialized grobid
    attributes and the google patents linking api"""
    with open(file, "r") as lines:
        with concurrent.futures.ThreadPoolExecutor(max_workers) as executor:
            executor.map(add_publication_number, lines)


@app.command()
def add_identifier(file: str):
    """Return each line with identifiers (md5 and patcit_id) - create if not existing, preserve
    otherwise.
    Expect a .jsonl file.
    """
    with open(file, "r") as lines:
        for line in lines:
            line = json.loads(line)
            doi_ = line.get("DOI")
            md5_ = line.get("md5")

            if not md5_:
                md5_ = md5(
                    json.dumps(line, sort_keys=True).lower().encode("utf-8")
                ).hexdigest()
                line.update({"md5": md5_})

            if doi_:
                line.update({"patcit_id": doi_})
            else:
                line.update({"patcit_id": md5_})

            typer.echo(json.dumps(line))


if __name__ == "__main__":
    app()
