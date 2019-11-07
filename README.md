[DOCDB]:https://www.epo.org/searching-for-patents/data/bulk-data-sets/docdb.html#tab-1
[user-guide]:user-guide/user-guide.md
[beta-db]:https://console.cloud.google.com/bigquery?project=npl-parsing&p=npl-parsing&d=patcit&t=beta&page=table
[grobid]:https://github.com/kermitt2/grobid
[biblio-glutton]:https://github.com/kermitt2/biblio-glutton
[issues-create]:https://github.com/cverluise/SciCit/issues/new/choose
[issues]:https://github.com/cverluise/SciCit/issues
[polls]:https://github.com/cverluise/SciCit/issues?q=is%3Aissue+is%3Aopen+label%3APolls
[good-first-issue]:https://github.com/cverluise/SciCit/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22
[help-wanted]:https://github.com/cverluise/SciCit/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22
[gderasse]:https://github.com/gderasse
[gder]:http://www.gder.info/
[cverluise]:https://github.com/cverluise
[cver]:https://cverluise.github.io/


# READ ME

## Worldwide Patent-to-Science Citations dataset

### :rocket: Beta release (October 2019)

We have released a beta version of our novel Worldwide Patent-to-Science Citations dataset in. We hope that you will enjoy the database as much as we enjoy creating and improving it!

 
**What's in there for me?** We parse and consolidate the 40 million Non Patent Literature (NPL) citations reported in the [DOCDB][DOCDB] database. This is as simple as that and this is just a first step.

**What does it mean?** We extract bibliographic attributes (e.g. title, authors, journal, etc) from the free-form NPL citations reported in the [DOCDB][DOCDB] database. We match these attributes with the Crossref, Pubmed and Unpaywall databases. Hence, we are able to enrich the final output with additional attributes such as the DOI, the PMID and the open access url *inter allia*. 

**Give it a try!** We just released a beta version of the dataset. It includes 100k NPL citations. It is publicly available on Google Cloud BigQuery. Just click [here][beta-db]! and follow our [User Guide][user-guide].  For anyone having a smattering of SQL, we believe that this is the perfect environment to play with the data. 
 
**Help us improve.** We want to make this dataset truly useful to the community. We are thus very happy for feedback. Our most pressing questions include: 

1. Your ideal level of [documentation][issues-create]
2. Any recommendations to make the dataset more user-friendly  
3. Information on any recurrent mistake in the data 
4. Your [feature requests][issues-create] to meet your use-case
5. :new: Your vote in the [polls][polls] we have created for you
 
**Let's grow the community.** We believe that these discussions are much more valuable if they are publicly shared, so that more people can benefit from it. Hence, we strongly encourage you to share your feedback on our GitHub repository [issue][issues] section. 

**Don't want to miss any updates?** Give us a :star:

### Tell me more 

Still reading? Curious? We tell you more!
 
**What's next?** We plan to release the full database - hopefully integrating your feedback - in the course of November. There is more! We are currently processing US patent full-texts to extract, parse and consolidate in-text patent and NPL citations. We are also planning to do it for other major patent offices. 

**Under the hood.** We build on two great open source libraries: [Grobid][grobid], a Machine Learning library for extracting, parsing and restructuring raw documents and [biblio-glutton][biblio-glutton], a framework dedicated to bibliographic information with a powerful bibliographical matching service. These services are articulated in an efficient data pipeline in the cloud to process up to 2 million citations per day. 

**Values.** 

1. Fresh data - Our full dataset will be released as soon as possible
2. Open source - Visit our GitHub, raise [issues][issues-create], request [features][issues-create] and contribute!
3. Worldwide data - We put a specific emphasis on releasing data with a large geographical scope to stimulate research on non-US countries.

## Team

This project is maintained by [G. de Rassenfosse][gder] ([@gderasse][gderasse]) and [C. Verluise][cver] ([@cverluise][cverluise]).

We will be more than happy to receive any contributions from the community and have already started to tag some [issues][issues-create] with [`good first issue`][good-first-issue] and [`help wanted`][help-wanted] tags so that you can start as of now!   



