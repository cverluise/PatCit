### READ ME

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
