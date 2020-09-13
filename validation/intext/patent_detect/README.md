# READ ME

## Results


var|value
---|---
*Nb documents*|	153
*Nb preds*|	395
*Nb golds*|	467
*Nb true positives*|	385
*Nb false positives*|	10
*Nb false negatives*|	82
*Precision*|	**0.97**
*Recall*|	**0.82**
*Leniency*|	0

<details><summary>More</summary>

````shell script
 python cli/patcit-cli.py models evaluate grobid-intext validation/intext/patent_detect/val_detect.jsonl validation/intext/patent_detect/val_detect.gold.jsonl

````

</details>



## Data

#### `detect.jsonl`

Grobid detected `PAT` in shape for prodigy labeling (Grobid prediction correction)

<details><summary>More</summary>

````shell script
python cli/patcit-cli.py models data prep-spacy-sam  --texts-file validation/intext/patent_detect/eval_texts_1590481723.csv --citations-file validation/intext/patent_detect/eval_citations_1590481723.csv >> validation/intext/patent_detect/tmp.jsonl
python cli/patcit-cli.py models data align-spans validation/intext/patent_detect/tmp.jsonl  >> detect.jsonl
rm validation/intext/patent_detect/tmp.jsonl
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
