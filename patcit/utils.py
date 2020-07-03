from patcit.config import Config
import dateparser

TODAY = int(dateparser.parse("today").strftime("%Y%m%d"))


def str_to_bq_ref(s):
    """
    Return a bq.TableRef from a string like path (e.g npl-parsing.patcit.raw)
    :param s: str
    :return: bq.Tableref
    """
    project_id, dataset_id, table_id = s.split(".")
    config = Config(project_id=project_id, dataset_id=dataset_id)
    return config.table_ref(table_id)


def ref_to_bq_path(ref):
    """
    Return a string like path from a bq.TableRef object
    :param ref: bq.Tableref
    :return: str
    """
    return ".".join(ref._key())


def parse_date(s):
    """
    Return the yyyymmdd format of the natural language date in S
    :param s: str, natural language date (e.g. '19 juin 1991')
    :return: str
    """
    try:
        date = dateparser.parse(s)
    except OverflowError:
        date = 0
    if date:
        date = int(date.strftime("%Y%m%d"))
        if date > TODAY:
            #  handle cases where dateparser parses futuristic dates, which should not be the case
            date = 0
    else:  # default when dateparser.parse fails
        date = 0
    return date
