# GUIDELINES

## Background

We used grobid to extract in-text patent citations for the corpus of USPTO patents. Each time grobid detects a patent (e.g. "In EP0123456B1 nothing interesting."), it sends back an `xml` object with multiple attributes. These attributes include:

- the `orgName` (e.g. EP),
- the `docNum` (e.g. 0123456)
- the `kindCode` (e.g. B1)
- the `stringRange` (e.g. ('mWYp9Fa',5,9) where 5 is the index of the start of the `docNum` string and 9 is its length)

<details><summary>E.g. Grobid xml object for "In EP0123456B1 nothing interesting."</summary>

```xml
<?xml version="1.0" encoding="UTF-8"?>
<TEI
    xmlns="http://www.tei-c.org/ns/1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink">
    <teiHeader />
    <text>
        <div id="_mWYp9Fa">In EP0123456B1 nothing interesting.</div>
        <div type="references">
            <listBibl>
                <biblStruct type="patent" status="publication">
                    <monogr>
                        <authority>
                            <orgName type="regional">EP</orgName>
                        </authority>
                        <idno type="docNumber" subtype="epodoc">0123456</idno>
                        <idno type="docNumber" subtype="original">0123456</idno>
                        <imprint>
                            <classCode scheme="kindCode">B1</classCode>
                        </imprint>
                        <ptr target="#string-range('mWYp9Fa',5,9)"></ptr>
                    </monogr>
                </biblStruct>
            </listBibl>
        </div>
    </text>
</TEI>

```

</details>

## "Patent detect" validation task


The `docNum` (called `PATENT` for the sake of simplicity) extracted by Grobid have been projected on the text of a random set of 496 full-text US Patents.

<details><summary>Prodigy preview</summary>

![](./prodigy_preview.png)

</details>

The task is to check that Grobid rightly detected the `docNumber`  (e.g. “Pat. No.`6,082,350` PATENT “, “ation No.
`PCT/GB2014/052259 PATENT`”).

## FAQ

**What is a `PATENT`?** The label `PATENT` includes publication, application, provisional and reissued. Actuallly, the data sent by Grobid when it detects a PATENT includes a status attribute which can take application as a value .


**What about `orgName`?** Sometimes (partly due to token alignment), the span under `PATENT` might include the `orgName` (e.g. EP, PCT, etc) and sometimes not. We should not take care about that. What we want to check is that the `docNumber` is in the extracted span.

**What about patent "self-citation" in the header?** Although this kind of citations is not what we are looking for from analytical point of view, still, grobid should not be penalized for detecting a patent citations -> that's what we ask for. The decision to get rid of these citations is part of the cleaning process, ie it comes downstream. In short, we should leave patent self-citations detected in the header.

## In practice

||True|False
---|---|---
|**Positive**|<p><font color="green">"Pat. No.`3,148,291 PATENT` and U.S."</font></p> Action: **None**|<p><font color="red">I was born on `06191991 PATENT` at Les Lilas</font></p> Action: **_Un_label**
|**Negative**|<p><font color="green">If a polymer such as plyurethane</font></p>Action: **None**| <p><font color="red">Application Ser. No. 527,247, filed Nov</font></p> Action: **Label** the missing `docNum` (ie, `527,247 PATENT`)


## Egs (with alignment)

Below is a list of spans which were detected by Grobid as `PATENT` with a bit of context (left and right).

There are 3 columns:

- `prodigy` : this is the span as it will be displayed on the annotation platform
- `orig` : this is the span as it was extracted by grobid
- `aligned` : this is True if the span extracted by grobid had to be modified to be aligned with the tokenizer used by prodigy under the hood. This is relatively rare and is rather technical -> you can forget about it

