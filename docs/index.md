[^1]: Patent text contain patent, [**NPL**](./vocabulary#non-patent-literature-npl), software, database, product, etc citations.
[^2]: Bibliographical reference, office action, patent, webpage, norm & standard, product documentation, database and litigation
[^nvy]: <span style="color:red">Not validated yet</span>

# <small>Welcome to</small> PatCit

*Making Patent Citations Uncool Again*

Patents are at the crossroads of many innovation nodes: science, industry, products, competition, etc. Such interactions can be identified through citations *in a broad sense*.

It is now common to use patent-to-patent citations to study some aspects of the innovation system. However, **there is much more buried in the [**Non Patent Literature (NPL)**](./vocabulary#non-patent-literature-npl) citations and in the patent text itself**.[^1]

Good news, Natural Language Processing (NLP) tools now enable social scientists to excavate and structure this long hidden information. **That's the purpose of this project**.

## Achievements

So far, we have:

1. **classified** the 40 million NPL citations reported in the [**DOCDB**](./vocabulary#epo-worldwide-bibliographic-data-docdb) database in 9 distinct research oriented classes[^2] with a 90% accuracy rate.
2. [**parsed**](./vocabulary#parse) and [**consolidated**](./vocabulary#consolidate) the 27 million [**NPL**](./vocabulary#non-patent-literature-npl) citations classified as bibliographical references.

    !!! more
        From the 27 million bibliographical references:

        1. 11 million (40%) were matched with a [**DOI**](./vocabulary#digital-object-identifier-doi) with a 99% [**precision**](./vocabulary#precision) rate
        2. the main bibliographic attributes were parsed with [**accuracy**](./vocabulary#accuracy) rates ranging between 71% and 92% for the remaining 16 million (60%)

3. [**extracted**](./vocabulary#extract), [**parsed**](./vocabulary#parse) and [**consolidated**](./vocabulary#consolidate) in-text bibliographical references and patent citations from the body of all time USPTO patents.[^nvy]

    !!! more
        From the 16 million USPTO patents, we have:

        1. [**extracted**](./vocabulary#extract) and [**parsed**](./vocabulary#parse) 70 million in-text bibliographical references and 80 million patent citations[^nvy].
        2. found a [**DOI**](./vocabulary#digital-object-identifier-doi) for 13+ million in-text bibliographical references (18%)[^nvy].


## Features

#### Open

- The code is licensed under MIT-2 and the dataset is licensed under CC4. Two highly permissive licenses.
- The project is thought to be *dynamically improved by and for the community*. Anyone should feel free to open discussions, raise issues, request features and contribute to the project.

#### Comprehensive

- We address *worldwide patents*, as long as the data is available.
- We address *all classes of citations*[^2], not only bibliographical references.
- We address front-page and in-text citations.

#### Highest standards

- We use and implement state-of-the art machine learning solutions.
- We take great care to implement only the most efficient solutions. We believe that computational resources should be used sparsely, for both environmental sustainability and long term financial sustainability of the project.
