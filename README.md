[bq-patcit]:https://console.cloud.google.com/bigquery?project=patcit-public-data&p=patcit-public-data&page=project
[zen-patcit]:https://zenodo.org/record/3710994#.Xm_uE5NKhEI
[cc-by]: http://creativecommons.org/licenses/by/4.0/
<!-- Place this tag in your head or just before your close body tag. -->
<script async defer src="https://buttons.github.io/buttons.js"></script>

<p align="center">
    <br><font style="font-size:10vw">patCit</font>
    <svg width="40" height="40" viewBox="0 0 13 13" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 2C2.44772 2 2 2.44772 2 3V12C2 12.5523 2.44772 13 3 13H12C12.5523 13 13 12.5523 13 12V8.5C13 8.22386 12.7761 8 12.5 8C12.2239 8 12 8.22386 12 8.5V12H3V3L6.5 3C6.77614 3 7 2.77614 7 2.5C7 2.22386 6.77614 2 6.5 2H3ZM12.8536 2.14645C12.9015 2.19439 12.9377 2.24964 12.9621 2.30861C12.9861 2.36669 12.9996 2.4303 13 2.497L13 2.5V2.50049V5.5C13 5.77614 12.7761 6 12.5 6C12.2239 6 12 5.77614 12 5.5V3.70711L6.85355 8.85355C6.65829 9.04882 6.34171 9.04882 6.14645 8.85355C5.95118 8.65829 5.95118 8.34171 6.14645 8.14645L11.2929 3H9.5C9.22386 3 9 2.77614 9 2.5C9 2.22386 9.22386 2 9.5 2H12.4999H12.5C12.5678 2 12.6324 2.01349 12.6914 2.03794C12.7504 2.06234 12.8056 2.09851 12.8536 2.14645Z" fill="currentColor" fill-rule="evenodd" clip-rule="evenodd"></path></svg>
    <br>
<p>
<p align="center">
    <a>
        <img src="https://img.shields.io/badge/release-0.3.0-yellow">
    </a>
    <a href="https://cverluise.github.io/PatCit/">
        <img alt="Documentation" src="https://img.shields.io/badge/website-online-brightgreen">
    </a>
        <img src="https://img.shields.io/badge/code-MIT-green">
    <a>
        <img src="https://img.shields.io/badge/data-CC%20BY%204.0-blue">
    </a>
    <a href="https://doi.org/10.5281/zenodo.3710993">
        <img src="https://img.shields.io/badge/zenodo-0.3.0-darkblue">
    </a>
    <a>
        <img src="https://img.shields.io/badge/models-dvc-purple">
    </a>
</p>

<p align="center">
	<a class="github-button" href="https://github.com/cverluise/PatCit/subscription" data-icon="octicon-eye" data-show-count="true" aria-label="Watch cverluise/PatCit on GitHub">Watch</a>

	<a class="github-button" href="https://github.com/cverluise/PatCit" data-icon="octicon-star" data-show-count="true" aria-label="Star cverluise/PatCit on GitHub">Star</a>

	<a class="github-button" href="https://github.com/cverluise/PatCit/fork" data-icon="octicon-repo-forked" data-show-count="true" aria-label="Fork cverluise/PatCit on GitHub">Fork</a>
</p>



<h3 align="center">
<p>Building a comprehensive dataset of patent citations
</h3>


👩‍🔬 Exploring the universe of patent citations has never been easier. No more complicated data set-up, memory issue and queries running for ever, we host <a style="color:black" href="https://console.cloud.google.com/bigquery?project=patcit-public-data&p=patcit-public-data&page=project">patCit on BigQuery</a> for you.

🤗 patCit is community driven and benefits from the suppport of a reactive team who is eager happy to help and tackle your next request. This is where academics and industry practitioners meet.

🔮 patCit is based on state-of-the-art open source projects and libraries such as <a href="https://github.com/kermitt2/grobid" style="color:black">grobid</a>/<a href="https://github.com/kermitt2/biblio-glutton" style="color:black">biblio-glutton</a> and <a href="https://github.com/explosion/spaCy" style="color:black">spaCy</a>. Even better, patCit is continuously improving with the rest of its ecosystem.

🎓 Want to know more? Read patCit <a style="color:black" href="https://docs.google.com/presentation/d/11COlz64EZn8PipXvnDBBZI_bnDD0fpm6tyx1_EqD6lU/edit?usp=sharing">academic presentation</a> or dive into usage and technical guides on patCit <a style="color:black" href="https://cverluise.github.io/PatCit/">documentation website</a>.

