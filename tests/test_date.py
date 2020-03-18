import pytest

from app.utils import date


@pytest.mark.parametrize("str_date, fuzzy_bool, expected_value",
                         [("1990-12-1", False, True),
                          ("2005/3", False, True),
                          ("Jan 19, 1990", False, True),
                          ("today is 2019-03-27", False, False),
                          ("Monday at 12:01am", False, True),
                          ("xyz_not_a_date", False, False),
                          ("yesterday", False, False),
                          ("today is 2019-03-27", True, True)])
def test_is_date(str_date, fuzzy_bool, expected_value):
    """
    Testdata from https://stackoverflow.com/a/25341965/7120095
    """
    assert date.is_date(str_date, fuzzy=fuzzy_bool) is expected_value
