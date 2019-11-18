# READ ME


## DOCDB

```bash
python bin/ListKeys.py --path "/Volumes/HD_CyrilVerluise/patstat18b/small_chunks/serialized_tls214_part0*.jsonl"
```

```json
{"DOI": "(10949781, <class 'str'>)",
 "ISSN": "(8908483, <class 'str'>)",
 "ISSNe": "(4976619, <class 'str'>)",
 "PMCID": "(1160983, <class 'str'>)",
 "PMID": "(5849708, <class 'str'>)",
 "authors": "(26088857, <class 'dict'>)",
 "from": "(19296258, <class 'int'>)",
 "idno": "(1730523, <class 'str'>)",
 "issue": "(13002428, <class 'int'>)",
 "issues": "(11553001, <class 'list'>)",
 "level": "(151, <class 'str'>)",
 "npl_publn_id": "(38928209, <class 'int'>)",
 "page": "(4277130, <class 'str'>)",
 "target": "(3845427, <class 'str'>)",
 "title_abbrev_j": "(8611341, <class 'str'>)",
 "title_j": "(21118045, <class 'str'>)",
 "title_m": "(6743861, <class 'str'>)",
 "title_main_a": "(18387599, <class 'str'>)",
 "title_main_m": "(7922582, <class 'str'>)",
 "to": "(19539649, <class 'int'>)",
 "type": "(35598855, <class 'str'>)",
 "unit": "(19721770, <class 'str'>)",
 "volume": "(24445214, <class 'int'>)",
 "when": "(35492532, <class 'str'>)",
 "year": "(34909502, <class 'int'>)"}
```

NB: there were 2 missing "small-chunks" (2/396)

##  Crossref

```bash
python bin/ListKeys.py --path /Volumes/HD_CyrilVerluise/biblio-glutton/crossref-works.2018-09-05.json.xz --tar True --limit 1000000
```

```
{'DOI': (1000001, <class 'str'>),
 'ISBN': (292951, <class 'list'>),
 'ISSN': (468030, <class 'list'>),
 'URL': (1000001, <class 'str'>),
 '_id': (1000001, <class 'dict'>),
 'abstract': (19684, <class 'str'>),
 'alternative-id': (250357, <class 'list'>),
 'approved': (6477, <class 'dict'>),
 'archive': (5374, <class 'list'>),
 'article-number': (4692, <class 'str'>),
 'assertion': (36463, <class 'list'>),
 'author': (583456, <class 'list'>),
 'chair': (39, <class 'list'>),
 'clinical-trial-number': (24, <class 'list'>),
 'container-title': (891983, <class 'list'>),
 'content-created': (71173, <class 'dict'>),
 'content-domain': (1000001, <class 'dict'>),
 'content-updated': (67958, <class 'dict'>),
 'created': (1000001, <class 'dict'>),
 'degree': (267, <class 'list'>),
 'deposited': (1000001, <class 'dict'>),
 'edition-number': (2, <class 'str'>),
 'editor': (19887, <class 'list'>),
 'event': (52122, <class 'dict'>),
 'funder': (9603, <class 'list'>),
 'indexed': (1000001, <class 'dict'>),
 'institution': (83328, <class 'dict'>),
 'is-referenced-by-count': (1000001, <class 'int'>),
 'isbn-type': (319, <class 'list'>),
 'issn-type': (468030, <class 'list'>),
 'issue': (395087, <class 'str'>),
 'issued': (1000001, <class 'dict'>),
 'journal-issue': (395119, <class 'dict'>),
 'language': (318573, <class 'str'>),
 'license': (153082, <class 'list'>),
 'link': (478720, <class 'list'>),
 'member': (1000001, <class 'str'>),
 'original-title': (23358, <class 'list'>),
 'page': (541715, <class 'str'>),
 'prefix': (1000001, <class 'str'>),
 'published-online': (315452, <class 'dict'>),
 'published-print': (665761, <class 'dict'>),
 'publisher': (999977, <class 'str'>),
 'publisher-location': (221171, <class 'str'>),
 'reference': (70604, <class 'list'>),
 'reference-count': (1000001, <class 'int'>),
 'relation': (70628, <class 'dict'>),
 'score': (1000001, <class 'int'>),
 'short-container-title': (394346, <class 'list'>),
 'short-title': (1400, <class 'list'>),
 'source': (1000001, <class 'str'>),
 'standards-body': (6233, <class 'dict'>),
 'subject': (3051, <class 'list'>),
 'subtitle': (106937, <class 'list'>),
 'title': (920820, <class 'list'>),
 'translator': (54, <class 'list'>),
 'type': (999876, <class 'str'>),
 'update-policy': (79705, <class 'str'>),
 'update-to': (1931, <class 'list'>),
 'volume': (423500, <class 'str'>)}
```

<details>

