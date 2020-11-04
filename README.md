<h1 align="center">patCit<img src="./patcit-logo.svg" height="25">
</h1>

<p align="center">
<img src="https://img.shields.io/badge/release-0.3.0-yellow">
<a href="https://cverluise.github.io/PatCit/">
<img alt="Documentation" src="https://img.shields.io/badge/website-online-brightgreen">
<img src="https://img.shields.io/badge/code-MIT-green">
<img src="https://img.shields.io/badge/data-CC%20BY%204.0-blue">
<a href="https://doi.org/10.5281/zenodo.3710993">
<img src="https://img.shields.io/badge/zenodo-0.3.0-darkblue">
</a>
<img src="https://img.shields.io/badge/models-dvc-purple">
</p>

<p align="center">
<img src="https://img.shields.io/github/forks/cverluise/PatCit?style=social">
<img src="https://img.shields.io/github/stars/cverluise/PatCit?style=social">
<img src="https://img.shields.io/github/forks/cverluise/PatCit?style=social">
</p>



<h3 align="center">
<p>Building a comprehensive dataset of patent citations
</h3>

[patcit-bq]:https://console.cloud.google.com/bigquery?project=patcit-public-data&p=patcit-public-data&page=project
[grobid]:https://github.com/kermitt2/grobid
[biblio-glutton]:https://github.com/kermitt2/biblio-glutton
[spacy]:https://github.com/explosion/spaCy
[patcit-academic]:https://docs.google.com/presentation/d/11COlz64EZn8PipXvnDBBZI_bnDD0fpm6tyx1_EqD6lU/edit?usp=sharing
[patcit-website]:https://cverluise.github.io/PatCit/
[patcit-newsletter]:https://tinyletter.com/patcit

👩‍🔬 Exploring the universe of patent citations has never been easier. No more complicated data set-up, memory issue and queries running for ever, we host [patCit on BigQuery][patcit-bq] for you.

🤗 patCit is community driven and benefits from the suppport of a reactive team who is eager happy to help and tackle your next request. This is where academics and industry practitioners meet.

🔮 patCit is based on state-of-the-art open source projects and libraries such as [grobid][grobid]/[biblio-glutton][biblio-glutton] and [spaCy][spacy]. Even better, patCit is continuously improving with the rest of its ecosystem.

🎓 Want to know more? Read patCit [academic presentation][patcit-academic] or dive into usage and technical guides on patCit [documentation website][patcit-website].

💌 Receive project updates in your mails/gitHub feed, join the [patCit newsletter][patcit-newsletter] and star the repository on gitHub.


## What will you find in patCit?

Patents are at the crossroads of many innovation nodes: science, open knwoledge, products, competition, etc. At patCit, we are building a *comprehensive* dataset of patent citations to help the community explore this *terra incognita*. patCit is:

- 🌎 worlwide coverage
- 📄 & 📚 front-page and in-text citations
- 🌈 all sorts of documents, not just scientific articles

> 💡 **How we do?** We use recent progress in Natural Language Processing (NLP) to extract and structure citations into actionable piece of information.

#### Front-page

[docdb]:https://www.epo.org/searching-for-patents/data/bulk-data-sets/docdb.html#tab-1

patCit builds on [DOCDB][docdb], the largest database of Non Patent Literature (NPL) citations. First, we deduplicate this corpus and organize it into 10 categories. Then, we design and apply category specific information extraction models using [spaCy][spacy]. Eventually, when possible, we enrich the data using external domain specific high quality databases.


Category|Classification (Million docs)|Information extraction|Enrichment|BigQuery table|Colab notebook|
----|----|----|----|----|----
Bibliographical reference|<p align="center">✅</p>|<p align="center">✅</p>|<p align="center">✅</p>|<p align="center"><a href="https://console.cloud.google.com/bigquery?project=patcit-public-data&p=patcit-public-data&d=frontpage&t=bibliographical_reference&page=table"><img  src="https://seeklogo.com/images/G/google-big-query-logo-AC63E7C329-seeklogo.com.png" width="55" height="20"></a></p>|<p align="center">🔜</p>
Office action|<p align="center">✅</p>||||
Patent|<p align="center">✅</p>||||
Search report|<p align="center">✅</p>||||
Product documentation|<p align="center">✅</p>||||
Norm & standard|<p align="center">✅</p>|<p align="center">✅</p>||<p align="center"><a href="https://console.cloud.google.com/bigquery?project=patcit-public-data&p=patcit-public-data&d=frontpage&t=norm_standard&page=table"><img  src="https://seeklogo.com/images/G/google-big-query-logo-AC63E7C329-seeklogo.com.png" width="55" height="20"></a></p>|[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cverluise/PatCit/blob/nightly/notebook/frontpage_normstandard.ipynb)
Webpage|<p align="center">✅</p>||||
Database|<p align="center">✅</p>|<p align="center">✅</p>||<p align="center"><a href="https://console.cloud.google.com/bigquery?project=patcit-public-data&p=patcit-public-data&d=frontpage&t=database&page=table"><img  src="https://seeklogo.com/images/G/google-big-query-logo-AC63E7C329-seeklogo.com.png" width="55" height="20"></a></p>|<p align="center">🔜</p>
Litigation|<p align="center">✅</p>||||
Wiki|<p align="center">✅</p>|<p align="center">✅</p>||<p align="center"><a href="https://console.cloud.google.com/bigquery?project=patcit-public-data&p=patcit-public-data&d=frontpage&t=wiki&page=table"><img  src="https://seeklogo.com/images/G/google-big-query-logo-AC63E7C329-seeklogo.com.png" width="55" height="20"></a></p>|[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cverluise/PatCit/blob/nightly/notebook/frontpage_wiki.ipynb)
*All*|<p align="center">✅</p>|<p align="center">NR</p>|<p align="center">✅</p>|<p align="center"><a href="https://console.cloud.google.com/bigquery?project=patcit-public-data&p=patcit-public-data&d=frontpage&t=all_meta&page=table"><img  src="https://seeklogo.com/images/G/google-big-query-logo-AC63E7C329-seeklogo.com.png" width="55" height="20"></a></p>|[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cverluise/PatCit/blob/nightly/notebook/frontpage_all.ipynb)



