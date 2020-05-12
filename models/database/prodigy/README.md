# READ ME

## Manual annotation

`prodigy ner.manual` recipe on `database_00_sm.json` with `--pattern ACC_NUM_patterns.jsonl` and `NAME_patterns.jsonl`

Datasets:

- `DATABASE_DATE_ner`
- `DATABASE_NAME_ner`, `DATABASE_NAME_ner_corr` (same but fix label name `DNAME` -> `NAME`)
- `DATABASE_ACC_NUM_ner`
- `DATABASE_ner`: merge of single label datasets (above)

Train a v0 `ner` model

Nb: `DATABASE_textcat_bin` used for data exploration/validation of cat

## Model Correct

`prodigy ner.correct` recipe on `database_00_lg.json`

Datasets:

- `DATABASE_ner.corr`
- `DATABASE_ner_0.1`: merge of `DATABASE_ner.corr` & `DATABASE_ner`
