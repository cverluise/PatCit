# READ ME

## Results

 ~|orgname | doc number
---|---|---
*N* | 300| 300
*Accuracy*|0.98 | 0.96

## Data

#### `parsing.jsonl`

Data in shape for prodigy annotation (`ACCEPT`/`REJECT`) of parsed status.

<details><summary>More</summary>

```bash
python cli/patcit-cli.py models data contextualize-spans validation/intext/patent_detect/detect.corr.jsonl >> validation/intext/patent_parsing/parsing.jsonl
```

</details>
