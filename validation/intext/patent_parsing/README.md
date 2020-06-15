# READ ME

## `parsing.check.jsonl`

```bash
python cli/patcit-cli.py models data contextualize-spans validation/intext/patent_detect/detect.corr.jsonl >> validation/intext/patent_parsing/parsing.check.new.jsonl
```

## Validation

```bash
cd validation/intext/patent_parsing
prodigy parsing.check <attr>.parsing.check parsing.check.jsonl --attr <attr> -F recipe.py
```
