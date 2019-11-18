import json
import lzma
from glob import glob
from pprint import pprint

import click
import smart_open
from tqdm import tqdm


@click.command()
@click.option("--path", help="Path. Wilcard '*' enabled")
@click.option("--tar", default=False, help="True for .xz files")
@click.option(
    "--flavor",
    default="sm",
    help="Examples reported if <flavor> is lg. Default " "<falvor> is sm.",
)
@click.option(
    "--limit", default=None, type=int, help="Break after <limit> iterations"
)
def main(path, tar, flavor, limit):
    assert flavor in ["sm", "lg"]
    key_val = {}
    i = 0
    for file in tqdm(glob(path)):
        if tar:
            _open = lzma.open
        else:
            _open = smart_open.open
        with _open(file) as f:
            for l in tqdm(f):
                i += 1
                for k, v in json.loads(l).items():
                    if k in key_val.keys():
                        if flavor == "lg":
                            key_val.update(
                                {
                                    k: (
                                        key_val[k][0] + 1,
                                        key_val[k][1],
                                        key_val[k][2],
                                    )
                                }
                            )
                        else:
                            key_val.update(
                                {k: (key_val[k][0] + 1, key_val[k][1])}
                            )
                    else:
                        if flavor == "lg":
                            key_val.update({k: (1, type(v), v)})
                        else:
                            key_val.update({k: (1, type(v))})
                if limit:
                    if i > limit:
                        break

    pprint(key_val)


if __name__ == "__main__":
    main()
