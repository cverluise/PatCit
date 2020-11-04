## Model

Current classifier is based on spaCy `textCategorizer` class. Specifically, a `ensemble` model to classify between the npl classes mentioned above (except for `OTHERS`).

### Training

```bash
spacy train en models/npl-cat/npl_cat_npl_sm/ models/npl-cat/data/npl_cat_train.json models/npl-cat/data/npl_cat_dev.json --pipeline textcat --version 0.1
```

**Model specs**

- ensemble model (bow+cnn with bagging)
- spaCy embedding `sm`

**Training specs**

- trained on 4180 examples and evaluated on 1044 examples (hold-out)
- *augmented* training set specifically targeting:
   1. hard cases: we draw 1,000 samples where `v0.2` prediction failed (`UNKNOWN`)
   1. small classes: we draw 200 samples from the set of `npl_citations` classified in the class of interest by earlier version of the model (which includes errors)


### Results

- model: `en_cat_npl_sm`
- version: 0.1

|                           |      p |     r |     f |
|:--------------------------|-------:|------:|------:|
| DATABASE                  |  94.92 | 88.89 | 91.8  |
| OFFICE_ACTION             |  89.74 | 93.33 | 91.5  |
| WEBPAGE                   |  57.41 | 50    | 53.45 |
| NA                        | 100    | 50    | 66.67 |
| LITIGATION                |  93.33 | 84.34 | 88.61 |
| BIBLIOGRAPHICAL_REFERENCE |  84.55 | 92.77 | 88.47 |
| PATENT                    |  78.31 | 89.04 | 83.33 |
| NORM_STANDARD             |  87.5  | 71.01 | 78.4  |
| PRODUCT_DOCUMENTATION     |  66.96 | 62.6  | 64.71 |
| SEARCH_REPORT             |  96.3  | 87.64 | 91.76 |
| ***ALL (avg)***           |  -     | -     |***79.87***|


Overall performs well, in particular for crucial NPL classes. Current classification pitfalls: `WEBPAGE` and `PRODUCT_DOCUMENTATION`.

### Ideas

Research directions for future improvements include

- Architecture (`bow` and `simple-cnn`)
- Use sub-word embeddings
- Training data augmentations (e.g. generate examples from truncated `npl_biblio`)
- Active learning: label by hand examples with score close to threshold
