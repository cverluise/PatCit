# READ ME

## `detect.corr.jsonl`

````shell script
python cli/patcit-cli.py models data prep-spacy-sam --texts-file validation/intext/patent_detect/eval_texts_1590481723.csv --citations-file validation/intext/bibref_detect/processed_eval_texts_1590481723.csv --flavor bibrefs >> validation/intext/bibref_detect/tmp.jsonl
python cli/patcit-cli.py models data align-spans validation/intext/bibref_detect/tmp.jsonl  >> validation/intext/bibref_detect/detect.corr.jsonl
rm validation/intext/bibref_detect/tmp.jsonl
````