💌 Receive project updates in your mails/gitHub feed, join the <a style="color:black" href="https://tinyletter.com/patcit">patCit newsletter</a> and star the repository on gitHub.


## What will you find in patCit?

Patents are at the crossroads of many innovation nodes: science, open knwoledge, products, competition, etc. At patCit, we are building a *comprehensive* dataset of patent citations to help the community explore this *terra incognita*. patCit is:

- 🌎 worlwide coverage
- 📄 & 📚 front-page and in-text citations
- 🌈 all sorts of documents, not just scientific articles

> 💡 **How we do?** We use recent progress in Natural Language Processing (NLP) to extract and structure citations into actionable piece of information.

#### Front-page

patCit builds on <a href="https://www.epo.org/searching-for-patents/data/bulk-data-sets/docdb.html#tab-1" style="color:black">DOCDB</a>, the largest database of Non Patent Literature (NPL) citations. First, we deduplicate this corpus and organize it into 10 categories. Then, we design and apply category specific information extraction models using <a href="https://github.com/explosion/spaCy" style="color:black">spaCy</a>. Eventually, when possible, we enrich the data using external domain specific high quality databases.

Category|Classification (Million docs)|Information extraction|Enrichment|BigQuery table|Colab notebook|
----|----|----|----|----|----
Bibliographical reference|<p align="center">✅</p>|<p align="center">✅</p>||<p align="center"><a href="https://console.cloud.google.com/bigquery?project=patcit-public-data&p=patcit-public-data&d=frontpage&t=bibliographical_reference&page=table"><img  src="https://seeklogo.com/images/G/google-big-query-logo-AC63E7C329-seeklogo.com.png" width="55" height="20"></a></p>|[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]()
Office action|<p align="center">✅</p>||||
Patent|<p align="center">✅</p>||||
Search report|<p align="center">✅</p>||||
Product documentation|<p align="center">✅</p>||||
Norm & standard|<p align="center">✅</p>|<p align="center">✅</p>||<p align="center"><a href="https://console.cloud.google.com/bigquery?project=patcit-public-data&p=patcit-public-data&d=frontpage&t=norm_standard&page=table"><img  src="https://seeklogo.com/images/G/google-big-query-logo-AC63E7C329-seeklogo.com.png" width="55"width="55" height="20"></a></p>|[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]()
Webpage|<p align="center">✅</p>||||
Database|<p align="center">✅</p>|<p align="center">✅</p>||<p align="center"><a href="https://console.cloud.google.com/bigquery?project=patcit-public-data&p=patcit-public-data&d=frontpage&t=database&page=table"><img  src="https://seeklogo.com/images/G/google-big-query-logo-AC63E7C329-seeklogo.com.png" width="55" height="20"></a></p>|[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]()
Litigation|<p align="center">✅</p>||||
Wiki|<p align="center">✅</p>|<p align="center">✅</p>||<p align="center"><a href="https://console.cloud.google.com/bigquery?project=patcit-public-data&p=patcit-public-data&d=frontpage&t=wiki&page=table"><img  src="https://seeklogo.com/images/G/google-big-query-logo-AC63E7C329-seeklogo.com.png" width="55" height="20"></a></p>|[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]()
*All*|<p align="center">✅</p>|<p align="center">NR</p>||<p align="center"><a href="https://console.cloud.google.com/bigquery?project=patcit-public-data&p=patcit-public-data&d=frontpage&t=all_meta&page=table"><img  src="https://seeklogo.com/images/G/google-big-query-logo-AC63E7C329-seeklogo.com.png" width="55" height="20"></a></p>|[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]()



#### In-text

patCit builds on Google Patents corpus of <a href="https://console.cloud.google.com/bigquery?project=patcit-public-data&p=patents-public-data&d=patents&t=publications&page=table" style="color:black">USPTO full-text patents</a>. First, we extract patent and bibliographical reference citations. Then, we parse detected in-text citations into a series of category dependent attributes using <a href="https://github.com/kermitt2/grobid" style="color:black">grobid</a>. Patent citations are matched with a standard publication number using the Google Patents <a href="https://patents.google.com/api/match" style="color:black">matching API</a> and bibliographical references are matched with a DOI using <a href="https://github.com/kermitt2/biblio-glutton" style="color:black">biblio-glutton</a>. Eventually, when possible, we enrich the data using external domain specific high quality databases.

