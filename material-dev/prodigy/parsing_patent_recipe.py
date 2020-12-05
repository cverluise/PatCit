import prodigy
from prodigy.components.loaders import JSONL, JSON
import os


@prodigy.recipe(
    "parsing.check",
    dataset=("The dataset to use", "positional", None, str),
    source=("Path to jsonl", "positional", None, str),
    attr=("Span attribute to be checked", "option", "a", str),
)
def parsing_check(dataset, source, attr):
    """
    The annotator gets a contextualized patent citation displayed
    - the patent citation is highlighted
    - the title (h3 + bold + purple) is the value of the parsed attribute (e.g. orgname)
    - the citation has an href linking to the patent webpage (on google patents), in case further
    inspection is needed. Note, There is no guarantee that the link actually exists.
    The annotator faces a binary choice ACCEPT or REJECT.
    """

    def add_html(stream):
        for task in stream:
            span = task["spans"][0]
            root = "https://patents.google.com/patent/"
            suffix = span["orgname"] + span["original"]

            start, end = (span["start"], span["end"])
            text = task["text"]
            before = text[:start]
            span_ = text[start:end]
            after = text[end:]

            task["html"] = (
                f"<span style='background-color:#775ec2;color:white;font-size:130%;font-weight:bold;'>  "
                f"{str(span.get(attr))}  </span><br> \
                           {before} <span style='background-color: #fae284'><a \
                           href={root + suffix}>{span_}</a></span> \
                           {after}"
            )
            yield task

    fmt = os.path.splitext(source)[-1]
    stream = JSONL(source) if fmt == ".jsonl" else JSON(source)
    stream = add_html(stream)

    # return {"view_id": "classification",
    return {
        "view_id": "blocks",
        "dataset": dataset,
        "stream": stream,
        "config": {"blocks": [{"view_id": "html"}]},  # add the blocks to the config
    }