#### In-text

[google-ocr]:https://console.cloud.google.com/bigquery?project=patcit-public-data&p=patents-public-data&d=patents&t=publications&page=table
[google-matchapi]:https://patents.google.com/api/match

patCit builds on Google Patents corpus of [USPTO full-text patents][google-ocr]. First, we extract patent and bibliographical reference citations. Then, we parse detected in-text citations into a series of category dependent attributes using [grobid][grobid. Patent citations are matched with a standard publication number using the Google Patents [matching API][google-matchapi] and bibliographical references are matched with a DOI using [biblio-glutton][biblio-glutton]. Eventually, when possible, we enrich the data using external domain specific high quality databases.

Category|Citation extraction (Million docs)|Information extraction|Enrichment|BigQuery table|Colab notebook|
----|----|----|----|----|----
Bibliographical reference|<p align="center">✅</p>|<p align="center">✅</p>|<p align="center">✅</p>|<p align="center"><a href="https://console.cloud.google.com/bigquery?project=patcit-public-data&p=patcit-public-data&d=intext&t=bibliographical_reference&page=table"><img  src="https://seeklogo.com/images/G/google-big-query-logo-AC63E7C329-seeklogo.com.png" width="55" height="20"></a></p>|<p align="center">🔜</p>
Patents|<p align="center">✅</p>|<p align="center">✅</p>|<p align="center">✅</p>|<p align="center"><a href="https://console.cloud.google.com/bigquery?project=patcit-public-data&p=patcit-public-data&d=intext&t=patent&page=table"><img  src="https://seeklogo.com/images/G/google-big-query-logo-AC63E7C329-seeklogo.com.png" width="55" height="20"></a></p>|[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cverluise/PatCit/blob/nightly/notebook/intext_patent.ipynb)



## FAIR

[patcit-zenodo]:https://zenodo.org/record/3710994
[bq-quickstart]:https://cloud.google.com/bigquery/docs/quickstarts/quickstart-web-ui

📍 **Find** - The patCit dataset is available on [BigQuery][patcit-bq] in an interactive environment. For those who have a smattering of SQL, this is the perfect place to explore the data. It can also be downloaded on [Zenodo][patcit-zenodo].

> 👨‍🎓 If you are new to BigQuery and want to learn the basics of Google BigQuery (GBQ), you can take the GBQ [Quickstart][bq-quickstart]. This should not take more than 2 minutes and might help a lot !

📖 **Access** - We maintain a detailed documentation on how to access the data once you have found them on BigQuery or Zenodo. See usage notes on the patCit [documentation website][patcit-website].

🔀 **Interoperate** - Interoperability is at the core of patCit ambition. We take care to extract unique identifiers whenever it is possible to enable data enrichment for domain specific high quality databases. This includes the DOI, PMID and PMCID for bibliographical references, the Technical Doc Number for standards, the Accession Number for Genetic databases, the publication number for PATSTAT and Claims, etc. See specific table for more details.

🔂 **Reproduce** - You are at the right place. This gitHub repository is the project factory. You can learn more about data recipes and models on the patCit [documentation website][patcit-website].


## Contributing

[issue]:https://github.com/cverluise/SciCit/issues

There are many ways to contribute to patCit, many do not include coding.

**Give feedback** - We want to make patCit truly useful to the community. We are thus very happy for feedback.

**Share your thoughts** - We believe that discussions are much more valuable if they are publicly shared. This way, everyone can benefit from it. Hence, we strongly encourage you to share your issues and request on patCit GitHub repository [issue][issue] section.

**Feel like coding today?** - We will be more than happy to receive any contributions from you and the community. We have already started to tag some issues with [![good first issue](https://img.shields.io/badge/issue-good--first--issue-purple)](https://github.com/cverluise/SciCit/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) and [![help wanted](https://img.shields.io/badge/issue-help--wanted-turquoise)](https://github.com/cverluise/SciCit/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).



## Team
[credit]:./CRediT.md
[gabriele]:https://people.epfl.ch/gabriele.cristelli
[kyle]:https://scholar.google.com/citations?user=Ze-7kTYAAAAJ&hl=en
[tim]:http://people.bu.edu/tsimcoe/
[gaétan]:http://www.gder.info/
[cyril]:https://cverluise.github.io/


This project was initiated by [Gaétan de Rassenfosse][gaétan] (EPFL) and [Cyril Verluise][cyril] (Collège de France) in 2019.

Since then, it has benefited from the contributions of [Gabriele Cristelli][gabriele] (EPFL), Francesco Gerotto (Sciences Po), [Kyle Higham][kyle] (Hitsotsubashi University) and Lucas Violon (HEC Paris).

We are also thankful to Domenico Golzio for constant support and to [@leflix311](https://github.com/leflix311), [@kermitt2](https://github.com/kermitt2), [Tim Simcoe][tim] (Boston University) [@SuperMayo](https://github.com/SuperMayo) and [@wetherbeei](https://github.com/wetherbeei) for helpful comments.

Contribution details are available in [CRediT][credit].
