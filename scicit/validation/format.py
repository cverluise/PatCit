import datetime
import re

regex = re.compile(r"[\n\r\t]")


def clean_string(value):
    """
    Return the value without string control characters. Nb: Only strings are actually modified
    :param value: obj
    :return: str
    """
    if value and isinstance(value, str):
        value = regex.sub("", str(value))
        value = value.lower()
    return value


def roman_to_int(s: str):
    """
    Return a digit from a roman numeral (<s>)
    :param s: str
    :return: int
    """
    rom_val = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    int_val = 0
    try:
        for i in range(len(s)):
            if i > 0 and rom_val[s[i]] > rom_val[s[i - 1]]:
                int_val += rom_val[s[i]] - 2 * rom_val[s[i - 1]]
            else:
                int_val += rom_val[s[i]]
            out = int_val
    except KeyError:
        out = s
    return out


def to_int(s):
    """
    Return <s> as an integer if possible. Else None.
    :param s: str
    :return: int (or None)
    """
    if s:
        try:
            out = int(s)
        except ValueError:
            out = None
    else:
        out = None
    return out


def to_number(val):
    """
    Return a number from <val> if possible. Roman numeral enabled
    :param val:obj
    :return: int or None
    """
    if isinstance(val, str):
        out = to_int(roman_to_int(val))
    elif isinstance(val, int):
        out = val
    else:
        out = None
    return out


def is_date_format(s):
    """
    Return True if s has a date format ('%Y-%m-%d' or '%Y-%m' or '%Y'), else False
    :param s: obj
    :return: bool
    """
    s = str(s)
    out = True
    try:
        datetime.datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        try:
            datetime.datetime.strptime(s, "%Y-%m")
        except ValueError:
            try:
                datetime.datetime.strptime(s, "%Y")
            except ValueError:
                out = False
    return out
