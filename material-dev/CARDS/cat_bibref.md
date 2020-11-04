# READ ME


## Data

#### `silver.jsonl`

json extract from `v01_UScontextual_Pat`

<details><summary>More</summary>

```json
{"publication_number_o":"US-2017233441-A1","DOI":"10.1126/science.1245625","ISSN":"0036-8075","ISSNe":"1095-9203","PMCID":"pmc3886632","PMID":"24179159","idno":null,"authors":[{"first":"J-P","middle":null,"surname":"Julien","genname":null}]}
```
</details>

#### `val_silver_to_gold.jsonl` & `val_silver_to_gold.gold.jsonl`

- `val_silver_to_gold.jsonl` formated for manual labeling
- `val_silver_to_gold.gold.jsonl` same with actual manual annotations (gold)

> `val_silver_to_gold.gold.jsonl` used for training classifier on top of Grobid predictions

<details><summary>More</summary>

```shell script
python pacit.py models data prep-bibref-silver-to-gold silver.jsonl >> silver_to_gold.jsonl
```

```json
{"text": "Gottfried Magerl In Ieee Transactions Of Microwave Theory And Techniques Entitled &#34;Ridged Waveguides Within Homogeneous Dielectric-Slab Loading&#34 1978-06 26"}
```
</details>

````shell script
prodigy data-to-spacy models/bibref-cat/data/train_silver_to_gold.json models/bibref-cat/data/dev_silver_to_gold.json -l en -tc silver_to_gold_BIBREF -es .2
````

## Model training

````shell script
spacy train en models/bibref-cat/bibref-cat models/bibref-cat/data/train_silver_to_gold.json models/bibref-cat/data/dev_silver_to_gold.json --pipeline textcat -TML --version 0.0
````

**Results**

ROC-AUC: 0.935

## Thresholding

````shell script
python cli/patcit_models_finetune.py  models/bibref-cat/data/dev_silver_to_gold.json models/bibref-cat/bibref-cat_0.0 --label "BIBREF" --exante-prec .45 --exante-rec .67
````

**Results**

Best threshold:0.556

r|p|f1
---|---|---
0.609| 0.809| 0.702