prodigy|orig|aligned
---|---|---
Pat. No.`3,951,897 PATENT`.|Pat. No.`3,951,897 PATENT`.|False
Ser. No.`09/244,608 PATENT`, filed Fe|Ser. No.`09/244,608 PATENT`, filed Fe|False
Pat. No.`6,082,350 PATENT`.|Pat. No.`6,082,350 PATENT`.|False
Pat. No.`3,148,291 PATENT`, which is|Pat. No.`3,148,291 PATENT`, which is|False
Pat. No.`3,148,291 PATENT`includes|Pat. No.`3,148,291 PATENT`includes|False
Pat. No.`3,148,291 PATENT`and U.S.|Pat. No.`3,148,291 PATENT`and U.S.|False
Pat. No.`3,148,291 PATENT`. However,|Pat. No.`3,148,291 PATENT`. However,|False
Pat. No.`3,148,291 PATENT`or may co|Pat. No.`3,148,291 PATENT`or may co|False
tion Nos.`2002-083102 PATENT`and 2002-|tion Nos.`2002-083102 PATENT`and 2002-1|True
83102 and`2002-190106 PATENT`respectiv|83102 and`2002-190106 PATENT`respectiv|False
pened No.`H05-79,867 PATENT`(Patent L|ened No. H`05-79,867 PATENT`(Patent L|True
pened No.`H06-13,064 PATENT`(Patent L|ened No. H`06-13,064 PATENT`(Patent L|True
pened No.`2001-6,780 PATENT`(Patent L|pened No.`2001-6,780 PATENT`(Patent L|False
pened No.`H05-79,867 PATENT`, disclose|ened No. H`05-79,867 PATENT`, disclose|True
pened No.`H06-13,064 PATENT`, disclose|ened No. H`06-13,064 PATENT`, disclose|True
pened No.`2001-6,780 PATENT`, this inv|pened No.`2001-6,780 PATENT`, this inv|False
EP-`A-2,374,635 PATENT`describes|EP-A-`2,374,635 PATENT`describes|True
US-`A-2012/0225964 PATENT`and DE-A-|US-A-`2012/0225964 PATENT`and DE-A-|True
64 and DE-`A-10 2012 024 494 PATENT`describe|and DE-A-`10 2012 024 494 PATENT`describe|True
Ser. No.`11/638,385 PATENT`, filed De|Ser. No.`11/638,385 PATENT`, filed De|False
Pat. No.`7,920,244 PATENT`now allow|Pat. No.`7,920,244 PATENT`now allow|False
ation No.`2006-0041835 PATENT`, filed on|ation No.`2006-0041835 PATENT`, filed on|False
ation No.`PCT/GB2014/052259 PATENT`, filed Ju|ation No.`PCT/GB2014/052259 PATENT`, filed Ju|False
[4 1 May`30, 1972 541 PATENT`TACKY MAT|[4 1 May`30, 1972 541 PATENT`TACKY MAT|False
Pat. No.`3,083,393 PATENT`. Broadly,|Pat. No.`3,083,393 PATENT`. Broadly,|False
Pat. No.`3,501,797 PATENT`there is|Pat. No.`3,501,797 PATENT`there is|False
Pat. No.`3,083,393 PATENT`, the illu|Pat. No.`3,083,393 PATENT`, the illu|False
Pat. No.`3,083,393 PATENT`. An a|Pat. No.`3,083,393 PATENT`.    An a|False
es Patent`3,197,827 PATENT`END CURE|es Patent`3,197,827 PATENT`END CURE|False
plication`14190599.2 PATENT`, which wa|plication`14190599.2 PATENT`, which wa|False
on no. EP-`A-1,420,298 PATENT`) or a liq|no. EP-A-`1,420,298 PATENT`) or a liq|True
on no. US`2004-0207824 PATENT`. Other li|on no. US`2004-0207824 PATENT`. Other li|False
Pat. No.`5,578,083 PATENT`, the disc|Pat. No.`5,578,083 PATENT`, the disc|False
ation No.`2016-230950 PATENT`, filed on|ation No.`2016-230950 PATENT`, filed on|False
Pat. No.`2,810,688 PATENT`, on the o|Pat. No.`2,810,688 PATENT`, on the o|False
Ser. No.`504,989 PATENT`. This met|Ser. No.`504,989 PATENT`. This met|False
Ser. No.`504,989 PATENT`, and the|Ser. No.`504,989 PATENT`, and the|False
Ser. No.`504,989 PATENT`, the reac|Ser. No.`504,989 PATENT`, the reac|False
Ser. No.`10/114,800 PATENT`, entitled|Ser. No.`10/114,800 PATENT`, entitled|False
Pat. No.`5,246,062 PATENT`. In the k|Pat. No.`5,246,062 PATENT`. In the k|False
Patent DE`29 07 770 C2 PATENT`, a heat e|Patent DE`29 07 770 C2 PATENT`, a heat e|False
Ser. No.`10/955,133 PATENT`, filed on|Ser. No.`10/955,133 PATENT`, filed on|False
Ser. No.`10/955,795 PATENT`, filed Se|Ser. No.`10/955,795 PATENT`, filed Se|False
Pat. No.`6,561,495 PATENT`or U.S. P|Pat. No.`6,561,495 PATENT`or U.S. P|False
Pat. No.`6,640,770 PATENT`, both of|Pat. No.`6,640,770 PATENT`, both of|False
Ser. No.`10/955,781 PATENT`, filed Se|Ser. No.`10/955,781 PATENT`, filed Se|False
Ser. No.`10/955,795 PATENT`, filed on|Ser. No.`10/955,795 PATENT`, filed on|False
Ser. No.`10/955,133 PATENT`, filed on|Ser. No.`10/955,133 PATENT`, filed on|False
Pat. No.`4,412,287 PATENT`, Automate|Pat. No.`4,412,287 PATENT`, Automate|False
Pat. No.`4,674,044 PATENT`, Automate|Pat. No.`4,674,044 PATENT`, Automate|False
Pat. No.`6,195,647 PATENT`, On-line|Pat. No.`6,195,647 PATENT`, On-line|False
Pat. No.`4,412,287 PATENT`, Automate|Pat. No.`4,412,287 PATENT`, Automate|False
Pat. No.`4,674,044 PATENT`, Automate|Pat. No.`4,674,044 PATENT`, Automate|False
Pat. No.`6,195,647 PATENT`, On-line|Pat. No.`6,195,647 PATENT`, On-line|False
Ser. No.`13/015,134 PATENT`, filed Ja|Ser. No.`13/015,134 PATENT`, filed Ja|False
Ser. No.`12/055,726 PATENT`, filed Ma|Ser. No.`12/055,726 PATENT`, filed Ma|False
Pat. No.`8,216,560 PATENT`, issued o|Pat. No.`8,216,560 PATENT`, issued o|False
Ser. No.`11/096,209 PATENT`, filed Ma|Ser. No.`11/096,209 PATENT`, filed Ma|False
Pat. No.`7,556,799 PATENT`, issued o|Pat. No.`7,556,799 PATENT`, issued o|False
Ser. No.`10/965,274 PATENT`, filed Oc|Ser. No.`10/965,274 PATENT`, filed Oc|False
Pat. No.`7,488,495 PATENT`, issued o|Pat. No.`7,488,495 PATENT`, issued o|False
Ser. No.`10/814,527 PATENT`, filed Ma|Ser. No.`10/814,527 PATENT`, filed Ma|False
Pat. No.`7,854,924 PATENT`, issued o|Pat. No.`7,854,924 PATENT`, issued o|False
Ser. No.`10/814,749 PATENT`, filed Ma|Ser. No.`10/814,749 PATENT`, filed Ma|False
Pat. No.`8,192,758 PATENT`, issued o|Pat. No.`8,192,758 PATENT`, issued o|False
Ser. No.`10/813,872 PATENT`, filed Ma|Ser. No.`10/813,872 PATENT`, filed Ma|False
Pat. No.`5,112,993 PATENT`). A prefe|Pat. No.`5,112,993 PATENT`). A prefe|False
Pat. No.`4,427,794 PATENT`), whereby|Pat. No.`4,427,794 PATENT`), whereby|False
Pat. Nos.`5,607,669 PATENT`; 6,294,16|Pat. Nos.`5,607,669 PATENT`; 6,294,16|False
,607,669;`6,294,163 PATENT`; and 5,37|,607,669;`6,294,163 PATENT`; and 5,37|False
,163; and`5,374,422 PATENT`; Figuly e|,163; and`5,374,422 PATENT`; Figuly e|False
ation No.`EP373852A2 PATENT`and U.S.|ion No. EP`373852A2 PATENT`and U.S.|True
Pat. No.`6,475,510 PATENT`, and Remi|Pat. No.`6,475,510 PATENT`, and Remi|False
on Number`PCT/JP2015/000015 PATENT`filed on|on Number`PCT/JP2015/000015 PATENT`filed on|False
on Number`2014-004479 PATENT`filed on|on Number`2014-004479 PATENT`filed on|False
ation No.`2012-225807 PATENT`, when a h|ation No.`2012-225807 PATENT`, when a h|False
ation No.`2011-179997 PATENT`, the ligh|ation No.`2011-179997 PATENT`, the ligh|False
Pat. No.`5,602,575 PATENT`, which co|Pat. No.`5,602,575 PATENT`, which co|False
Ser. No.`14/016,544 PATENT`, filed on|Ser. No.`14/016,544 PATENT`, filed on|False
Ser. No.`61/697,580 PATENT`, filed on|Ser. No.`61/697,580 PATENT`, filed on|False
Ser. No.`13/547,251 PATENT`, filed Ju|Ser. No.`13/547,251 PATENT`, filed Ju|False
ation No.`61/168,853 PATENT`, entitled|ation No.`61/168,853 PATENT`, entitled|False
Pat. No.`4,678,108 PATENT`, there is|Pat. No.`4,678,108 PATENT`, there is|False
Pat. No.`2,558,382 PATENT`. In this|Pat. No.`2,558,382 PATENT`. In this|False
ation No.`2012-506006 PATENT`, for exam|ation No.`2012-506006 PATENT`, for exam|False
ation No.`2012-506006 PATENT`mentioned|ation No.`2012-506006 PATENT`mentioned|False
ation No.`2012-506006 PATENT`depending|ation No.`2012-506006 PATENT`depending|False
ation No.`2012-506006 PATENT`; hereinaf|ation No.`2012-506006 PATENT`; hereinaf|False
ation No.`20 2010 015 899.0 PATENT`filed Nov|ation No.`20 2010 015 899.0 PATENT`filed Nov|False
ation No.`62/280,984 PATENT`, filed Ja|ation No.`62/280,984 PATENT`, filed Ja|False
ation No.`61/681,032 PATENT`entitled|ation No.`61/681,032 PATENT`entitled|False
Ser. No.`10/297,978 PATENT`, filed Ju|Ser. No.`10/297,978 PATENT`, filed Ju|False
ation No.`PCT/US01/19089 PATENT`filed Jun|ation No.`PCT/US01/19089 PATENT`filed Jun|False
ation No.`60/223,734 PATENT`filed Aug|ation No.`60/223,734 PATENT`filed Aug|False
ation No.`60/211,375 PATENT`filed Jun|ation No.`60/211,375 PATENT`filed Jun|False
Pat. No.`5,994,409 PATENT`) are high|Pat. No.`5,994,409 PATENT`) are high|False
Pat. No.`6,071,956 PATENT`, discusse|Pat. No.`6,071,956 PATENT`, discusse|False
Pat. Nos.`4,561,726 PATENT`; 4,589,99|Pat. Nos.`4,561,726 PATENT`; 4,589,99|False
,561,726;`4,589,996 PATENT`; 4,592,85|,561,726;`4,589,996 PATENT`; 4,592,85|False
,589,996;`4,592,858 PATENT`; 4,596,66|,589,996;`4,592,858 PATENT`; 4,596,66|False
,592,858;`4,596,667 PATENT`; 4,613,20|,592,858;`4,596,667 PATENT`; 4,613,20|False
,596,667;`4,613,209 PATENT`; 4,614,60|,596,667;`4,613,209 PATENT`; 4,614,60|False
,613,209;`4,614,609, PATENT`and 4,622|,613,209;`4,614,609, PATENT`and 4,622,|True
,609, and`4,622,165 PATENT`. Ferroele|,609, and`4,622,165 PATENT`. Ferroele|False
Pat. No.`4,932,758 PATENT`(to Hanyu|Pat. No.`4,932,758 PATENT`(to Hanyu|False
`12, 1941. ALKAN&#39 PATENT`; emoumnmr|`12, 1941. A PATENT`LKAN&#39;|True
Ser. No.`62/349,534 PATENT`, filed Ju|Ser. No.`62/349,534 PATENT`, filed Ju|False
Ser. No.`12/172,681 PATENT`, filed on|Ser. No.`12/172,681 PATENT`, filed on|False
Ser. No.`10/143,833 PATENT`, filed on|Ser. No.`10/143,833 PATENT`, filed on|False
ation No.`60/290,352 PATENT`, filed Ma|ation No.`60/290,352 PATENT`, filed Ma|False
ation No.`62/469,356 PATENT`titled DI|ation No.`62/469,356 PATENT`titled DI|False
on Number`2012-011804 PATENT`, filed Ja|on Number`2012-011804 PATENT`, filed Ja|False
on Number`2012-130075 PATENT`, filed Ju|on Number`2012-130075 PATENT`, filed Ju|False
ation No.`4-223697 PATENT`has been|ation No.`4-223697 PATENT`has been|False
Ser. No.`13/543,779 PATENT`filed Jul|Ser. No.`13/543,779 PATENT`filed Jul|False
Ser. No.`12/111,816 PATENT`filed Apr|Ser. No.`12/111,816 PATENT`filed Apr|False
Ser. No.`11/280,560 PATENT`filed Nov|Ser. No.`11/280,560 PATENT`filed Nov|False
Pat. No.`8,391,039 PATENT`), which i|Pat. No.`8,391,039 PATENT`), which i|False
Ser. No.`11/094,137 PATENT`filed Mar|Ser. No.`11/094,137 PATENT`filed Mar|False
Pat. No.`7,209,397 PATENT`), which i|Pat. No.`7,209,397 PATENT`), which i|False
Ser. No.`10/732,533 PATENT`filed Dec|Ser. No.`10/732,533 PATENT`filed Dec|False
Pat. No.`7,225,311 PATENT`), which i|Pat. No.`7,225,311 PATENT`), which i|False
Ser. No.`09/841,911 PATENT`filed Apr|Ser. No.`09/841,911 PATENT`filed Apr|False
Pat. No.`6,675,272 PATENT`), all of|Pat. No.`6,675,272 PATENT`), all of|False
Ser. No.`12/132,559 PATENT`, filed Ju|Ser. No.`12/132,559 PATENT`, filed Ju|False
Pat. No.`8,398,816 PATENT`on Mar. 1|Pat. No.`8,398,816 PATENT`on Mar. 1|False
Ser. No.`11/391,134 PATENT`(now aban|Ser. No.`11/391,134 PATENT`(now aban|False
Ser. No.`13/562,421 PATENT`, filed Ju|Ser. No.`13/562,421 PATENT`, filed Ju|False
Pat. No.`8,518,210 PATENT`on Aug. 2|Pat. No.`8,518,210 PATENT`on Aug. 2|False
Ser. No.`12/586,175 PATENT`, filed Se|Ser. No.`12/586,175 PATENT`, filed Se|False
Pat. No.`8,282,768 PATENT`on Oct. 9|Pat. No.`8,282,768 PATENT`on Oct. 9|False
Ser. No.`11/391,134 PATENT`(now aban|Ser. No.`11/391,134 PATENT`(now aban|False
atent No.`60/742,844 PATENT`, filed De|atent No.`60/742,844 PATENT`, filed De|False
Ser. No.`11/115,576 PATENT`filed Apr|Ser. No.`11/115,576 PATENT`filed Apr|False
Pat. No.`8,137,465 PATENT`on Mar. 2|Pat. No.`8,137,465 PATENT`on Mar. 2|False
Ser. No.`10/672,311 PATENT`, filed Se|Ser. No.`10/672,311 PATENT`, filed Se|False
Pat. No.`7,208,389 PATENT`on Apr. 2|Pat. No.`7,208,389 PATENT`on Apr. 2|False
Ser. No.`11/115,576 PATENT`filed Apr|Ser. No.`11/115,576 PATENT`filed Apr|False
Pat. No.`8,137,465 PATENT`on Mar. 2|Pat. No.`8,137,465 PATENT`on Mar. 2|False
. Patents`2,067,580, PATENT`2,091,615|. Patents`2,067,580, PATENT`2,091,615|False
,067,580,`2,091,615, PATENT`and 2,154|,067,580,`2,091,615, PATENT`and 2,154|False
,615, and`2,154,639 PATENT`. The comp|,615, and`2,154,639 PATENT`. The comp|False
Pat. Nos.`2,865,719 PATENT`; 2,867,50|Pat. Nos.`2,865,719 PATENT`; 2,867,50|False
,865,719;`2,867,509 PATENT`; 2,926,07|,865,719;`2,867,509 PATENT`; 2,926,07|False
,867,509;`2,926,072 PATENT`; and 2,92|,867,509;`2,926,072 PATENT`; and 2,92|False
Pat. No.`3,014,943 PATENT`and Briti|Pat. No.`3,014,943 PATENT`and Briti|False
tion) No.`2010-502977 PATENT`(correspo|tion) No.`2010-502977 PATENT`(correspo|False
onding to`US2010/0054415 PATENT`). In this|ding to US`2010/0054415 PATENT`). In this|True
-open No.`2011-200532 PATENT`discloses|-open No.`2011-200532 PATENT`discloses|False
-open No.`2011-200532 PATENT`discloses|-open No.`2011-200532 PATENT`discloses|False
-open No.`2011-200532 PATENT`solve the|-open No.`2011-200532 PATENT`solve the|False
-open No.`2011-200532 PATENT`, but also|-open No.`2011-200532 PATENT`, but also|False
ation No.`2012-172012 PATENT`, filed Au|ation No.`2012-172012 PATENT`, filed Au|False
G DEVICE.`No.1412,804 PATENT`. Patented|EVICE. No.`1412,804 PATENT`. Patented|True
Pat. Nos.`4,723,779 PATENT`; 4,979,74|Pat. Nos.`4,723,779 PATENT`; 4,979,74|False
,723,779;`4,979,740 PATENT`; 4,817,94|,723,779;`4,979,740 PATENT`; 4,817,94|False
,979,740;`4,817,946 PATENT`; 3,971,55|,979,740;`4,817,946 PATENT`; 3,971,55|False
,817,946;`3,971,558 PATENT`; 5,203,55|,817,946;`3,971,558 PATENT`; 5,203,55|False
,971,558;`5,203,557 PATENT`; and U.S.|,971,558;`5,203,557 PATENT`; and U.S.|False
Pat. Nos.`5,113,981 PATENT`; 6,085,80|Pat. Nos.`5,113,981 PATENT`; 6,085,80|False
,113,981;`6,085,802 PATENT`; 6,390,23|,113,981;`6,085,802 PATENT`; 6,390,23|False
,085,802;`6,390,234 PATENT`; and 6,53|,085,802;`6,390,234 PATENT`; and 6,53|False
,234; and`6,533,066 PATENT`and WIPO|,234; and`6,533,066 PATENT`and WIPO|False
Ser. No.`60/470,172 PATENT`, filed Ma|Ser. No.`60/470,172 PATENT`, filed Ma|False
Ser. No.`60/514,634 PATENT`, filed Oc|Ser. No.`60/514,634 PATENT`, filed Oc|False
Pat. No.`5,690,312 PATENT`to Yang d|Pat. No.`5,690,312 PATENT`to Yang d|False
es Patent`3,377,331 PATENT`PRODUCTIO|es Patent`3,377,331 PATENT`PRODUCTIO|False
atent No.`533,362 PATENT`, issued M|atent No.`533,362 PATENT`, issued M|False
Ser. No.`532,365 PATENT`, filed Se|Ser. No.`532,365 PATENT`, filed Se|False
an Patent`533,362 PATENT`, namely c|an Patent`533,362 PATENT`, namely c|False
an Patent`533,362 PATENT`, in vario|an Patent`533,362 PATENT`, in vario|False
atent No.`2,699,457 PATENT`. Attentio|atent No.`2,699,457 PATENT`. Attentio|False
n Patents`534,792 PATENT`and 534,8|n Patents`534,792 PATENT`and 534,88|True
4,792 and`534,888 PATENT`, the disc|4,792 and`534,888 PATENT`, the disc|False
atent No.`4682750 PATENT`|atent No.`4682750 PATENT`|False
Pat. No.`5,851,387 PATENT`, which is|Pat. No.`5,851,387 PATENT`, which is|False
-Open No.`2011-207235 PATENT`has discl|-Open No.`2011-207235 PATENT`has discl|False
-Open No.`2011-207235 PATENT`enable a|-Open No.`2011-207235 PATENT`enable a|False
ation No.`2007-518587 PATENT`, such as|ation No.`2007-518587 PATENT`, such as|False
ation No.`2016-189754 PATENT`filed Sep|ation No.`2016-189754 PATENT`filed Sep.|True
iled Sep.`28, 2016, PATENT`and No. 2|iled Sep.`28, 2016, PATENT`and No. 20|True
, and No.`2016-189755 PATENT`filed Sep|, and No.`2016-189755 PATENT`filed Sep|False
G. CLARK`3,051,848 PATENT`SHIFT REG|G. CLARK`3,051,848 PATENT`SHIFT REG|False
ded by US-`A-2004/0044542 PATENT`, which de|d by US-A-`2004/0044542 PATENT`, which de|True
iques, US-`A-2004/0254768 PATENT`describes|ues, US-A-`2004/0254768 PATENT`describes|True
ations WO-`A-2005/18249 PATENT`and PCT/E|ions WO-A-`2005/18249 PATENT`and PCT/E|True
WO-`A-2005/18249 PATENT`discloses|WO-A-`2005/18249 PATENT`discloses|True
rs.`PCT/EP2005/008238 PATENT`discloses|rs.`PCT/EP2005/008238 PATENT`discloses|False
ure of WO-`A-2005/18249 PATENT`wherein i|e of WO-A-`2005/18249 PATENT`wherein i|True
method of`PCT/EP2005/008238 PATENT`includes|method of`PCT/EP2005/008238 PATENT`includes|False
003 or US-`A-2004/0254768 PATENT`(both alr|3 or US-A-`2004/0254768 PATENT`(both alr|True
ure 1: WO`2014/156388 PATENT`DIS|ure 1: WO`2014/156388 PATENT`DIS|False
ent 1] JP-`A-11-335613 PATENT`|t 1] JP-A-`11-335613 PATENT`|True
bed in JP-`B-51-44706 PATENT`, JP-B-51-|d in JP-B-`51-44706 PATENT`, JP-B-51-|True
44706, JP-`B-51-44707 PATENT`, JP-B-1-2|706, JP-B-`51-44707 PATENT`, JP-B-1-2|True
44707, JP-`B-1-29398 PATENT`, and the|707, JP-B-`1-29398 PATENT`, and the|True
bed in JP-`B-4-17154 PATENT`, JP-A-7-1|d in JP-B-`4-17154 PATENT`, JP-A-7-1|True
17154, JP-`A-7-179777 PATENT`, JP-A-7-3|154, JP-A-`7-179777 PATENT`, JP-A-7-3|True
79777, JP-`A-7-33997 PATENT`, JP-A-8-3|777, JP-A-`7-33997 PATENT`, JP-A-8-3|True
33997, JP-`A-8-39936 PATENT`and the l|997, JP-A-`8-39936 PATENT`and the l|True
bed in JP-`A-2006-137886 PATENT`is suitab|d in JP-A-`2006-137886 PATENT`is suitab|True
bed in JP-`A-2006-188660 PATENT`can be al|d in JP-A-`2006-188660 PATENT`can be al|True
atoms (JP-`A-11-129623 PATENT`), a speci|oms (JP-A-`11-129623 PATENT`), a speci|True
ester (JP-`A-2001-105732 PATENT`), a galli|ter (JP-A-`2001-105732 PATENT`), a galli|True
ester (JP-`A-2003-253149 PATENT`), or the|ter (JP-A-`2003-253149 PATENT`), or the|True
ation No.`2008-049303 PATENT`filed on|ation No.`2008-049303 PATENT`filed on|False
ation No.`2008-190422 PATENT`filed on|ation No.`2008-190422 PATENT`filed on|False
ation No.`2006-313792 PATENT`, a manufa|ation No.`2006-313792 PATENT`, a manufa|False
Pat. No.`6,797,421 PATENT`, the fuel|Pat. No.`6,797,421 PATENT`, the fuel|False
In U.S.`2002/0068202 PATENT`, it is su|In U.S.`2002/0068202 PATENT`, it is su|False
ation No.`PCT/JP2007/000656 PATENT`, filed Ju|ation No.`PCT/JP2007/000656 PATENT`, filed Ju|False
ation No.`2006-195241 PATENT`, the enti|ation No.`2006-195241 PATENT`, the enti|False
cation CN`201520060877.X PATENT`filed Jan|cation CN`201520060877 PATENT`.X filed J|True
ation No.`PCT/EP2011/073681 PATENT`, filed De|ation No.`PCT/EP2011/073681 PATENT`, filed De|False
EP-`A-0902082 PATENT`discloses|EP-A-`0902082 PATENT`discloses|True
EP-`A-1493801 PATENT`discloses|EP-A-`1493801 PATENT`discloses|True
ations CN`200910249088.X PATENT`and EP102|ations CN`200910249088 PATENT`.X and EP1|True
bed in EP-`A-1493801 PATENT`, CN 20091|d in EP-A-`1493801 PATENT`, CN 20091|True
93801, CN`200910249088.X PATENT`and EP102|93801, CN`200910249088 PATENT`.X and EP1|True
088.X and`EP10250232.5 PATENT`do allow|8.X and EP`10250232 PATENT`.5 do allo|True
WO`2007/118614 PATENT`describes|WO`2007/118614 PATENT`describes|False
bed in WO`97/18320 PATENT`, the cont|bed in WO`97/18320 PATENT`, the cont|False
ation No.`PCT/JP2008/002547 PATENT`, filed Se|ation No.`PCT/JP2008/002547 PATENT`, filed Se|False
ation No.`2007-238140 PATENT`, Sep. 13,|ation No.`2007-238140 PATENT`, Sep. 13,|False
cument 1]`WO99/38822 PATENT`[Nonpat|ment 1] WO`99/38822 PATENT`[Nonpat|True
ation No.`5-305238 PATENT`can be ex|ation No.`5-305238 PATENT`can be ex|False
ation No.`PCT/JP2003/009664 PATENT`filed Jul|ation No.`PCT/JP2003/009664 PATENT`filed Jul|False
ation No.`2002-055781 PATENT`J|ation No.`2002-055781 PATENT`J|False
ation No.`10-269021 PATENT`J|ation No.`10-269021 PATENT`J|False
ation No.`5-250094 PATENT`SU|ation No.`5-250094 PATENT`SU|False
Pat. No.`4,108,150 PATENT`issued on|Pat. No.`4,108,150 PATENT`issued on|False
Ser. No.`09/331,807 PATENT`, filed Au|Ser. No.`09/331,807 PATENT`, filed Au|False
Pat. No.`6,047,624 PATENT`.|Pat. No.`6,047,624 PATENT`.|False
Ser. No.`08/700,583 PATENT`or assays|Ser. No.`08/700,583 PATENT`or assays|False
Pat. No.`5,137,806 PATENT`(detectio|Pat. No.`5,137,806 PATENT`(detectio|False
Pat. No.`5,348,855 PATENT`(assay fo|Pat. No.`5,348,855 PATENT`(assay fo|False
Pat. No.`5,512,441 PATENT`(detectio|Pat. No.`5,512,441 PATENT`(detectio|False
Pat. No.`5,272,057 PATENT`and U.S.|Pat. No.`5,272,057 PATENT`and U.S.|False
Pat. No.`5,380,645 PATENT`(RFLP ana|Pat. No.`5,380,645 PATENT`(RFLP ana|False
Pat. No.`5,527,676 PATENT`(detectio|Pat. No.`5,527,676 PATENT`(detectio|False
Pat. No.`5,330,892 PATENT`(detectio|Pat. No.`5,330,892 PATENT`(detectio|False
Pat. No.`5,352,775 PATENT`(detectio|Pat. No.`5,352,775 PATENT`(detectio|False
Pat. No.`5,532,108 PATENT`(detectio|Pat. No.`5,532,108 PATENT`(detectio|False
), and in`WO96/08514 PATENT`(monoclon|and in WO`96/08514 PATENT`(monoclon|True
Pat. Nos.`4,333,734 PATENT`and 5,196|Pat. Nos.`4,333,734 PATENT`and 5,196,|True
3,734 and`5,196,167 PATENT`, incorpor|3,734 and`5,196,167 PATENT`, incorpor|False
Pat. No.`5,380,647 PATENT`, incorpor|Pat. No.`5,380,647 PATENT`, incorpor|False
Pat. No.`4,857,300 PATENT`, incorpor|Pat. No.`4,857,300 PATENT`, incorpor|False
Pat. No.`6,516,227 PATENT`(“the &#3|Pat. No.`6,516,227 PATENT`(“the &#3|False
Ser. No.`11/305,898 PATENT`, filed De|Ser. No.`11/305,898 PATENT`, filed De|False
ation No.`PCT/IL2004/000374 PATENT`, filed on|ation No.`PCT/IL2004/000374 PATENT`, filed on|False
plication`60/467,562 PATENT`, filed Ma|plication`60/467,562 PATENT`, filed Ma|False
eference.`PCT/IL2004/000374 PATENT`is also a|eference.`PCT/IL2004/000374 PATENT`is also a|False
Ser. No.`10/398,375 PATENT`, filed on|Ser. No.`10/398,375 PATENT`, filed on|False
hed as US`2004-0075814 PATENT`, which is|hed as US`2004-0075814 PATENT`, which is|False
plication`PCT/IL01/00933 PATENT`, filed on|plication`PCT/IL01/00933 PATENT`, filed on|False
hed as WO`02/28266 PATENT`, which ta|hed as WO`02/28266 PATENT`, which ta|False
Ser. No.`09/781,548 PATENT`, filed on|Ser. No.`09/781,548 PATENT`, filed on|False
Pat. No.`6,656,131 PATENT`. The pres|Pat. No.`6,656,131 PATENT`. The pres|False
Ser. No.`10/368,002 PATENT`, filed on|Ser. No.`10/368,002 PATENT`, filed on|False
hed as US`2003-0223038 A1 PATENT`, which cl|hed as US`2003-0223038 A1 PATENT`, which cl|False
plication`60/357,115 PATENT`, filed on|plication`60/357,115 PATENT`, filed on|False
