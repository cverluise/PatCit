import asyncio

import requests
from bs4 import BeautifulSoup

from scicit.tei_parser import fetch_analytic, fetch_monogr, fetch_all

citation = (
    "WEIDLE U H ET AL: 'NEW EXPRESSION SYSTEM FOR MAMMALIAN CELLS BASED ON PUTATIVE "
    "REPLICATOR SEQUENCES OF THE MOUSE AND A TRUNCATED THYMIDINE KINASE GENE', GENE, "
    "ELSEVIER BIOMEDICAL PRESS. AMSTERDAM, NL, vol. 73, no. 2, 20 December 1988 ("
    "1988-12-20), pages 427 - 437, XP000000220, ISSN: 0378-1119"
)

# 'Kotter, David K., et al..; Abstract: Detection and Classification of Concealed '
# 'Weapons Using a Magnetometer-based Portal; NASA ADS Instrumentation Abstract '
# 'Service; Aug. 2002; 1 page; The International Society for Optical Engineering.'

# "Graff, Expert. Opin. Ther. Targets (2002) 6(1): 103-113"

data = {"citations": citation.title(), "consolidateCitations": 1}


response = requests.post(
    "http://localhost:8070/api/processCitation", data=data
)


soup = BeautifulSoup(response.text, "lxml")

analytic_ = soup.find("analytic")
monogr_ = soup.find("monogr")

analytic_dict = asyncio.run(fetch_analytic(analytic_))
imprint_dict = asyncio.run(fetch_monogr(monogr_))
all_dict = asyncio.run(fetch_all(response.text))
