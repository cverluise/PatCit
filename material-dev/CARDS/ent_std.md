# CARD

## Training

```shell script
spacy train en models/en_ent_std_sm data/ent_std_train.json data/ent_std_test.json -p ner --version 0.3.0
```

## Results

|          |      p |      r |      f |
|:---------|-------:|-------:|-------:|
| WG       |  95.95 | 100    |  97.93 |
| MEETING  |  95.12 | 100    |  97.5  |
| DATE     |  94.14 |  95.9  |  95.01 |
| BODY     |  98.55 |  98.84 |  98.69 |
| TDOC_NUM | 100    |  94.92 |  97.39 |
| TECH     |  79.03 |  75.38 |  77.17 |
| TSG      |  98.92 |  95.83 |  97.35 |
| TYPE     |  99.28 |  99.28 |  99.28 |
| VERSION  |  94.44 |  94.44 |  94.44 |
| REF      | 100    | 100    | 100    |
|ALL   |96.27  |96.43  |96.35 |


Nb: no `TITLE` & `SOURCE`, later
