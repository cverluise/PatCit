[DOCDB]:https://www.epo.org/searching-for-patents/data/bulk-data-sets/docdb.html#tab-1
[user-guide]:user-guide/user-guide.md
[db]:https://console.cloud.google.com/bigquery?project=npl-parsing&p=npl-parsing&d=patcit&page=dataset


# VERSIONS

## v0.1 Patent Contextual Citations dataset (December 2019)

Extends the Beta to all USTPO patents (all-time)

### Beta (November 2019)

Sandbox for data tests and user feedbacks. Includes 250k US Patents.

Access the data [here][db] (tables *beta\_contextualNPL* and *beta\_contextualPat*) and follow the [user-guide][user-guide].


## Worldwide Patent-to-Science Citations dataset

### v0.2 (March 2020)

- Add `npl_class`
- Propagate `ISSN` based on `title_j` (+1.8 million)

### v0.1 (November 2019)

Full scale release. 40 million [DOCDB][DOCDB] NPL citations. Additional variables from crossref (abstract, subject and funders, see [#10][issue-10] for more).

Access the data [here][db] (tables *v01*) and follow the [user-guide][user-guide].

### Beta (October 2019)

Sandbox for data tests and user feedbacks. Includes 100k NPL citations.

*Deprecated*
