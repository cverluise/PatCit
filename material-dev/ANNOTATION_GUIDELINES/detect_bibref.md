# GUIDELINES

:hugging_face: [@lucas-violon](https://github.com/lucas-violon)

## Background


Since the work from **Galibert et al. (2010)**, research started to use machine learning technics to extract bibliographical references in natural language from patent corpus. Those citations, often refered to as in-text Non-Patent Litterature (NPL), could more accurately translate knowledge and innovation flows than front-page patent references subject to legal obligations ("duty of disclosure", see **Bryan et al. (2019)**). Thus, this project aims to set a comprehensive dataset of NPL in-text citations in order to better monitor innovation dynamics across countries, industries and time.

Here, we use Grobid to extract in-text non-patent citations from the corpus of USPTO patents. Each time Grobid detects a bibliographical reference (aka `BIBREF`) (e.g. " For more details, see "Baileys Industrial Oil and Fat Products", Wiley - Interscience Publishers (2005)" ), it sends back an `xml` object with multiple bibliographical attributes.


## "BIBREF detect" validation task

The span of the Grobid extracted citations (called `BIBREF` for the sake of simplicity) have been projected on the text of a random set of 496 full-text US Patents.

The task is to check that Grobid rightly detected the `BIBREF` span (e.g. " see `"Baileys Industrial Oil and Fat Products", Wiley - Interscience Publishers (2005) BIBREF`). If not, the labeler corrects Grobid predictions.

**Prodigy preview**

![Alt ProdigPreview](detect_bibref_prodigy_preview.jpg)


## Q&A

#### What is a `BIBREF`?

A `BIBREF`is any non-patent bibliographical reference that is made in the patent text body. It includes references to:

- books
- scientific articles
- technical reports
- engineering notices (such as IETF requests for comments)
- other white papers with a disclosure intent

#### What about the following "limit cases"?

* `BIBREF` excludes:

	* Global models, standards and paradigmas (such as in "uses the World Geodetic System 1984 model (WGS-84)").
	* References to suppliers of a specific piece sometimes mentionned in a patent.
	* Web references such as Wiki articles.

>All of the above might be the objects of future isolated analysis from PatCit project.

*  `BIBREF` includes:

	* Short quotes such as "A.L. Genovese et al (1998))".

## In Practice

|               | True            | False             |
|:------------- |:----------------| :-----------------|
| **Positive**  | see `"Baileys...Products", Wiley - Int Pub (2005) BIBREF` for more | `The table includes 2500 BIBREF` data   |
| **Negative**  | The table includes 2500 data |  see "Baileys...Products", Wiley - Int Pub (2005) for more |



### Grobid errors typology

#### False Positives from 203 annotated patents


|  Type | Count | Example(s) |
|:------------- |:----------------| :-----------------|
| *Capital letters and Numbers in graph descriptions* | ≈ 135 |  `An X-axis frame roller 1124 is attached via a shaft 1126 to the X-axis frame 1128 and tracks along the upper edge of a roller track 1130 affixed to the inside edge of an upper mainframe horizontal member 1132” BIBREF` or `Both lines 1040 and 1050 clearly exhibit switching intervals 1060 and 1070 that correspond to maneuvers 240 and 250 BIBREF`|
| *Patent or patent authors* | ≈ 40 |  "in patent application Ser. No. 442802 filed Feb 18 1974 in the name of `R.J. Rosa, G. R. Enos and S. W.Petty **BIBREF**`" or `Patented July 31, 1956 2?757?351 CoAxrAL BUTT CONTACT CONNECTOR Curt W. Klostermann, Chicago, III., assignor to Amercian Phenolic Corporation, Chicago, III., a corporation of Illinois Application February 4, 1953, Serial No? 335,135 BIBREF`    |
|*Material suppliers* | ≈ 15 |  “Mentions may also be made to the aerogels sold by the company Cabot under the references `Aerogel TLD 201, Aerogel OLG 201, Aerogel TLD 203, Envoa Aerogel 1100 and Enova Aerogel MT 1200 BIBREF`.”|
|**Total**  								| **≈ 190**


#### True Positives from 200 annotated patents

Grobid detected **about 290 `BIBREF`** within the first 200 documents from the patent set. Here are a few examples:

* `A.F. Genovese: “The Interacting Multiple Model Algorithm for accurate State Estimation of Maneuvering Targets”, APL Technical Digest 22 (4) 614-623 (2001) BIBREF`
* `G.A. Watson et al. : “benchmark Problem with a multisensor framework for Radar Resource Allocation …” NSWCDD TR 99-32 BIBREF`
* `IETF RFC « Routing metrics used for Path Calculation », by Vasseur et al. (March 2012) BIBREF`
* `Rasquin et al. BIBREF`

## References

Related Litterature:

* Galibert, Rosset, Tannier & Grandry, *`Hybrid Citation Extraction from Patents`*, 2010
* Tkaczyk, Collins, Sheridan & Beel, *`Machine Learning vs. Rules and Out-of-the-Box vs. Retrained`*, 2018
* Marx & Fuegi, *`Reliance on Science in Patenting`*, February 2019
* Bryan, Ozcat & Sampat, *`In-Text Patent Citations: A User’s Guide`*, March 2019


Software:

* `Prodigy`, https://prodi.gy, @2017 Copyright
