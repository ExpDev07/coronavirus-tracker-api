from dateutil.parser import parse

def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.
    - https://stackoverflow.com/a/25341965/7120095

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """

    try: 
        parse(string, fuzzy=fuzzy)
        return True
    except ValueError:
        return False