import pytest
from app.utils import countrycodes

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
def test_countrycodes_is_3166_1(country_name, expected_country_code):
    assert countrycodes.country_code(country_name) == expected_country_code


@pytest.mark.parametrize(
    "country_name_synonym, expected_country_code",
    [("Deutschland", "DE"), ("Iran (Islamic Republic of)", "IR"), ("British Virgin Islands", "VG")],
)
def test_countrycodes_synonym(country_name_synonym, expected_country_code):
    assert countrycodes.country_code(country_name_synonym) == expected_country_code
