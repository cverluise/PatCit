# Annotation Guidelines: `DATABASE`

The majority of documents in this section belong to biological polymer sequences. These documents are most often identified by the accession number (see definition below). Note that accession numbers are defined at the sequence level. It can refer to mutiple documents (biblref, patents, etc). This document is sometimes explicitly mentioned.

Sample record of the NCBI database [U49845](https://www.ncbi.nlm.nih.gov/Sitemap/samplerecord.html).

## `NAME`

*Database name*: This is the name of the cited database/ the database from which the document cited is issued.

E.g.:

- GENBANK
- EMBL
- NCBI

_Annotation choices_


1. Annotate without the "database" word which does not provide any additional information here
2. Do not annotate database retrieved from. E.g "DATABASE `EMBL DNAME` \[online\] (...), retrieved EBI accession no. EMBL : CF66..." EBI is not annotated
3. Do not annotate when the database is part of the accession number. E.g. "UNIPROT : B5YAF8"


## `ACC_NUM`

*Accession number*: This is the unique identifier given to a biological polymer sequence (DNA, protein) when it is submitted to a sequence database. This might be the key for consolidation.

> Note: strictly speaking, the acccession number is sometimes the version number.

E.g.:

- Y78511
- 1976-519336
- AB333793
- AK001872.1 (AN:AK001872, Version:1)

## `DATE`

*Accession year*: This is the year at which the document cited was accessed (i.e. integrated to the database).

E.g.

- 2006
- 2006-10-20
- 20 oct 2006

_Annotation choices_

1. Do not annotate retrieval date. E.g. "retrieved on Mar. 21, 2006"


## `BIB_REF`

*Bibliographical reference*: It can refer to mutiple documents (biblref, patents, etc). This document is sometimes explicitly mentioned.

E.g. Prescott, J.S. et al. 'Human androgen regulated homeobox protein (NKX3.1) mRNA, complete cds' (Dec. 1996)
