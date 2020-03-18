[presentation]:https://github.com/cverluise/PatCit/blob/master/dissemination/IIPP-CEMI_03032020.pdf
[release]: https://github.com/cverluise/PatCit/releases
[npl_class_training]:https://github.com/cverluise/PatCit/tree/master/models/npl_class_training
[validation]:https://github.com/cverluise/PatCit/tree/master/validation

!!! done

    A detailed presentation of the current state of the project is available in our [March 2020 presentation][presentation].


## Front-page [Non Patent Literature (NPL)](./vocabulary#non-patent-literature-npl) citations ![](https://img.shields.io/badge/-npl-lightgrey)

* [x] Structure the [**NPL**](./vocabulary#non-patent-literature-npl) citations into research oriented classes -  `v0.2-npl` and above

    ??? more
        - 9 exclusive classes: bibliographical reference, office action, patent, webpage, norm & standard, product documentation, database and litigation
        - Classification model available for download in [`v0.2-npl` release][release]
        - Classification model details (labeling guidelines, performance, etc) available in [models/npl_class_training][npl_class_training]

        **Research direction**: Improve classifier


* [x] [**Parse**](./vocabulary#parse) and [**consolidate**](./vocabulary#consolidate) [**NPL**](./vocabulary#non-patent-literature-npl) citations based on their categories - `beta-npl` and above

    ??? more
        - Supports bibliographical references only (60% of all [**NPL**](./vocabulary#non-patent-literature-npl) citations)
        - Validation details available in [validation/][validation]

        **Research direction**: Extend parsing models to other classes of [**NPL**](./vocabulary#non-patent-literature-npl)

## In-text citations ![](https://img.shields.io/badge/-in--text-lightgrey)

* [x] [**Extract**](./vocabulary#extract), [**parse**](./vocabulary#parse) and [**consolidate**](./vocabulary#consolidate) *in-text* patent and NPL citations - `beta-intext*` and above

    ??? more
        **Research direction**: Validate results and improve model

* [ ] [**Extract**](./vocabulary#extract) and [**consolidate**](./vocabulary#consolidate) *in-text* entities of interest (software, database, product, chemicals, etc) - unsupported yet
