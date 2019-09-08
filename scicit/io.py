import csv

import requests
from smart_open import open
from tqdm import tqdm

header_fin = [
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


def process_biblio_tls214(input_file: str):
    tmp = input_file.split("/")
    output_file = (
        "/".join(tmp[:-1]) + "/processed_" + ".".join(tmp[-1].split(".")[:-1])
    )
    data = {"citations": None, "consolidateCitations": 1}  # init
    with open(input_file, mode="r") as fin:
        fin_reader = csv.DictReader(
            fin,
            fieldnames=header_fin,
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
                    # print(line_count)
                    data.update({"citations": line["npl_biblio"].title()})
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
