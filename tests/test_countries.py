import pytest

from app.utils import countries


"""
Todo:
    * Test cases for capturing of stdout/stderr
"""


@pytest.mark.parametrize(
    "country_name,expected_country_code",
    [
        ("Germany", "DE"),
        ("Bolivia, Plurinational State of", "BO"),
        ("Korea, Democratic People's Republic of", "KP"),
        ("BlaBla", "XX"),
    ],
)
def test_countries_country_name__country_code(country_name, expected_country_code):
    assert countries.country_code(country_name) == expected_country_code


@pytest.mark.parametrize(
    "country_name_alias, expected_country_code",
    [("Deutschland", "DE"), ("Iran (Islamic Republic of)", "IR"), ("British Virgin Islands", "VG")],
)
def test_country_name_alias(country_name_alias, expected_country_code):
    assert countries.country_code(country_name_alias) == expected_country_code
