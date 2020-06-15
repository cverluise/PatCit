# READ ME

## `detect.correct.jsonl`

````bash
python cli/patcit-cli.py models data prep-spacy-sam  --texts-file validation/intext/patent_detect/eval_texts_1590481723.csv --citations-file validation/intext/patent_detect/eval_citations_1590481723.csv >> validation/intext/patent_detect/tmp.jsonl
python cli/patcit-cli.py models data align-spans validation/intext/patent_detect/tmp.jsonl  >> validation/intext/patent_detect/detect.corr.jsonl
rm validation/intext/patent_detect/tmp.jsonl
````
