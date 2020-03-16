[gs-quickstart]:https://cloud.google.com/storage/docs/quickstarts-console
[gs-patcit]:https://console.cloud.google.com/storage/browser/patcit/
[zen-patcit]:https://zenodo.org/record/3710994#.Xm_uE5NKhEI
[^nest]:E.g. there are many authors with a name, surname, a gender name, etc for a unique publication
[^zen]:Zenodo is a general-purpose open-access repository developed under the European OpenAIRE program and operated by CERN

## Before you start

#### Dataset structure

The PatCit dataset has the following structure:

```bash
📁 patcit
├── 📝 README.md
├── 📁 npl
│   ├── 📁 csv
│   └── 📁 json
└── 📁 intext
    ├── 📁 csv
    └── 📁 json
```

where:

- `npl` refers to the front-page NPL citations data
- `intext` refers to the in-text citations data

#### Data format

Each sub-dataset is available in 2 flavors:

- newline delimited `json` - *recommended*
- `csv`

!!! info "`json` or `csv`?"

    Bibliographical data include fundamentally nested variables[^nest]. That's why we recommend the `json` format. Note also that any modern data management platform supports `json` formats. We provide the schema of the dataset to make sure that you can easily load it in this format.

    We are also aware that some users might be used to `csv` and relational databases. We thus provide the dataset in this flavor although we believe that it implies overhead time-costs.

#### Additional information

Each sub-folder (e.g. `patcit/npl/json`) contains a specific `README*.md` file which will give you additional information on how to load and use it.

## Download from Google Cloud Storage - <small>*recommended*</small>

??? tip "Google Storage Quickstart"
    If you are new to GCP and want to learn the basics of Google Storage (the storage service of GCP), you can take the
    Google Storage [Quickstart][gs-quickstart]. This should not take more than 2 minutes and might help a lot !

This is the best way to experiment a customizable, smooth and resilient download process. We will make sure that the latest version of the dataset is always available on the [gs://patcit][gs-patcit] bucket.


```bash
gsutil  -u <your-billing-project> \ # specify your billing project
-m cp -r gs://patcit/ <your/destination/folder-or-uri>
```

!!! info
    You can download a specific subset of the dataset by specifying the source folder. E.g. `gs://patcit/npl/json` (instead of `gs://patcit`) will get you only the latest version of the `npl` dataset in its json version.

## Download from Zenodo

The dataset can also be downloaded from Zenodo[^zen]. Follow the [link][zen-patcit]!

!!! info "PatCit versioning on Zenodo"
    Older versions of the dataset will be archived on Zenodo as of `v0.15`.
