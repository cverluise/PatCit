# READ ME


## Data

````shell script
prodigy data-to-spacy models/bibref-cat/data/train_silver_to_gold.json models/bibref-cat/data/dev_silver_to_gold.json -l en -tc silver_to_gold_BIBREF -es .2
````

## Model training

````shell script
spacy train en models/bibref-cat/bibref-cat models/bibref-cat/data/train_silver_to_gold.json models/bibref-cat/data/dev_silver_to_gold.json --pipeline textcat -TML --version 0.0
````

**Results**

ROC-AUC: 0.935

## Thresholding

````shell script
python cli/patcit_models_finetune.py  models/bibref-cat/data/dev_silver_to_gold.json models/bibref-cat/bibref-cat_0.0 --label "BIBREF" --exante-prec .45 --exante-rec .67
````

**Results**

Best threshold:0.556

r|p|f1
---|---|---
0.609| 0.809| 0.702
