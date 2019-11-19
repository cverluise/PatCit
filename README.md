[DOCDB]:https://www.epo.org/searching-for-patents/data/bulk-data-sets/docdb.html#tab-1
[user-guide]:user-guide/user-guide.md
[beta-db]:https://console.cloud.google.com/bigquery?project=npl-parsing&p=npl-parsing&d=patcit&t=beta&page=table
[v01-db]:https://console.cloud.google.com/bigquery?project=npl-parsing&p=npl-parsing&d=patcit&t=v01&page=table
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


# READ ME

## Worldwide Patent-to-Science Citations dataset

**What's in there?** We parse and consolidate the 40 million Non Patent Literature (NPL) citations reported in the [DOCDB][DOCDB] database. This is as simple as that and this is just a first step.

**What does it mean?** We extract bibliographic attributes (e.g. title, authors, journal, etc) from the free-form NPL citations reported in the [DOCDB][DOCDB] database. We match these attributes with the Crossref, Pubmed and Unpaywall databases. Hence, we are able to enrich the final output with additional attributes such as the DOI, the PMID and the open access url *inter allia*. 

**Give it a try!** We just released the v0.1 of the dataset. It includes the 40 million [DOCDB][DOCDB] NPL citations. It is open access and publicly available on Google Cloud BigQuery. No gatekeeper, no request time. Just click [here][v01-db]! and follow our [User Guide][user-guide]. For anyone having a smattering of SQL, we believe that this is the perfect environment to play with the data. 

**Data quality.** There a mainly 3 levels of quality. 

|Quality degree| Characterization| Share of the [DOCDB][DOCDB]|
|---|---|---|
|1|Matched with a Digital Object Identifier (DOI)| 29%|
|2|Parsed *at least* a document title (journal, conference, article), excl 1.| 43%|
|3|Neither 1. nor 2.| 28%|

And we can do even better! Quality will keep improving fast, [stay up to date](#update) and [contribute](#contribute).   

**License.** The dataset is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.

### Release

#### :new: v0.1

Full scale release. 40 million [DOCDB][DOCDB] NPL citations. Additional variables from crossref (abstract, subject and funders, see [#10][issue-10] for more).

Access the data [here][v01-db] and follow the [user-guide][user-guide]. 

#### Beta release (October 2019)

Sandbox for data tests and user feedbacks. Includes 100k NPL citations.  

Access the data [here][beta-db] and follow the [user-guide][user-guide].


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
 
**What's next?** Of course, we plan to keep improving the Worldwide Patent-to-Science Citations dataset. There is more! We are currently processing US patent full-texts to extract, parse and consolidate in-text patent and NPL citations. We are also planning to do it for other major patent offices. 

**Under the hood.** We build on two great open source libraries: [Grobid][grobid], a Machine Learning library for extracting, parsing and restructuring raw documents and [biblio-glutton][biblio-glutton], a framework dedicated to bibliographic information with a powerful bibliographical matching service. These services are articulated in an efficient data pipeline in the cloud to process up to 2 million citations per day. 

**Values.** 

1. Fresh data - Our full dataset will be released as soon as possible
2. Open source - Visit our GitHub, raise [issues][issues-create], request [features][issues-create] and contribute!
3. Worldwide data - We put a specific emphasis on releasing data with a large geographical scope to stimulate research on non-US countries.

## Team

This project is maintained by [G. de Rassenfosse][gder] ([@gderasse][gderasse]) and [C. Verluise][cver] ([@cverluise][cverluise]).
  



