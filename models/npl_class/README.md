[doccano]:https://github.com/doccano/doccano

# READ ME

## Extract

#### `results-20200204-154633.csv`

We draw a random set of 10,000 NPL citations within the set of citations affected by issue 14 v0.1

```sql
WITH
  issue_14 AS (
  SELECT
    npl_publn_id
  FROM
    `npl-parsing.patcit.v01`
  WHERE
    14 IN UNNEST(Issues) )
SELECT
  issue_14.npl_publn_id,
  npl_biblio
FROM
  `usptobias.patstat.tls214` AS tls214,
  issue_14
WHERE
  issue_14.npl_publn_id=tls214.npl_publn_id
  and RAND()<10000/11130400

```


#### `results-20200223-114412.csv`

We draw a random set of 10,000 NPL citations within the set of citations which have no doi but are not affected by issue 14 in the v0.1

```sql
WITH
  issue_14 AS (
  SELECT
    npl_publn_id
  FROM
    `npl-parsing.patcit.v01`
  WHERE
    DOI IS NULL
    AND 14 NOT IN UNNEST(Issues) )
SELECT
  issue_14.npl_publn_id,
  npl_biblio
FROM
  `usptobias.patstat.tls214` AS tls214,
  issue_14
WHERE
  issue_14.npl_publn_id=tls214.npl_publn_id
  AND RAND()<10000/16770000

```


## Labelling


### Technology

[Doccano][doccano]


### Output

- `label-0200204-154633.csv`
- `label-20200223-114412.csv`

### Thanks

Francesco Gerotto

### Labelling guidelines

#### Bibliographical reference

*Includes but is not restricted to:*

- Journal
- Book
- Technical report
- Thesis dissertation

> /!\ Non latin-character based citations (chinese, japan, etc) should not be labelled. Even if they have a vol and/or num.

#### Office action

*Includes but is not restricted to:*

- Office action
- Response to office action
- Notice of allowance
- Office communication
- Invitation to pay additional fees
- Restriction requirements
- Invitation to pay additional fees

#### Patent

*Includes but is not restricted to:*

- Patent *without* any reference to an office action
- Patent translation *without*...
- Patent abstract *without*...
- Patent specification *without*...
- Patent chart
- Derwent patent abstract, DWPI, WPI

#### Search report

*Includes but is not restricted to:*

- Search report
- Written opinion
- Report of preliminary patentability
- Examiner interview

#### Litigation

*Includes but is not restricted to:*

- Inter Parte Review (IPR)
- Notice of opposition
- Patent litigation


#### Database

*Includes but is not restricted to:*

- EMBL
- Genebank
- Geneseq

#### Product Documentation

*Includes but is not restricted to:*

- Catalogue
- Brochure
- Product description
- Manual/user guide
- Commercial doc
- Product data sheet

#### Norms and standards

*Includes but is not restricted to:*

- ISO
- DIN
- 3GPP
- IETF
- RFC (Request for comments)


#### Web article/page

*Includes but is not restricted to:*

- Wikipedia
- Articles with web as primary source (except for product documentation)

#### Litigation

*Includes but is not restricted to:*

- IPR
- Petition
- Invalidity contention

#### Others

*Includes but is not restricted to:*

Mainly uncomplete citations

#### Na

- NEANT/...

## Models

Current solution is based on spaCy `textCategorizer` class. Specifically, a `ensemble` model to classify between the npl classes mentioned above (except for others.


### Usage

```
cd models/npl_class/
python train-textcat.py data/label*.csv --train-share .8 --spacy-model en_core_web_sm --model-path ./ --eval-path eval/
```

### Results

Overall performs well, in particular for crucial NPL classes.

Current classification pitfall: webpage and product documentation.


### Ideas

Research directions for future improvements include

- Thresholding
- Architecture (`bow` and `simple-cnn`)
- Add examples of under-represented classes
- Training data augmentations (e.g. generate examples from truncated npl_biblio)
