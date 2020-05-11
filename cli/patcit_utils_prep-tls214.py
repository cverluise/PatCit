import os

import click


@click.command()
@click.argument("path", required=False, type=str)
def main(path):
    """
    Process names of files created by split cli to get back to usual patterns.
    Ex: *.text.gz.sub-aa -> *_sub-aa.text.gz
    :param path: str
    :return:
    """
    for src_file in [f for f in os.listdir(path) if "sub" in f.split(".")[-1]]:
        tmp = src_file.split(".")
        tmp = [tmp[0] + "_" + tmp[-1], tmp[1]]
        dest_file = ".".join(tmp)
        os.rename(path + src_file, path + dest_file)


if __name__ == "__main__":
    main()
