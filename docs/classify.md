[models/npl_class_training]:https://github.com/cverluise/PatCit/tree/master/models/npl_class_training/
[gh-release]:https://github.com/cverluise/PatCit/releases
[^1]: Include but is not restricted to.


## Classes

We defined 9 research-oriented classes as follows:

|Class |Content[^1]|
|---|---|
|Bibliographical reference|Journal, Book, Technical report, Thesis dissertation|
|Office action|Office action, Response to office action, Notice of allowance, Office communication, Invitation to pay additional fees, Restriction requirements, Invitation to pay additional fees|
|Patent| Patent without any reference to an office action, Patent translation without..., Patent abstract without..., Patent specification without..., Patent chart, Derwent patent abstract, DWPI, WPI|
|Search report|Search report, Written opinion, Report of preliminary patentability, Examiner interview|
|Litigation|Inter-Parte-Review (IPR), Notice of opposition, Patent litigation|
|Database| EMBL, Genebank, Geneseq|
|Product Documentation| Catalogue, Brochure, Product description, Manual/user guide, Commercial doc, Product data sheet|
|Norms and standards|ISO, DIN, 3GPP, IETF, RFC (Request for comments)|
|Webpage| Wikipedia, Articles with web as primary source (except for product documentation)|
|Litigation| IPR, Petition, Invalidity contention|

Approximately 3,000 citations were labelled by hand in one of those exclusive classes thanks to [**Doccano**](awesome#softwares-and-libraries) awesome labeling platform.

!!! warning
    Due to limited ability of the labeling team, non latin-character based citations (Chinese, Japan, etc) were not labelled at all. **Any contribution welcome. **

## Classification model

For the classification model, we rely on [**spaCy's**](./awesome#softwares-and-libraries) textCategorizer.

Specifically, we choose the `ensemble` architecture model. This means that the model is a stacked ensemble of a bag-of-words model and a neural network model. The neural network uses a Convolutional Neural Network (CNN) with mean pooling and attention.

!!! more

    - Training data and model evaluation are available in [`models/npl_class_training`][models/npl_class_training]
    - Models are available in [`v0.2-npl` release][gh-release]
