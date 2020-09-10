# READ ME

## Results

var|	value| value
---|---|---
*Nb documents*|	203|  203
*Nb preds*|	534| 534
*Nb golds*|	343| 343
*Nb true positives*|	220| 230
*Nb false positives*|	314| 304
*Nb false negatives*|	123| 113
*Precision*|	**0.41**| **0.43**
*Recall*|	**0.64**| **0.67**
*Leniency*|	0| 20

<details><summary>More</details>

````shell script

 python cli/patcit-cli.py models evaluate grobid-intext validation/intext/bibref_detect/val_detect.jsonl validation/intext/bibref_detect/val_detect.gold.jsonl --leniency 0/20

````
</details>


## Data

### detect

#### `detect.jsonl`

Grobid detected BIBREF in shape for prodigy labeling (Grobid prediction correction)

<details><summary>More</summary>

````shell script
python cli/patcit-cli.py models data prep-spacy-sam --texts-file validation/intext/patent_detect/eval_texts_1590481723.csv --citations-file validation/intext/bibref_detect/processed_eval_texts_1590481723.csv --flavor bibrefs >> validation/intext/bibref_detect/tmp.jsonl
python cli/patcit-cli.py models data align-spans validation/intext/bibref_detect/tmp.jsonl  >> validation/intext/bibref_detect/detect.jsonl
rm validation/intext/bibref_detect/tmp.jsonl
````

````json
{"publication_number":"string", "text":"long-string", "spans":[{"start":"int","end":"int","label":"string"}]}
````

</details>



#### `val_detect.jsonl` & `val_detect.gold.jsonl`

Light-weight version of `detect.jsonl` ( resp `detect.gold.jsonl`) used for performance metrics computation.

> `val_detect.gold.jsonl` is the manually annotated sample of `detect.jsonl` (same lightweight format).

<details><summary>More</summary>

```shell script
jq '{publication_number,spans}' validation/intext/bibref_detect/detect.jsonl  -c >> `val_detect.jsonl`
```

````json
{"publication_number":"string", "spans":[{"start":"int","end":"int","label":"string"}]}
````

</details>





### Silver to gold

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
