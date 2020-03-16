[US-5914367-A]:https://patents.google.com/patent/US5914367?oq=US5914367A
[^acc]:More at https://developers.google.com/machine-learning/crash-course/classification/accuracy
[^prec]:More at https://developers.google.com/machine-learning/crash-course/classification/precision-and-recall
[^docdb]:More at https://www.epo.org/searching-for-patents/data/bulk-data-sets/docdb.html#tab-1

#### Accuracy

Accuracy[^acc] is one metric for evaluating classification models. Informally, accuracy is the fraction of predictions our model got right. Formally, accuracy has the following definition:

$$
Accuracy=\frac{Number~of~correct~predictions}{Total~number~of~predictions}
$$

#### Consolidate

Match the standardized bibliographical attributes with high quality bibliographical databases. Enrich the final output with additional attributes such as the DOI, the PMID and the open access url inter allia.

??? example "In practice"
    Let's consider the following free-form NPL citation:

    > "Z. Yang, D. Williams, and A. J. Russell, J. Am. Chem. Soc., 1995, vol. 117, 4843."

    Matching it with Crossref, we can [**consolidate**](./vocabulary#consolidate) the bibliographical attributes found in the text with the following enriched attributes:

    >- `Article title`: "Activity and Stability of Enzymes Incorporated into Acrylic Polymers"
    >- `Journal title`: Journal of the American Chemical Society
    >- `DOI`: 10.1021/ja00122a014
    >- `ISSN: 0002-7863

#### Crossref

Crossref interlinks millions of items from a variety of content types, including journals, books, conference proceedings, working papers, technical reports, and data sets. Linked content includes materials from Scientific, Technical and Medical (STM) and Social Sciences and Humanities (SSH) disciplines.

#### EPO worldwide bibliographic data (DOCDB)
The EPO worldwide bibliographic data[^docdb] includes bibliographic data from over 90 countries worldwide. The data goes back as far as the 1830s for some patent authorities.


#### Digital Object Identifier (DOI)
A digital object identifier (DOI) is a persistent identifier or handle used to identify objects uniquely, standardized by the International Organization for Standardization (ISO). DOIs are in wide use mainly to identify academic, professional, and government information, such as journal articles, research reports and data sets *inter allia*. Publisher quality bibliographical attributes can be retrieved from the DOI.

#### Extract

Detect and stage entity, NPL and patent citations in plain text documents.

??? example "In practice"
    Let's consider an excerpt from [US-5914367-A][US-5914367-A]:

    > "Another disadvantage of this process is that such modified enzymes usually show low solubility in organic solvents, thereby limiting the enzyme loading to about 0.02% by weight in the final polymer products. Sea Z. Yang, D. Williams, and A. J. Russell, J. Am. Chem. Soc., 1995, vol. 117, 4843. The solubilized enzyme of this process also shows lower activity (...)"

    The NPL extraction task consists in detecting and staging the following NPL citation:

    > "Z. Yang, D. Williams, and A. J. Russell, J. Am. Chem. Soc., 1995, vol. 117, 4843"

#### Non Patent Literature (NPL)

Any literature which is publicly available and not a patent or a pending/expired publication in a patent office can be an NPL.

#### Parse

Structure a free-form NPL or patent citations into standard bibliographic attributes (e.g. title, authors, journal, etc)


??? example "In practice"

    Let's consider the following free-form [**NPL**](./vocabulary#non-patent-literature-npl) citation:

    > "Z. Yang, D. Williams, and A. J. Russell, J. Am. Chem. Soc., 1995, vol. 117, 4843."

    The parsing task consists in structuring this sequence into the following standardized bibliographical attributes:

    >- `Authors: Z. Yang, D. Williams, A. J. Russell
    >- `Journal`: J. Am. Chem. Soc.
    >- `Date`: 1995
    >- `Volume`: 117
    >- `Page`: 4843

#### Precision

Precision[^prec] attempts to answer the following question: "What proportion of positive identifications was actually correct?". Formerly, precision is defined as:

$$
Precision = \frac{True~Positive}{True~Positive + False~Positive}
$$

#### PubMed

PubMed is a free search engine accessing primarily the MEDLINE database of references and abstracts on life sciences and biomedical topics.
