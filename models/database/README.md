# READ ME

## Reproduce results

### Train & save model

```bash
cd models/database
python -m spacy train en en_database_0.1 data/train4spacy_01.json data/eval4spacy_01.json -p ner && cp -r en_database_0.1/model-best/ en_database_0.1 && rm -r en_database_0.1/model*
```

### Eval model

```bash
python -m spacy evaluate en_database_0.1/ data/eval4spacy_01.json -dp eval/ -R
cd $PROJECT_DIR && python cli/patcit-cli.py models eval spacy-model models/database/en_database_0.1
```

### Model performance

    NER Scores
                     p          r          f
    ACC_NUM  93.750000  92.307692  93.023256
    NAME     95.135135  90.721649  92.875989
    DATE     91.964286  91.964286  91.964286
    -------------------------------------
    ALL   93.853821  92.169657  93.004115