```
{'DOI': (1000001, <class 'str'>, '10.1111/iwj.12120'),
 'ISBN': (292951, <class 'list'>, ['9783318060867', '9783318060874']),
 'ISSN': (468030, <class 'list'>, ['1742-4801']),
 'URL': (1000001, <class 'str'>, 'http://dx.doi.org/10.1111/iwj.12120'),
 '_id': (1000001, <class 'dict'>, {'$oid': '5b907476f1c57925e77f7436'}),
 'abstract': (19684,
              <class 'str'>,
              '<jats:p>&lt;p&gt;Accounting for Political Parties. Healthy '
              'political parties, credible and capable of running the General '
              'Election held in a democratic, honest and fair is the capital '
              'of democracy credible. Democracy is a credible government '
              'authorized the creation of a solid and authoritative with '
              'effective control of the institution legistalif. Credible '
              'democracy is not possible without transparency and clear '
              'accountability mechanisms for the financing of political '
              'activities, both financial and political party financing of the '
              'General Election. This financial accountability requires '
              'transparency of financial accounting standards for political '
              'parties, political party auditing guidelines, and the existence '
              'of guidelines, regulations, and procedures for financial '
              'reporting on the activities of the General Election campaign '
              'for political parties. One of the major problems that arise are '
              'the accounting standards. In the meantime, the existing '
              'accounting standards, namely Principle of Financial Accounting '
              'Standards 45, the accounting standards made for non-profit '
              'organization that Indonesia Institute of Accountants (IAI )is '
              'also used for political parties. (PSAK) 45 is not sufficient to '
              'accommodate the characteristics of different political parties '
              'with other nonprofit organizations. Therefore, this study '
              'recommends a modification or specific guidelines for financial '
              'accounting standard for political parties. This article we hope '
              'will encourage various parties, in this Parliament, the '
              'Commission, the Supreme Court and the Association of Accounting '
              'Indonesia to sit together and agree on specific accounting '
              'standards for political parties including campaign funds. This '
              'paper hopefully be a reference, although subject to change '
              'according to the Law on Political Parties and Elections are '
              'currently being discussed in Parliament. Accounting standards '
              'in this paper can be a reference to the new legislation. '
              'Reflecting the general election of 2009 was the lack of '
              'management, accountability and control of financing of '
              'political activities. Almost all political parties having '
              'problems financing of political activities, including the '
              'financing of legislative elections that followed the political '
              'campaign. Weak financial systems has led to uncontrolled '
              'political money (money politics), which involves \xa0almost all '
              'political parties in elections.&lt;/p&gt;</jats:p>'),
 'accepted': (33038, <class 'str'>),
 'alternative-id': (250357, <class 'list'>, ['S1054139X1500508X']),
 'approved': (6477, <class 'dict'>, {'date-parts': [[2015, 1, 31]]}),
 'archive': (5374, <class 'list'>, ['Portico']),
 'article-number': (4692, <class 'str'>, '70'),
 'assertion': (36463,
               <class 'list'>,
               [{'label': 'This article is maintained by',
                 'name': 'publisher',
                 'value': 'Elsevier'},
                {'label': 'Article Title',
                 'name': 'articletitle',
                 'value': 'Welcome to three new Editors'},
                {'label': 'Journal Title',
                 'name': 'journaltitle',
                 'value': 'Materials Science and Engineering: R: Reports'},
                {'label': 'CrossRef DOI link to publisher maintained version',
                 'name': 'articlelink',
                 'value': 'https://doi.org/10.1016/j.mser.2016.02.001'},
                {'label': 'Content Type',
                 'name': 'content_type',
                 'value': 'simple-article'},
                {'label': 'Copyright',
                 'name': 'copyright',
                 'value': 'Copyright © 2016 Published by Elsevier B.V.'}]),
 'author': (583456,
            <class 'list'>,
            [{'affiliation': [{'name': 'Clinic for Plastic and Reconstructive '
                                       'Surgery, Handsurgery, Burn Care '
                                       'Center; University of Witten/Herdecke, '
                                       'Cologne-Merheim Medical Center; Köln '
                                       'Germany'}],
              'family': 'Thamm',
              'given': 'Oliver C',
              'sequence': 'first'},
             {'affiliation': [{'name': 'Clinic for Plastic and Reconstructive '
                                       'Surgery, Handsurgery, Burn Care '
                                       'Center; University of Witten/Herdecke, '
                                       'Cologne-Merheim Medical Center; Köln '
                                       'Germany'}],
              'family': 'Theodorou',
              'given': 'Panagiotis',
              'sequence': 'additional'},
             {'affiliation': [{'name': 'Institute for Research in Operative '
                                       'Medicine (IFOM); University of '
                                       'Witten/Herdecke; Köln Germany'}],
              'family': 'Stuermer',
              'given': 'Ewa',
              'sequence': 'additional'},
             {'affiliation': [{'name': 'Clinic for Plastic and Reconstructive '
                                       'Surgery, Handsurgery, Burn Care '
                                       'Center; University of Witten/Herdecke, '
                                       'Cologne-Merheim Medical Center; Köln '
                                       'Germany'}],
              'family': 'Zinser',
              'given': 'Max J',
              'sequence': 'additional'},
             {'affiliation': [{'name': 'Institute for Research in Operative '
                                       'Medicine (IFOM); University of '
                                       'Witten/Herdecke; Köln Germany'}],
              'family': 'Neugebauer',
              'given': 'Edmund A',
              'sequence': 'additional'},
             {'affiliation': [{'name': 'Clinic for Plastic and Reconstructive '
                                       'Surgery, Handsurgery, Burn Care '
                                       'Center; University of Witten/Herdecke, '
                                       'Cologne-Merheim Medical Center; Köln '
                                       'Germany'}],
              'family': 'Fuchs',
              'given': 'Paul C',
              'sequence': 'additional'},
             {'affiliation': [{'name': 'Department of Trauma and Orthopedic '
                                       'Surgery; University of '
                                       'Witten/Herdecke, Cologne-Merheim '
                                       'Medical Center; Köln Germany'}],
              'family': 'Koenen',
              'given': 'Paola',
              'sequence': 'additional'}]),
 'chair': (39,
           <class 'list'>,
           [{'affiliation': [],
             'family': '杜祥琬',
             'given': '杜祥琬',
             'sequence': 'first'}]),
 'clinical-trial-number': (24,
                           <class 'list'>,
                           [{'clinical-trial-number': 'nct02308722',
                             'registry': '10.18810/clinical-trials-gov'}]),
 'container-title': (891983, <class 'list'>, ['International Wound Journal']),
 'content-created': (71173, <class 'dict'>, {'date-parts': [[2014, 11, 26]]}),
 'content-domain': (1000001,
                    <class 'dict'>,
                    {'crossmark-restriction': False, 'domain': []}),
 'content-updated': (67958, <class 'dict'>, {'date-parts': [[2014, 8, 1]]}),
 'created': (1000001,
             <class 'dict'>,
             {'date-parts': [[2013, 7, 11]],
              'date-time': '2013-07-11T07:01:43Z',
              'timestamp': {'$numberLong': '1373526103000'}}),
 'degree': (267, <class 'list'>, ['PhD']),
 'deposited': (1000001,
               <class 'dict'>,
               {'date-parts': [[2017, 6, 21]],
                'date-time': '2017-06-21T16:04:49Z',
                'timestamp': {'$numberLong': '1498061089000'}}),
 'edition-number': (2, <class 'str'>, '2'),
 'editor': (19887,
            <class 'list'>,
            [{'affiliation': [],
              'family': 'Arévalo',
              'given': 'F.',
              'sequence': 'first'},
             {'affiliation': [],
              'family': 'Alezzandrini',
              'given': 'A.',
              'sequence': 'additional'},
             {'affiliation': [],
              'family': 'Quiroz Mercado',
              'given': 'H.',
              'sequence': 'additional'},
             {'affiliation': [],
              'family': 'Roca',
              'given': 'J.A.',
              'sequence': 'additional'},
             {'affiliation': [],
              'family': 'Rodríguez',
              'given': 'F.J.',
              'sequence': 'additional'}]),
 'event': (52122,
           <class 'dict'>,
           {'acronym': 'icelaic-15',
            'end': {'date-parts': [[2015, 11, 8]]},
            'location': 'Kaifeng, China',
            'name': '2015 2nd International Conference on Education, Language, '
                    'Art and Intercultural Communication (ICELAIC-15)',
            'start': {'date-parts': [[2015, 11, 7]]}}),
 'funder': (9603,
            <class 'list'>,
            [{'DOI': '10.13039/501100001809',
              'award': ['81561128015', 'D12110000412001', '2015-3-017'],
              'doi-asserted-by': 'publisher',
              'name': 'National Natural Science Foundation of China'}]),
 'indexed': (1000001,
             <class 'dict'>,
             {'date-parts': [[2018, 3, 17]],
              'date-time': '2018-03-17T20:59:31Z',
              'timestamp': {'$numberLong': '1521320371467'}}),
 'institution': (83328,
                 <class 'dict'>,
                 {'acronym': ['-'], 'name': 'ISRCTN', 'place': ['London, UK']}),
 'is-referenced-by-count': (1000001, <class 'int'>, 3),
 'isbn-type': (319,
               <class 'list'>,
               [{'type': 'print', 'value': '9780444636997'}]),
 'issn-type': (468030,
               <class 'list'>,
               [{'type': 'print', 'value': '1742-4801'}]),
 'issue': (395087, <class 'str'>, '4'),
 'issued': (1000001, <class 'dict'>, {'date-parts': [[2013, 7, 11]]}),
 'journal-issue': (395119, <class 'dict'>, {'issue': '4'}),
 'language': (318573, <class 'str'>, 'en'),
 'license': (153082,
             <class 'list'>,
             [{'URL': 'http://doi.wiley.com/10.1002/tdm_license_1.1',
               'content-version': 'tdm',
               'delay-in-days': 782,
               'start': {'date-parts': [[2015, 9, 1]],
                         'date-time': '2015-09-01T00:00:00Z',
                         'timestamp': {'$numberLong': '1441065600000'}}}]),
 'link': (478720,
          <class 'list'>,
          [{'URL': 'https://api.wiley.com/onlinelibrary/tdm/v1/articles/10.1111%2Fiwj.12120',
            'content-type': 'unspecified',
            'content-version': 'vor',
            'intended-application': 'text-mining'}]),
 'member': (1000001, <class 'str'>, '311'),
 'original-title': (23358, <class 'list'>, ['농가용 도정기의 구조요인과 도정성능의 분석']),
 'page': (541715, <class 'str'>, '387-396'),
 'prefix': (1000001, <class 'str'>, '10.1111'),
 'published-online': (315452, <class 'dict'>, {'date-parts': [[2013, 7, 11]]}),
 'published-print': (665761, <class 'dict'>, {'date-parts': [[2015, 8]]}),
 'publisher': (999977, <class 'str'>, 'Wiley-Blackwell'),
 'publisher-location': (221171, <class 'str'>, 'Paris, France'),
 'reference': (70604,
               <class 'list'>,
               [{'DOI': '10.1111/j.1524-475X.2009.00543.x',
                 'article-title': 'Human skin wounds: a major and snowballing '
                                  'threat to public health and the economy',
                 'author': 'Sen',
                 'doi-asserted-by': 'crossref',
                 'first-page': '763',
                 'journal-title': 'Wound Repair Regen',
                 'key': '10.1111/iwj.12120-BIB0001|iwj12120-cit-0001',
                 'volume': '17',
                 'year': '2009'},
                {'article-title': 'Chemokines in cutaneous wound healing',
                 'author': 'Gillitzer',
                 'first-page': '513',
                 'journal-title': 'J Leukoc Biol',
                 'key': '10.1111/iwj.12120-BIB0002|iwj12120-cit-0002',
                 'volume': '69',
                 'year': '2001'},
                {'DOI': '10.1111/j.1067-1927.2005.130411.x',
                 'article-title': 'Early cellular changes of human mesenchymal '
                                  'stem cells and their interaction with other '
                                  'cells',
                 'author': 'Akino',
                 'doi-asserted-by': 'crossref',
                 'first-page': '434',
                 'journal-title': 'Wound Repair Regen',
                 'key': '10.1111/iwj.12120-BIB0003|iwj12120-cit-0003',
                 'volume': '13',
                 'year': '2005'},
                {'DOI': '10.1111/j.1524-475X.2000.00392.x',
                 'article-title': 'Proteinases, their inhibitors, and cytokine '
                                  'profiles in acute wound fluid',
                 'author': 'Baker',
                 'doi-asserted-by': 'crossref',
                 'first-page': '392',
                 'journal-title': 'Wound Repair Regen',
                 'key': '10.1111/iwj.12120-BIB0004|iwj12120-cit-0004',
                 'volume': '8',
                 'year': '2000'},
                {'DOI': '10.1046/j.1524-475X.1999.00442.x',
                 'article-title': 'Analysis of the acute and chronic wound '
                                  'environments: the role of proteases and '
                                  'their inhibitors',
                 'author': 'Trengove',
                 'doi-asserted-by': 'crossref',
                 'first-page': '442',
                 'journal-title': 'Wound Repair Regen',
                 'key': '10.1111/iwj.12120-BIB0005|iwj12120-cit-0005',
                 'volume': '7',
                 'year': '1999'},
                {'DOI': '10.1111/1523-1747.ep12359590',
                 'article-title': 'Wound fluid from chronic leg ulcers '
                                  'contains elevated levels of '
                                  'metalloproteinases MMP-2 and MMP-9',
                 'author': 'Wysocki',
                 'doi-asserted-by': 'crossref',
                 'first-page': '64',
                 'journal-title': 'J Invest Dermatol',
                 'key': '10.1111/iwj.12120-BIB0006|iwj12120-cit-0006',
                 'volume': '101',
                 'year': '1993'},
                {'DOI': '10.1046/j.1524-475X.1999.00423.x',
                 'article-title': 'Matrix metalloproteinases in repair',
                 'author': 'Parks',
                 'doi-asserted-by': 'crossref',
                 'first-page': '423',
                 'journal-title': 'Wound Repair Regen',
                 'key': '10.1111/iwj.12120-BIB0007|iwj12120-cit-0007',
                 'volume': '7',
                 'year': '1999'},
                {'DOI': '10.1111/1523-1747.ep12365637',
                 'article-title': 'Wound fluids from human pressure ulcers '
                                  'contain elevated matrix metalloproteinase '
                                  'levels and activity compared to surgical '
                                  'wound fluids',
                 'author': 'Yager',
                 'doi-asserted-by': 'crossref',
                 'first-page': '743',
                 'journal-title': 'J Invest Dermatol',
                 'key': '10.1111/iwj.12120-BIB0008|iwj12120-cit-0008',
                 'volume': '107',
                 'year': '1996'},
                {'DOI': '10.1046/j.1524-475X.1996.40307.x',
                 'article-title': 'Biochemical analysis of acute and chronic '
                                  'wound environments',
                 'author': 'Tarnuzzer',
                 'doi-asserted-by': 'crossref',
                 'first-page': '321',
                 'journal-title': 'Wound Repair Regen',
                 'key': '10.1111/iwj.12120-BIB0009|iwj12120-cit-0009',
                 'volume': '4',
                 'year': '1996'},
                {'DOI': '10.4093/dmj.2011.35.3.226',
                 'article-title': 'Comparison of EGF with VEGF non-viral gene '
                                  'therapy for cutaneous wound healing of '
                                  'streptozotocin diabetic mice',
                 'author': 'Ko',
                 'doi-asserted-by': 'crossref',
                 'first-page': '226',
                 'journal-title': 'Diabetes Metab J',
                 'key': '10.1111/iwj.12120-BIB0010|iwj12120-cit-0010',
                 'volume': '35',
                 'year': '2011'},
                {'DOI': '10.1073/pnas.95.10.5672',
                 'article-title': 'Neuronal defects and delayed wound healing '
                                  'in mice lacking fibroblast growth factor 2',
                 'author': 'Ortega',
                 'doi-asserted-by': 'crossref',
                 'first-page': '5672',
                 'journal-title': 'Proc Natl Acad Sci USA',
                 'key': '10.1111/iwj.12120-BIB0011|iwj12120-cit-0011',
                 'volume': '95',
                 'year': '1998'},
                {'DOI': '10.1016/j.bjps.2008.05.036',
                 'article-title': 'Searching for the right timing of surgical '
                                  'delay: angiogenesis, vascular endothelial '
                                  'growth factor and perfusion changes in a '
                                  'skin-flap model',
                 'author': 'Holzbach',
                 'doi-asserted-by': 'crossref',
                 'first-page': '1534',
                 'journal-title': 'J Plast Reconstr Aesthet Surg',
                 'key': '10.1111/iwj.12120-BIB0012|iwj12120-cit-0012',
                 'volume': '62',
                 'year': '2009'},
                {'article-title': 'Roles of cytokines in wound healing '
                                  'processes',
                 'author': 'Ono',
                 'first-page': '522',
                 'journal-title': 'Nihon Geka Gakkai Zasshi',
                 'key': '10.1111/iwj.12120-BIB0013|iwj12120-cit-0013',
                 'volume': '100',
                 'year': '1999'},
                {'DOI': '10.1093/jb/mvr060',
                 'article-title': 'Critical role of c-Jun N-terminal kinase in '
                                  'regulating bFGF-induced angiogenesis in '
                                  'vitro',
                 'author': 'Kaikai',
                 'doi-asserted-by': 'crossref',
                 'first-page': '189',
                 'journal-title': 'J Biochem',
                 'key': '10.1111/iwj.12120-BIB0014|iwj12120-cit-0014',
                 'volume': '150',
                 'year': '2011'},
                {'DOI': '10.5021/ad.2011.23.2.150',
                 'article-title': 'Effects of human adipose-derived stem cells '
                                  'on cutaneous wound healing in nude mice',
                 'author': 'Lee',
                 'doi-asserted-by': 'crossref',
                 'first-page': '150',
                 'journal-title': 'Ann Dermatol',
                 'key': '10.1111/iwj.12120-BIB0015|iwj12120-cit-0015',
                 'volume': '23',
                 'year': '2011'},
                {'DOI': '10.1097/SAP.0b013e31817f01b6',
                 'article-title': 'Accelerated wound healing in '
                                  'healing-impaired db/db mice by autologous '
                                  'adipose tissue-derived stromal cells '
                                  'combined with atelocollagen matrix',
                 'author': 'Nambu',
                 'doi-asserted-by': 'crossref',
                 'first-page': '317',
                 'journal-title': 'Ann Plast Surg',
                 'key': '10.1111/iwj.12120-BIB0016|iwj12120-cit-0016',
                 'volume': '62',
                 'year': '2009'},
                {'DOI': '10.1161/ATVBAHA.108.178962',
                 'article-title': 'Cell therapy based on adipose '
                                  'tissue-derived stromal cells promotes '
                                  'physiological and pathological wound '
                                  'healing',
                 'author': 'Ebrahimian',
                 'doi-asserted-by': 'crossref',
                 'first-page': '503',
                 'journal-title': 'Arterioscler Thromb Vasc Biol',
                 'key': '10.1111/iwj.12120-BIB0017|iwj12120-cit-0017',
                 'volume': '29',
                 'year': '2009'},
                {'article-title': 'Competitive RNA templates for detection and '
                                  'quantitation of growth factors, cytokines, '
                                  'extracellular matrix components and matrix '
                                  'metalloproteinases by RT-PCR',
                 'author': 'Tarnuzzer',
                 'first-page': '670',
                 'journal-title': 'Biotechniques',
                 'key': '10.1111/iwj.12120-BIB0018|iwj12120-cit-0018',
                 'volume': '20',
                 'year': '1996'},
                {'DOI': '10.1046/j.1523-1747.2003.12471.x',
                 'article-title': 'Iron and 8-isoprostane levels in acute and '
                                  'chronic wounds',
                 'author': 'Yeoh-Ellerton',
                 'doi-asserted-by': 'crossref',
                 'first-page': '918',
                 'journal-title': 'J Invest Dermatol',
                 'key': '10.1111/iwj.12120-BIB0019|iwj12120-cit-0019',
                 'volume': '121',
                 'year': '2003'},
                {'DOI': '10.1128/jb.170.9.4055-4064.1988',
                 'article-title': 'Metabolic regulation in Streptomyces '
                                  'parvulus during actinomycin D synthesis, '
                                  'studied with 13C- and 15 N-labeled '
                                  'precursors by 13C and 15N nuclear magnetic '
                                  'resonance spectroscopy and by gas '
                                  'chromatography-mass spectrometry',
                 'author': 'Inbar',
                 'doi-asserted-by': 'crossref',
                 'first-page': '4055',
                 'journal-title': 'J Bacteriol',
                 'key': '10.1111/iwj.12120-BIB0020|iwj12120-cit-0020',
                 'volume': '170',
                 'year': '1988'},
                {'DOI': '10.1007/BF00174204',
                 'article-title': 'Enzyme stabilization be ectoine-type '
                                  'compatible solutes: protection against '
                                  'heating, freezing and drying',
                 'author': 'Lippert',
                 'doi-asserted-by': 'crossref',
                 'first-page': '61',
                 'journal-title': 'Appl Microbiol Biotechnol',
                 'key': '10.1111/iwj.12120-BIB0021|iwj12120-cit-0021',
                 'volume': '37',
                 'year': '1992'},
                {'DOI': '10.1016/j.bpc.2010.02.007',
                 'article-title': 'The effect of compatible solute ectoines on '
                                  'the structural organization of lipid '
                                  'monolayer and bilayer membranes',
                 'author': 'Harishchandra',
                 'doi-asserted-by': 'crossref',
                 'first-page': '37',
                 'issue': '1-3',
                 'journal-title': 'Biophys Chem',
                 'key': '10.1111/iwj.12120-BIB0022|iwj12120-cit-0022',
                 'volume': '150',
                 'year': '2010'},
                {'DOI': '10.1080/14653240600855905',
                 'article-title': 'Minimal criteria for defining multipotent '
                                  'mesenchymal stromal cells. The '
                                  'International Society for Cellular Therapy '
                                  'position statement',
                 'author': 'Dominici',
                 'doi-asserted-by': 'crossref',
                 'first-page': '315',
                 'journal-title': 'Cytotherapy',
                 'key': '10.1111/iwj.12120-BIB0023|iwj12120-cit-0023',
                 'volume': '8',
                 'year': '2006'},
                {'DOI': '10.1006/abio.2001.5530',
                 'article-title': 'A new quantitative method of real time '
                                  'reverse transcription polymerase chain '
                                  'reaction assay based on simulation of '
                                  'polymerase chain reaction kinetics',
                 'author': 'Liu',
                 'doi-asserted-by': 'crossref',
                 'first-page': '52',
                 'journal-title': 'Anal Biochem',
                 'key': '10.1111/iwj.12120-BIB0024|iwj12120-cit-0024',
                 'volume': '302',
                 'year': '2002'},
                {'DOI': '10.1111/1523-1747.ep12276531',
                 'article-title': 'Spreading and enhanced motility of human '
                                  'keratinocytes on fibronectin',
                 'author': "O'Keefe",
                 'doi-asserted-by': 'crossref',
                 'first-page': '125',
                 'journal-title': 'J Invest Dermatol',
                 'key': '10.1111/iwj.12120-BIB0025|iwj12120-cit-0025',
                 'volume': '85',
                 'year': '1985'},
                {'DOI': '10.1046/j.1524-4725.2000.99281.x',
                 'article-title': 'Level of fibronectin mRNA is markedly '
                                  'increased in human chronic wounds',
                 'author': 'Ongenae',
                 'doi-asserted-by': 'crossref',
                 'first-page': '447',
                 'journal-title': 'Dermatol Surg',
                 'key': '10.1111/iwj.12120-BIB0026|iwj12120-cit-0026',
                 'volume': '26',
                 'year': '2000'},
                {'DOI': '10.1111/1523-1747.ep12499839',
                 'article-title': 'Degradation of fibronectin and vitronectin '
                                  'in chronic wound fluid: analysis by cell '
                                  'blotting, immunoblotting, and cell adhesion '
                                  'assays',
                 'author': 'Grinnell',
                 'doi-asserted-by': 'crossref',
                 'first-page': '410',
                 'journal-title': 'J Invest Dermatol',
                 'key': '10.1111/iwj.12120-BIB0027|iwj12120-cit-0027',
                 'volume': '98',
                 'year': '1992'},
                {'DOI': '10.1111/j.1742-481X.2012.00967.x',
                 'article-title': "Chronic wounds - is cellular 'reception' at "
                                  'fault? Examining integrins and '
                                  'intracellular signalling',
                 'author': 'Widgerow',
                 'doi-asserted-by': 'crossref',
                 'first-page': '185',
                 'journal-title': 'Int Wound J',
                 'key': '10.1111/iwj.12120-BIB0028|iwj12120-cit-0028',
                 'volume': '10',
                 'year': '2013'},
                {'DOI': '10.1016/j.clindermatol.2010.03.009',
                 'article-title': 'Chronic wound infection: facts and '
                                  'controversies',
                 'author': 'Siddiqui',
                 'doi-asserted-by': 'crossref',
                 'first-page': '519',
                 'journal-title': 'Clin Dermatol',
                 'key': '10.1111/iwj.12120-BIB0029|iwj12120-cit-0029',
                 'volume': '28',
                 'year': '2010'},
                {'DOI': '10.1111/j.1524-475X.2007.00290.x',
                 'article-title': 'Inhibition of keratinocyte migration by '
                                  'lipopolysaccharide',
                 'author': 'Loryman',
                 'doi-asserted-by': 'crossref',
                 'first-page': '45',
                 'journal-title': 'Wound Repair Regen',
                 'key': '10.1111/iwj.12120-BIB0030|iwj12120-cit-0030',
                 'volume': '16',
                 'year': '2008'},
                {'DOI': '10.1038/jid.2008.405',
                 'article-title': 'Chemokine-mediated migration of '
                                  'skin-derived stem cells: predominant role '
                                  'for CCL5/RANTES',
                 'author': 'Kroeze',
                 'doi-asserted-by': 'crossref',
                 'first-page': '1569',
                 'journal-title': 'J Invest Dermatol',
                 'key': '10.1111/iwj.12120-BIB0031|iwj12120-cit-0031',
                 'volume': '129',
                 'year': '2009'},
                {'DOI': '10.1007/s00403-009-1011-1',
                 'article-title': 'Protease and pro-inflammatory cytokine '
                                  'concentrations are elevated in chronic '
                                  'compared to acute wounds and can be '
                                  'modulated by collagen type I in vitro',
                 'author': 'Wiegand',
                 'doi-asserted-by': 'crossref',
                 'first-page': '419',
                 'journal-title': 'Arch Dermatol Res',
                 'key': '10.1111/iwj.12120-BIB0032|iwj12120-cit-0032',
                 'volume': '302',
                 'year': '2010'},
                {'DOI': '10.1007/s00109-008-0378-3',
                 'article-title': 'IKK-2 is required for TNF-alpha-induced '
                                  'invasion and proliferation of human '
                                  'mesenchymal stem cells',
                 'author': 'Bocker',
                 'doi-asserted-by': 'crossref',
                 'first-page': '1183',
                 'journal-title': 'J Mol Med (Berl)',
                 'key': '10.1111/iwj.12120-BIB0033|iwj12120-cit-0033',
                 'volume': '86',
                 'year': '2008'},
                {'DOI': '10.1046/j.1524-475X.1993.10308.x',
                 'article-title': 'Inhibition of cell proliferation by chronic '
                                  'wound fluid',
                 'author': 'Bucalo',
                 'doi-asserted-by': 'crossref',
                 'first-page': '181',
                 'journal-title': 'Wound Repair Regen',
                 'key': '10.1111/iwj.12120-BIB0034|iwj12120-cit-0034',
                 'volume': '1',
                 'year': '1993'},
                {'DOI': '10.1016/S0741-5214(99)70113-8',
                 'article-title': 'The proliferative capacity of neonatal skin '
                                  'fibroblasts is reduced after exposure to '
                                  'venous ulcer wound fluid: a potential '
                                  'mechanism for senescence in venous ulcers',
                 'author': 'Mendez',
                 'doi-asserted-by': 'crossref',
                 'first-page': '734',
                 'journal-title': 'J Vasc Surg',
                 'key': '10.1111/iwj.12120-BIB0035|iwj12120-cit-0035',
                 'volume': '30',
                 'year': '1999'},
                {'DOI': '10.1126/science.2683075',
                 'article-title': 'G1 events and regulation of cell '
                                  'proliferation',
                 'author': 'Pardee',
                 'doi-asserted-by': 'crossref',
                 'first-page': '603',
                 'journal-title': 'Science',
                 'key': '10.1111/iwj.12120-BIB0036|iwj12120-cit-0036',
                 'volume': '246',
                 'year': '1989'},
                {'DOI': '10.1111/j.0022-202X.2004.23557.x',
                 'article-title': 'Chronic wound fluid suppresses '
                                  'proliferation of dermal fibroblasts through '
                                  'a Ras-mediated signaling pathway',
                 'author': 'Seah',
                 'doi-asserted-by': 'crossref',
                 'first-page': '466',
                 'journal-title': 'J Invest Dermatol',
                 'key': '10.1111/iwj.12120-BIB0037|iwj12120-cit-0037',
                 'volume': '124',
                 'year': '2005'},
                {'article-title': 'The anaerobic and aerobic microbiology of '
                                  'wounds: a review',
                 'author': 'Bowler',
                 'first-page': '170',
                 'journal-title': 'Wounds',
                 'key': '10.1111/iwj.12120-BIB0038|iwj12120-cit-0038',
                 'volume': '10',
                 'year': '1998'},
                {'DOI': '10.1111/1523-1747.ep12583377',
                 'article-title': 'Staphylococcal toxins and protein A '
                                  'differentially induce cytotoxicity and '
                                  'release of tumor necrosis factor-alpha from '
                                  'human keratinocytes',
                 'author': 'Ezepchuk',
                 'doi-asserted-by': 'crossref',
                 'first-page': '603',
                 'journal-title': 'J Invest Dermatol',
                 'key': '10.1111/iwj.12120-BIB0039|iwj12120-cit-0039',
                 'volume': '107',
                 'year': '1996'},
                {'DOI': '10.1016/j.phrs.2008.06.004',
                 'article-title': 'Oxidative stress in normal and impaired '
                                  'wound repair',
                 'author': 'Schafer',
                 'doi-asserted-by': 'crossref',
                 'first-page': '165',
                 'journal-title': 'Pharmacol Res',
                 'key': '10.1111/iwj.12120-BIB0040|iwj12120-cit-0040',
                 'volume': '58',
                 'year': '2008'},
                {'article-title': 'Oxygen free radicals and wound healing',
                 'author': 'White',
                 'first-page': '473',
                 'journal-title': 'Clin Plast Surg',
                 'key': '10.1111/iwj.12120-BIB0041|iwj12120-cit-0041',
                 'volume': '17',
                 'year': '1990'},
                {'DOI': '10.1097/00000637-199711000-00012',
                 'article-title': 'Oxygen free radicals impair wound healing '
                                  'in ischemic rat skin',
                 'author': 'Senel',
                 'doi-asserted-by': 'crossref',
                 'first-page': '516',
                 'journal-title': 'Ann Plast Surg',
                 'key': '10.1111/iwj.12120-BIB0042|iwj12120-cit-0042',
                 'volume': '39',
                 'year': '1997'},
                {'DOI': '10.1007/s00411-007-0096-1',
                 'article-title': 'UVB induced oxidative stress in human '
                                  'keratinocytes and protective effect of '
                                  'antioxidant agents',
                 'author': 'Jin',
                 'doi-asserted-by': 'crossref',
                 'first-page': '61',
                 'journal-title': 'Radiat Environ Biophys',
                 'key': '10.1111/iwj.12120-BIB0043|iwj12120-cit-0043',
                 'volume': '46',
                 'year': '2007'},
                {'DOI': '10.1371/journal.pone.0013839',
                 'article-title': 'Antioxidants protect keratinocytes against '
                                  'M. ulcerans mycolactone cytotoxicity',
                 'author': 'Gronberg',
                 'doi-asserted-by': 'crossref',
                 'first-page': 'e13839',
                 'journal-title': 'PLoS One',
                 'key': '10.1111/iwj.12120-BIB0044|iwj12120-cit-0044',
                 'volume': '5',
                 'year': '2010'},
                {'DOI': '10.1111/j.1751-1097.1999.tb08239.x',
                 'article-title': 'Apoptosis, the role of oxidative stress and '
                                  'the example of solar UV radiation',
                 'author': 'Pourzand',
                 'doi-asserted-by': 'crossref',
                 'first-page': '380',
                 'journal-title': 'Photochem Photobiol',
                 'key': '10.1111/iwj.12120-BIB0045|iwj12120-cit-0045',
                 'volume': '70',
                 'year': '1999'},
                {'article-title': 'In vivo skin antioxidant effect of a new '
                                  'combination based on a specific Vitis '
                                  'vinifera shoot extract and a '
                                  'biotechnological extract',
                 'author': 'Cornacchione',
                 'first-page': 's8',
                 'issue': '6 Suppl',
                 'journal-title': 'J Drugs Dermatol',
                 'key': '10.1111/iwj.12120-BIB0046|iwj12120-cit-0046',
                 'volume': '6',
                 'year': '2007'},
                {'DOI': '10.1016/j.jss.2008.04.023',
                 'article-title': 'The role of vascular endothelial growth '
                                  'factor in wound healing',
                 'author': 'Bao',
                 'doi-asserted-by': 'crossref',
                 'first-page': '347',
                 'journal-title': 'J Surg Res',
                 'key': '10.1111/iwj.12120-BIB0047|iwj12120-cit-0047',
                 'volume': '153',
                 'year': '2009'},
                {'DOI': '10.1016/S0002-9440(10)63754-6',
                 'article-title': 'Topical vascular endothelial growth factor '
                                  'accelerates diabetic wound healing through '
                                  'increased angiogenesis and by mobilizing '
                                  'and recruiting bone marrow-derived cells',
                 'author': 'Galiano',
                 'doi-asserted-by': 'crossref',
                 'first-page': '1935',
                 'journal-title': 'Am J Pathol',
                 'key': '10.1111/iwj.12120-BIB0048|iwj12120-cit-0048',
                 'volume': '164',
                 'year': '2004'},
                {'DOI': '10.1097/01.prs.0000173447.81513.7a',
                 'article-title': 'Effect of chronic wound exudates and '
                                  'MMP-2/-9 inhibitor on angiogenesis in vitro',
                 'author': 'Ulrich',
                 'doi-asserted-by': 'crossref',
                 'first-page': '539',
                 'journal-title': 'Plast Reconstr Surg',
                 'key': '10.1111/iwj.12120-BIB0049|iwj12120-cit-0049',
                 'volume': '116',
                 'year': '2005'},
                {'DOI': '10.1046/j.1524-475X.2002.10903.x',
                 'article-title': 'Ratios of activated matrix '
                                  'metalloproteinase-9 to tissue inhibitor of '
                                  'matrix metalloproteinase-1 in wound fluids '
                                  'are inversely correlated with healing of '
                                  'pressure ulcers',
                 'author': 'Ladwig',
                 'doi-asserted-by': 'crossref',
                 'first-page': '26',
                 'journal-title': 'Wound Repair Regen',
                 'key': '10.1111/iwj.12120-BIB0050|iwj12120-cit-0050',
                 'volume': '10',
                 'year': '2002'},
                {'DOI': '10.1016/j.biocel.2007.10.024',
                 'article-title': 'Metalloproteinases and their inhibitors: '
                                  'regulators of wound healing',
                 'author': 'Gill',
                 'doi-asserted-by': 'crossref',
                 'first-page': '1334',
                 'issue': '6-7',
                 'journal-title': 'Int J Biochem Cell Biol',
                 'key': '10.1111/iwj.12120-BIB0051|iwj12120-cit-0051',
                 'volume': '40',
                 'year': '2008'},
                {'DOI': '10.1007/s007920050116',
                 'article-title': 'Extrinsic protein stabilization by the '
                                  'naturally occurring osmolytes '
                                  'beta-hydroxyectoine and betaine',
                 'author': 'Knapp',
                 'doi-asserted-by': 'crossref',
                 'first-page': '191',
                 'journal-title': 'Extremophiles',
                 'key': '10.1111/iwj.12120-BIB0052|iwj12120-cit-0052',
                 'volume': '3',
                 'year': '1999'},
                {'DOI': '10.1186/1472-6750-7-82',
                 'article-title': 'Compatible solutes from hyperthermophiles '
                                  'improve the quality of DNA microarrays',
                 'author': 'Mascellani',
                 'doi-asserted-by': 'crossref',
                 'first-page': '82',
                 'journal-title': 'BMC Biotechnol',
                 'key': '10.1111/iwj.12120-BIB0053|iwj12120-cit-0053',
                 'volume': '7',
                 'year': '2007'}]),
 'reference-count': (1000001, <class 'int'>, 53),
 'references-count': (1000001, <class 'int'>, 53),
 'relation': (70628, <class 'dict'>, {'cites': []}),
 'score': (1000001, <class 'int'>, 1),
 'short-container-title': (394346, <class 'list'>, ['Int Wound J']),
 'short-title': (1400, <class 'list'>, ['EAPJMSE']),
 'source': (1000001, <class 'str'>, 'Crossref'),
 'standards-body': (6233,
                    <class 'dict'>,
                    {'acronym': 'BSI', 'name': 'BSI British Standards'}),
 'subject': (3051, <class 'list'>, ['Surgery', 'Dermatology']),
 'subtitle': (106937,
              <class 'list'>,
              ['Effects of hydroxyectoine on adipose-derived stem cells and '
               'keratinocytes in chronic wounds']),
 'title': (920820,
           <class 'list'>,
           ['Adipose-derived stem cells and keratinocytes in a chronic wound '
            'cell culture model: the role of hydroxyectoine']),
 'translator': (54,
                <class 'list'>,
                [{'affiliation': [],
                  'family': 'Abdul-Nour',
                  'given': 'Soraya Dib',
                  'sequence': 'first'}]),
 'type': (999876, <class 'str'>, 'journal-article'),
 'update-policy': (79705,
                   <class 'str'>,
                   'http://dx.doi.org/10.1007/springer_crossmark_policy'),
 'update-to': (1931,
               <class 'list'>,
               [{'DOI': '10.3109/15563650.2014.904045',
                 'label': 'Correction',
                 'type': 'correction',
                 'updated': {'date-parts': [[2014, 12, 29]],
                             'date-time': '2014-12-29T00:00:00Z',
                             'timestamp': {'$numberLong': '1419811200000'}}}]),
 'volume': (423500, <class 'str'>, '12')}
```

</details>