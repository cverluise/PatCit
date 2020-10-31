[DOCDB]:https://www.epo.org/searching-for-patents/data/bulk-data-sets/docdb.html#tab-1
[grobid]:https://github.com/kermitt2/grobid
[biblio-glutton]:https://github.com/kermitt2/biblio-glutton
[issues-create]:https://github.com/cverluise/SciCit/issues/new/choose
[issues]:https://github.com/cverluise/SciCit/issues
[good-first-issue]:https://github.com/cverluise/SciCit/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22
[help-wanted]:https://github.com/cverluise/SciCit/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22
[gbq-quickstart]:https://cloud.google.com/bigquery/docs/quickstarts/quickstart-web-ui
[gderasse]:https://github.com/gderasse
[gder]:http://www.gder.info/
[cverluise]:https://github.com/cverluise
[cver]:https://cverluise.github.io/
[nl]:https://tinyletter.com/patcit
[doc-website]:https://cverluise.github.io/PatCit/
[bq-patcit]:https://console.cloud.google.com/bigquery?project=brv-patent&p=npl-parsing&d=patcit&page=dataset
[gs-patcit]:https://console.cloud.google.com/storage/browser/patcit?forceOnBucketsSortingFiltering=false&project=npl-parsing&userProject=npl-parsing
[zen-patcit]:https://zenodo.org/record/3710994#.Xm_uE5NKhEI
[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg?label=Data

<a href="https://cverluise.github.io/PatCit/"><img src="https://github.com/cverluise/PatCit/blob/master/dissemination/logo-250x250.jpeg" width="125" height="125" align="right" /></a>

# PatCit: Making Patent Citations Uncool Again

[Website][doc-website], [Newsletter][nl], [BigQuery][bq-patcit], [G-Storage][gs-patcit], [Zenodo][zen-patcit]

![](https://img.shields.io/github/license/cverluise/PatCit?label=Code) [![CC BY 4.0][cc-by-shield]][cc-by] ![](https://img.shields.io/github/last-commit/cverluise/PatCit)

Patents are at the crossroads of many innovation nodes: science, industry, products, competition, etc. Such interactions can be identified through citations *in a broad sense*.

It is now common to use patent-to-patent citations to study some aspects of the innovation system. However, **there is much more buried in the Non Patent Literature (NPL) citations and in the patent text itself**. For instance, patent texts can contain citations to patents, bibliographical references, softwares, databases, products, etc. Similarly, NPL citations point to bibliographical references, office actions, patents, search reports, webpages, norm & standards, product documentations, databases and litigation documents.

Good news, Natural Language Processing (NLP) tools now enable social scientists to excavate and structure this long hidden information. **That's the purpose of this project**.

## Achievements

So far, we have:

1. **classified** the 40 million NPL citations reported in the **DOCDB** database in 9 distinct research oriented classes with a 90% accuracy rate.<sup>1</sup>
2. **parsed** and **consolidated** the 27 million **NPL** citations classified as bibliographical references.

	<details>

	>ℹ From the 27 million bibliographical references:
	>
	> 1. 11 million (40%) were matched with a **DOI** with a 99% **precision** rate
	> 2. the main bibliographic attributes were parsed with **accuracy** rates ranging between 71% and 92% for the remaining 16 million (60%)

	</details>

3. **extracted**, **parsed** and **consolidated** in-text bibliographical references and patent citations from the body of all time USPTO patents.

	<details>

	>ℹ From the 16 million USPTO patents, we have:
	>
	> 1. **extracted** and **parsed** 70 million in-text bibliographical references and 80 million patent citations.
	> 2. found a **DOI** for 13+ million in-text bibliographical references (18%).

	</details>

> 💬 A detailed presentation of the current state of the project is available in our [March 2020 presentation](./dissemination/IIPP-CEMI_03032020.pdf).

## Features

#### Open

- The code is licensed under MIT-2 and the dataset is licensed under CC-BY. Two highly permissive licenses.
- The project is thought to be *dynamically improved by and for the community*. Anyone should feel free to open discussions, raise issues, request features and contribute to the project.

#### Comprehensive

- We address *worldwide patents*, as long as the data is available.
- We address *all classes of citations*<sup>1</sup>, not only bibliographical references.
- We address front-page and in-text citations.

#### Highest standards

- We use and implement state-of-the art machine learning solutions.
- We take great care to implement only the most efficient solutions. We believe that computational resources should be used sparsely, for both environmental sustainability and long term financial sustainability of the project.



## Data access

The `PatCit` dataset is licensed under Creative Commons Attribution International 4.0 [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/).

#### Explore in BigQuery

The `PatCit` dataset is publicly available on Google Cloud BigQuery (GBQ). Follow the [link][bq-patcit]! For those who have a smattering of SQL, we believe that this is the perfect environment to play with the data.

> 💡 If you are new to GCP and want to learn the basics of Google BigQuery (GBQ), you can take the GBQ [Quickstart][gbq-quickstart]. This should not take more than 2 minutes and might help a lot !


#### Download from Google Cloud Storage - *recommended*


This is the best way to experiment a customizable, smooth and resilient download process. We will make sure that the latest version of the dataset is always available on the [gs://patcit][gs-patcit] bucket.


```bash
gsutil  -u <your-billing-project> \ # specify your billing project
-m cp -r gs://patcit/ <your/destination/folder-or-uri>
```


> 💡 You can download a specific subset of the dataset by specifying the source folder. E.g. `gs://patcit/npl/json` (instead of `gs://patcit`) will get you only the latest version of the `npl` dataset in its json version.

#### Download from Zenodo

The dataset can also be downloaded from Zenodo. Follow the [link][zen-patcit]!

> 💡 Versions of the dataset will be archived on Zenodo as of `v0.15-patcit`.


## Keep me updated


PatCit is a fast moving and fast improving project. Make sure that you are aware of the project most recent developments.


### Join our mail diffusion list

Click [here][nl], that's as simple as that.

<small>Expect 1 mail every 2 months. You can unsubscribe at any moment. We won't sell your information, ever.</small>

### Follow the `PatCit` project on GitHub

- ![](https://img.shields.io/github/stars/cverluise/PatCit?style=social): GitHub users can star the project repository. Project updates will be automatically added to their GitHub news feed.
- ![](https://img.shields.io/github/watchers/cverluise/PatCit?style=social): involved users and contributors are also invited to "watch" the project repository. They will be notified of releases, conversations, etc.



## By and for the community


#### Help us improve.
We want to make this dataset truly useful to the community. We are thus very happy for feedback.

#### Let's grow the community.
We believe that discussions are much more valuable if they are publicly shared, so that more people can benefit from it. Hence, we strongly encourage you to share your feedback on our GitHub repository [issue][issues] section.

#### Want to contribute?
Even better! We will be more than happy to receive any contributions from you and the community. We have already started to tag some [issues][issues-create] with [`good first issue`][good-first-issue] and [`help wanted`][help-wanted]. Ready? You can start as of now! Let's do it all together.

<a name="contribute"></a>

## Under the hood.

We build on large range of open-source tools. In particular, the project heavily relies on two great open source libraries:

- [Grobid][grobid], a Machine Learning library for extracting, parsing and restructuring raw documents
- [biblio-glutton][biblio-glutton], a framework dedicated to bibliographic information with a powerful bibliographical matching service.

These services are articulated in an efficient data pipeline in the cloud to process up to 2 million citations per day.


## :hugging_face: Team

This project is initiated by [G. de Rassenfosse][gder] ([@gderasse][gderasse]) and [C. Verluise][cver] ([@cverluise][cverluise]).

It has benefited from many contributions and helpful comments carefully recorded in [CRediT][./CRediT].

## Citation

```bibtex
@dataset{gaetan_de_rassenfosse_2020_3710994,
  author       = {Gaétan de Rassenfosse and Cyril Verluise},
  title        = {{PatCit: A Comprehensive Dataset of Patent Citations}},
  month        = mar,
  year         = 2020,
  publisher    = {Zenodo},
  version      = {0.15},
  doi          = {10.5281/zenodo.3710994},
  url          = {https://doi.org/10.5281/zenodo.3710994}
}
```

---

<sup>1</sup>  Bibliographical reference, office action, patent, search report, webpage, norm & standard, product documentation, database and litigation
