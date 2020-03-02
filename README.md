[DOCDB]:https://www.epo.org/searching-for-patents/data/bulk-data-sets/docdb.html#tab-1
[user-guide]:user-guide/user-guide.md
[db]:https://console.cloud.google.com/bigquery?project=npl-parsing&p=npl-parsing&d=patcit&page=dataset
[grobid]:https://github.com/kermitt2/grobid
[biblio-glutton]:https://github.com/kermitt2/biblio-glutton
[issues-create]:https://github.com/cverluise/SciCit/issues/new/choose
[issues]:https://github.com/cverluise/SciCit/issues
[polls]:https://github.com/cverluise/SciCit/issues?q=is%3Aissue+is%3Aopen+label%3APolls
[good-first-issue]:https://github.com/cverluise/SciCit/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22
[help-wanted]:https://github.com/cverluise/SciCit/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22
[issue-10]:https://github.com/cverluise/SciCit/issues/10
[gderasse]:https://github.com/gderasse
[gder]:http://www.gder.info/
[cverluise]:https://github.com/cverluise
[cver]:https://cverluise.github.io/
[v01]:https://console.cloud.google.com/bigquery?project=npl-parsing&p=npl-parsing&d=patcit&t=v01_npl&page=table
[v02]:https://console.cloud.google.com/bigquery?project=npl-parsing&p=npl-parsing&d=patcit&t=v02_npl&page=table
[beta-npl]:https://console.cloud.google.com/bigquery?project=npl-parsing&p=npl-parsing&d=patcit&t=beta_contextualNPL&page=table
[beta-pat]:https://console.cloud.google.com/bigquery?project=npl-parsing&p=npl-parsing&d=patcit&t=beta_contextualPat&page=table
[v01-npl]:https://console.cloud.google.com/bigquery?cloudshell=false&project=npl-parsing&p=npl-parsing&d=patcit&t=v01_UScontextualNPL&page=table
[v01-pat]:https://console.cloud.google.com/bigquery?cloudshell=false&project=npl-parsing&p=npl-parsing&d=patcit&t=v01_UScontextualPat&page=table
[US5914367A]:https://patents.google.com/patent/US5914367A/en


# READ ME

## Dataset


**License.** The dataset is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.


### :new: Worldwide NPL v0.2

**What's in there?** We parse and consolidate the 40 million Non Patent Literature (NPL) citations reported in the [DOCDB][DOCDB] database.


**Give it a try!** We just released the *[v0.2][v02]*. It builds on previous versions and adds a `npl_class` field which classifies the NPL publications in 9 different classes (bibliographical reference, office action, patent, search report, etc). We also extend the number of bibliographical reference with a ISSN (journal identifier) to 10.8 million (versus 8.9 million in v.01).

**Data quality**:

 - The classifier producing the `npl_class` achieves 89.9% accuracy
 - In the subset of bibliographical references (27.5 million), there are 3 main quality levels:

|Quality degree| Characterization| Share of the [DOCDB][DOCDB]|
|---|---|---|
|1|Matched with a Digital Object Identifier (DOI)| 40%|
|2|Parsed *at least* a document title (journal, conference, article), excl 1.| 40%|
|3|Neither 1. nor 2.| 20%|

 - When we match a DOI, this is the right one in 99% of the cases

