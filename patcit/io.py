import csv
import sys

import requests
from bs4 import BeautifulSoup
from smart_open import open
from tqdm import tqdm

csv.field_size_limit(sys.maxsize)

header_fin_tls214 = [
    "npl_publn_id",
    "npl_type",
    "npl_biblio",
    "npl_author",
    "npl_title1",
    "npl_title2",
    "npl_editor",
    "npl_volume",
    "npl_issue",
    "npl_publn_date",
    "npl_publn_end_date",
    "npl_publisher",
    "npl_page_first",
    "npl_page_last",
    "npl_abstract_nr",
    "npl_doi",
    "npl_isbn",
    "npl_issn",
    "online_availability",
    "online_classification",
    "online_search_date",
]

header_fin_fulltext_us = ["publication_number", "description"]


def process_biblio_tls214(
    input_file: str, consolidate: int = 1, capitalize: bool = True
):
    tmp = input_file.split("/")
    output_file = "/".join(tmp[:-1]) + "/processed_" + ".".join(tmp[-1].split(".")[:-1])
    data = {"citations": None, "consolidateCitations": consolidate}  # init
    with open(input_file, mode="r") as fin:
        fin_reader = csv.DictReader(
            fin,
            fieldnames=header_fin_tls214,
            delimiter=",",
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL,
        )
        with open(output_file, mode="w") as fout:
            fout_writer = csv.DictWriter(
                fout,
                fieldnames=["npl_publn_id", "npl_biblio", "npl_grobid"],
                delimiter=",",
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL,
            )
            line_count = 0
            for line in tqdm(fin_reader):
                if line_count == 0:
                    fout_writer.writeheader()
                    pass

                else:
                    print(line_count)
                    npl_biblio_ = (
                        line["npl_biblio"].title() if capitalize else line["npl_biblio"]
                    )
                    print(line["npl_biblio"])
                    data.update({"citations": npl_biblio_})
                    print(data)
                    # Seems that .title() improves output
                    # TODO discuss with @kermitt2
                    response = requests.post(
                        "http://localhost:8070/api/processCitation", data=data
                    )
                    fout_writer.writerow(
                        {
                            "npl_publn_id": line["npl_publn_id"],
                            "npl_biblio": line["npl_biblio"],
                            "npl_grobid": response.text,
                        }
                    )
                line_count += 1


def process_full_text(input_file: str):
    tmp = input_file.split("/")
    output_file = "/".join(tmp[:-1]) + "/processed_" + ".".join(tmp[-1].split(".")[:-1])
    data = {"input": None, "consolidateCitations": 1}  # init

    with open(input_file, mode="r") as fin:
        fin_reader = csv.DictReader(
            fin,
            fieldnames=header_fin_fulltext_us,
            delimiter=",",
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL,
        )
        with open(output_file, mode="w") as fout:
            fout_writer = csv.DictWriter(
                fout,
                fieldnames=["publication_number", "citations"],
                delimiter=",",
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL,
            )
            line_count = 0
            for line in tqdm(fin_reader):
                if line_count == 0:
                    fout_writer.writeheader()
                    pass
                else:
                    # print(line_count)
                    data.update({"input": line["description"]})

                    response = requests.post(
                        "http://localhost:8070/api/processCitationPatentTXT", data=data
                    )
                    soup = BeautifulSoup(response.text, "lxml")

                    fout_writer.writerow(
                        {
                            "publication_number": line["publication_number"],
                            "citations": list(
                                map(lambda x: str(x), soup.find_all("biblstruct"))
                            ),
                        }
                    )
                line_count += 1