Category|Citation extraction (Million docs)|Information extraction|Enrichment|BigQuery table|Colab notebook|
----|----|----|----|----|----
Bibliographical reference|<p align="center">✅</p>|<p align="center">✅</p>|<p align="center">✅</p>|<p align="center"><a href="https://console.cloud.google.com/bigquery?project=patcit-public-data&p=patcit-public-data&d=intext&t=bibliographical_reference&page=table"><img  src="https://seeklogo.com/images/G/google-big-query-logo-AC63E7C329-seeklogo.com.png" width="55" height="20"></a></p>|[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]()
Patents|<p align="center">✅</p>|<p align="center">✅</p>|<p align="center">✅</p>|<p align="center"><a href="https://console.cloud.google.com/bigquery?project=patcit-public-data&p=patcit-public-data&d=intext&t=patent&page=table"><img  src="https://seeklogo.com/images/G/google-big-query-logo-AC63E7C329-seeklogo.com.png" width="55" height="20"></a></p>|[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]()



## FAIR

📍 **Find** - The patCit dataset is available on <a style="color:black" href="https://console.cloud.google.com/bigquery?project=patcit-public-data&p=patcit-public-data&page=project">BigQuery</a> in an interactive enbironment. For those who have a smattering of SQL, this is the perfect place to explore the data. It can also be downloaded on <a style="color:black" href="https://zenodo.org/record/3710994">Zenodo</a>.

> 👨‍🎓 If you are new to BigQuery and want to learn the basics of Google BigQuery (GBQ), you can take the GBQ <a href="https://cloud.google.com/bigquery/docs/quickstarts/quickstart-web-ui" style="color:grey">Quickstart</a>. This should not take more than 2 minutes and might help a lot !

📖 **Access** - We maintain a detailed documetation on how to access the data once you have found them on BigQuery or Zenodo. See usage notes on the patCit <a href="https://cverluise.github.io/PatCit/" style="color:black">documentation website</a>.

🔀 **Interoperate** - Interoperability is at the core of patCit ambition. We take care to extract unique identifiers whenever it is possible to enable data enrichment for domain specific high quality databases. This includes the DOI, PMID and PMCID for bibliographical references, the Technical Doc Number for standards, the Accession Number for Genetic databases, the publication number for PATSTAT and Claims, etc. See specific table for more details.

🔂 **Reproduce** - You are at the right place. This gitHub repository is the project factory. You can learn more about data recipes and models on the patCit <a href="https://cverluise.github.io/PatCit/" style="color:black">documentation website</a>.


## Contributing

There are many ways to contribute to patCit, many do not include coding.

**Give feedback** - We want to make patCit truly useful to the community. We are thus very happy for feedback.

**Share your thoughts** - We believe that discussions are much more valuable if they are publicly shared. This way, everyone can benefit from it. Hence, we strongly encourage you to share your issues and request on patCit GitHub repository <a style="color:black" href="https://github.com/cverluise/SciCit/issues">issue</a> section.

**Feel like coding today?** - We will be more than happy to receive any contributions from you and the community. We have already started to tag some issues with [![good first issue](https://img.shields.io/badge/issue-good--first--issue-purple)](https://github.com/cverluise/SciCit/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) and [![help wanted](https://img.shields.io/badge/issue-help--wanted-turquoise)](https://github.com/cverluise/SciCit/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).



## Team

This project was initiated by <a style="color:black" href="http://www.gder.info/">Gaétan de Rassenfosse</a> (EPFL) and <a style="color:black" href="https://cverluise.github.io/">Cyril Verluise</a> (Collège de France) in 2019.

Since then, it has benefited from the contributions of Gabriele Cristelli (EPFL), Francesco Gerotto (Sciences Po), Kyle Higham (Hitsotsubashi University) and Lucas Violon (HEC Paris).

We are also thankful to Domenico Golzio for his constant support and to [@leflix311](https://github.com/leflix311), [@kermitt2](https://github.com/kermitt2), Tim Simcoe (Boston University) [@SuperMayo](https://github.com/SuperMayo) and [@wetherbeei](https://github.com/wetherbeei) for their helpful comments.

Contribution details are available in <a style="color:black" href="./CRediT.md">CRediT</a>.