And we can do even better! Quality will keep improving fast, [stay up to date](#update) and [contribute](#contribute).

### Patent Contextual Citations

**What's in there?** We extract, parse and consolidate *in-text* "patent-to-NPL" and "patent-to-patent" citations from patents description.

**Give it a try!** We just released the full US dataset. It includes the contextual NPL and patent   citations for all US patents.

**Data quality.** Data quality is under review. Any comments is most welcome. At this point, we know that we matched more than 13 million contextual NPL citations with a DOI. Overall, we extracted more than 70 million contextal NPL citations.


## In practice

### Data access

Our dataset is open access and publicly available on Google Cloud BigQuery. No gatekeeper, no request time. Plus, for anyone having a smattering of SQL, we believe that this is the perfect environment to play with the data.

Just follow this [link][db] and navigate to your favourite table!

|Data| Table (clickable link)|
|---|---|
|Worldwide NPL - v0.2| [v02][v02]|
|Worldwide NPL - v0.1| [v01][v01]|
|Patent-to-*NPL* Contextual Citations| [v01_UScontextualNPL][v01-npl]|
|Patent-to-*patent* Contextual Citations| [v01_UScontextualPat][v01-pat]|

Need a quickstart with BigQuery? Follow our [User Guide][user-guide].


### Vocabulary

Not sure to fully understand what we mean?

- **Extract**: We *detect* NPL and patent citations in plain text documents.

<details>
Let's consider an extract from [US5914367A][US5914367A]:

> "Another disadvantage of this process is that such modified enzymes usually show low solubility in organic solvents, thereby limiting the enzyme loading to about 0.02% by weight in the final polymer products. Sea Z. Yang, D. Williams, and A. J. Russell, J. Am. Chem. Soc., 1995, vol. 117, 4843. The solubilized enzyme of this process also shows lower activity (...)"

The extraction task consists in detecting the NPL citation

> "Z. Yang, D. Williams, and A. J. Russell, J. Am. Chem. Soc., 1995, vol. 117, 4843"

</details>

- **Parse**: We *structure* free-form NPL and patent citations into standard bibliographic attributes (e.g. title, authors, journal, etc).

<details>

Let's consider the following free-form NPL citation:

>"Z. Yang, D. Williams, and A. J. Russell, J. Am. Chem. Soc., 1995, vol. 117, 4843."

The parsing task consists in structuring this sequence into standardized bibliographical attributes, e.g.:

>- `Authors`: Z. Yang, D. Williams, A. J. Russell
>- `Journal`: J. Am. Chem. Soc.
>- `Date`: 1995
>- `Volume`: 117
>- `Page`: 4843

</details>

- **Consolidate**: We match the standardized bibliographical attributes with the Crossref, Pubmed and Unpaywall databases. Hence, we are able to enrich the final output with additional attributes such as the DOI, the PMID and the open access url *inter allia*.

<details>

Let's consider the following free-form NPL citation:

>"Z. Yang, D. Williams, and A. J. Russell, J. Am. Chem. Soc., 1995, vol. 117, 4843."

Matching it with Crossref, we can consolidate the bibliographical attribute found in the text with additional attributes, e.g.:

> - `Article title`: "Activity and Stability of Enzymes Incorporated into Acrylic Polymers"
> - `Journal title`: Journal of the American Chemical Society
> - `DOI`: 10.1021/ja00122a014
> - `ISSN`: 0002-7863

</details>



## By and for the community


**Help us improve.** We want to make this dataset truly useful to the community. We are thus very happy for feedback. Our most pressing questions include:

1. Your ideal level of [documentation][issues-create]
2. Any recommendations to make the dataset more user-friendly
3. Information on any recurrent mistake in the data
4. Your [feature requests][issues-create] to meet your use-case
5. :new: Your vote in the [polls][polls] we have created for you

**Let's grow the community.** We believe that these discussions are much more valuable if they are publicly shared, so that more people can benefit from it. Hence, we strongly encourage you to share your feedback on our GitHub repository [issue][issues] section.

**Don't want to miss any updates?** Give us a :star:
<a name="update"></a>

**Want to contribute?** Even better! We will be more than happy to receive any contributions from you and the community. We have already started to tag some [issues][issues-create] with [`good first issue`][good-first-issue] and [`help wanted`][help-wanted]. Ready? You can start as of now! Let's do it all together.

<a name="contribute"></a>

## Tell me more

Still reading? Curious? We tell you more!

**What's next?** We plan to keep improving the Worldwide Patent-to-Science Citations dataset in the coming months.

**Under the hood.** We build on two great open source libraries: [Grobid][grobid], a Machine Learning library for extracting, parsing and restructuring raw documents and [biblio-glutton][biblio-glutton], a framework dedicated to bibliographic information with a powerful bibliographical matching service. These services are articulated in an efficient data pipeline in the cloud to process up to 2 million citations per day.

**Values.**

1. Fresh data - Our full dataset will be released as soon as possible
2. Open source - Visit our GitHub, raise [issues][issues-create], request [features][issues-create] and contribute!
3. Worldwide data - We put a specific emphasis on releasing data with a large geographical scope to stimulate research on non-US countries.

## Team

This project is maintained by [G. de Rassenfosse][gder] ([@gderasse][gderasse]) and [C. Verluise][cver] ([@cverluise][cverluise]).
