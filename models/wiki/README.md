# READ ME

## Data

### `wikis_07022020`

```sql
WITH
  tmp AS (
  SELECT
    npl_publn_id,
    npl_biblio as text
  FROM
    `usptobias.patstat.tls214`
  WHERE
    LOWER(npl_biblio) LIKE "%wiki%")
SELECT
  *
FROM
  tmp
WHERE
  rand()<2500/106000
```

## Model


> **Hook for loading model with urls matcher custom component**

>See discussion on loading models saved with custom components

>- https://stackoverflow.com/questions/51412095/spacy-save-custom-pipeline
>- https://spacy.io/usage/processing-pipelines#custom-components

    ```python
    import spacy
    from cli.patcit_models_add import UrlsMatcher, UrlsHostname
    from spacy.language import Language
    Language.factories["urls_matcher"] = lambda nlp, **cfg: UrlsMatcher(nlp, **cfg)
    Language.factories["urls_hostname"] = lambda nlp, **cfg: UrlsHostname(nlp, **cfg)
    nlp = spacy.load("models/wiki/en_wiki_0.1")
    ```


## Protocol

### DATE

````shell script
prodigy ner.correct wikis_date_ner.corr_0 ../../database/en_database_0.1/ ../data/wiki_07022020.json --label DATE
````

Annotate 550

Note:
- when there are more than 1 date, usually the oldest is the date when the article was created, the most recent is the accession date and in-between (if any), this is the last modification date.
- Tag all dates except in "compact" form, `yyyymmdd`.

### ITEM

````shell script
prodigy ner.manual wikis_item_ner.corr_0 blank:en ../data/wiki_07022020.json --label ITEM
````

Annotate 570

## v0.x

### v0 (en with NER)

````shell script
prodigy db-merge wikis_item_ner.corr_0,wikis_date_ner.corr_0 wikis_ner.0
````

    Label   Precision   Recall   F-Score
    -----   ---------   ------   -------
    ITEM       80.682   89.873    85.030
    DATE       91.429   96.970    94.118


    Best F-Score   90.027
    Baseline       0.000

### V0.1 (v0 with urls custom components)

````shell script
python cli/patcit-cli.py models add url-components models/wiki/en_wiki_0 --dest models/wiki/en_wiki_0.1
````

> **Known limitations on urls**

>- sometimes `-` sould be a `_`
>- sometimes, the last character of a match should not be considered (e.g. `.`, `,`, etc)
>- sometimes there is a `&oldid=d+` at the end which makes the url invalid

### Generate data

````shell script
python cli/patcit-cli.py models process serialize models/wiki/data/npl_wiki_v021.jsonl --model models/wiki/en_wiki_0.1 --category WIKI >> models/wiki/data/npl_wiki_v021_serialized.jsonl
````
