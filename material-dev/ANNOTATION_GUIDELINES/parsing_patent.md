# GUIDELINES

:hugging_face: [@kylehigham](https://github.com/kylehigham) and G. Cristelli

## Background

When GROBID detects a patent citation, it sends back an xml object with the patent attributes *inter allia*. Among these attributes, we specifically look at 2 of them:

- the `orgname`: the name of the office to which the patent relates (ISO-2)
- the `original number`: the doc number as cited in the text (which might differ from the "normalized" number)

## Patent parsing validation task

The parsed attribute is reported above the span of text (the detected patent in context), the patent under review is highlighted in the text itself. The labeller has 3 different available actions:

- `ACCEPT`: if the labeller agrees with the parsed attribute
- `REJECT`: if he disagrees
- `IGNORE`: if he cannot say for some reason

The same labelling recipe is applied to the two attributes.

![](parsing_patent_prodigy_preview.png)


<details><summary>More</summary>

```shell sript
cd validation/intext/patent_parsing
prodigy parsing.check <attr>.parsing.check parsing.check.jsonl --attr <attr> -F parsing_patent_recipe.py
```

</details>
