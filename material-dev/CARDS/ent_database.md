# READ ME

## Data

### Manual annotation

`prodigy ner.manual` recipe on `database_00_sm.json` with `--pattern ACC_NUM_patterns.jsonl` and `NAME_patterns.jsonl`

Datasets:

- `DATABASE_DATE_ner`
- `DATABASE_NAME_ner`, `DATABASE_NAME_ner_corr` (same but fix label name `DNAME` -> `NAME`)
- `DATABASE_ACC_NUM_ner`
- `DATABASE_ner`: merge of single label datasets (above)

Train a v0 `ner` model

Nb: `DATABASE_textcat_bin` used for data exploration/validation of cat

### Model Correct

`prodigy ner.correct` recipe on `database_00_lg.json`

Datasets:

- `DATABASE_ner.corr`
- `DATABASE_ner_0.1`: merge of `DATABASE_ner.corr` & `DATABASE_ner`

## Reproduce results

### Train & save model

```bash
cd models/database
python -m spacy train en en_database_0.1 data/train4spacy_01.json data/eval4spacy_01.json -p ner && cp -r en_database_0.1/model-best/ en_database_0.1 && rm -r en_database_0.1/model*
```

### Eval model

```bash
python -m spacy evaluate en_database_0.1/ data/eval4spacy_01.json -dp eval/ -R
cd $PROJECT_DIR && python cli/patcit-cli.py models eval spacy-model models/database/en_database_0.1
```

### Model performance

    NER Scores
                     p          r          f
    ACC_NUM  93.750000  92.307692  93.023256
    NAME     95.135135  90.721649  92.875989
    DATE     91.964286  91.964286  91.964286
    -------------------------------------
    ALL   93.853821  92.169657  93.004115

## v0.3-dev

### User guide

Var|Content|type
---|---|---
`npl_publn_id`| npl publication id from PATSTAT 2018b TLS 214 | str
`npl_biblio`| npl biblio (raw citation text) from PATSTAT 2018b TLS 214| str
`name`| name of the database | list
`date`| accession date | list
`acc_num`| accession number | list
`url`| url | list


The table can be used to create a BQ table



<details><summary>**Table schema**</summary>summary>

```json
[
{
    "description": "npl publication id from PATSTAT 2018b TLS 214",
    "name": "npl_publn_id",
    "type": "STRING",
    "mode": "REQUIRED"
},
{
    "description": "npl biblio (raw citation text) from PATSTAT 2018b TLS 214",
    "name": "npl_biblio",
    "type": "STRING",
    "mode": "NULLABLE"
},
{
	"description":"name of the database",
	"name": "name",
	"type": "STRING",
	"mode": "REPEATED"
},
{
	"description":"accession date",
	"name": "date",
	"type": "STRING",
	"mode": "REPEATED"
},
{
	"description":"accession number",
	"name": "acc_num",
	"type": "STRING",
	"mode": "REPEATED"
},
{
	"description":"url",
	"name": "url",
	"type": "STRING",
	"mode": "REPEATED"
}
]
```
</details>

### Developers guide

#### Extract data

```bash

python cli/patcit-cli.py bq export extract-category `npl-parsing.patcit.npl_021` DATABASE --staging-table `npl-parsing.tmp.tmp` --destination-uri "gs://npl-parsing/npl_ctype/npl_ctype_database_v021_*" --tls214-table `usptobias.patstat.tls214`

```

#### Serialize data

```bash

python cli/patcit-cli.py models process serialize "npl_ctype_database_v021_*.json.gz" --category DATABASE --model models/database/en_database_0.1 >> npl_database_v021_serialized.jsonl

```

Preview `npl_database_v021_serialized.jsonl`

```json
{"name": ["UNIPROT"], "date": ["24 July 2013", "2013-07-24"], "acc_num": ["R8LDU5"], "url": ["http://www.uniprot.org"], "npl_publn_id": "55375485", "npl_biblio": "ANONYMOUS: 'cas9 - CRISPR-associated endonuclease Cas9 - Bacillus cereus VD131 - cas9 gene & protein', UNIPROT DATABASE, 24 July 2013 (2013-07-24), XP055375485, Retrieved from the Internet <URL:http://www.uniprot.org/uniprot/R8LDU5> [retrieved on 20170523]"}
```
