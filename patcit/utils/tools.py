import dateparser

TODAY = int(dateparser.parse("today").strftime("%Y%m%d"))


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
