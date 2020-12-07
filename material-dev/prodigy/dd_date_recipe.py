import prodigy
from prodigy.components.loaders import Images


OPTIONS = [{"id": 0, "text": "Unknown"}]


@prodigy.recipe("date-dd")
def date_dd(dataset, source):
    """Display 3 blocks: 1. image of the patent, 2. choice block, 3. text block for date. 2 is
    artifical and should be ignored"""

    def get_stream():
        # Load the directory of images and add options to each task
        stream = Images(source)
        for eg in stream:
            eg["options"] = OPTIONS
            yield eg

    return {
        "dataset": dataset,
        "view_id": "blocks",
        "config": {
            "choice_style": "single",
            "blocks": [
                {"view_id": "choice", "text": None},
                {
                    "view_id": "text_input",
                    "field_rows": 1,
                    "field_label": "Publication year (yyyy)",
                },
            ],
        },
        "stream": get_stream(),
    }
