import pytest

from app.utils import countries
from app.utils import lookup

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
        ("US", "US"),
        ("BlaBla", countries.DEFAULT_COUNTRY_CODE),
        ("Others", countries.DEFAULT_COUNTRY_CODE),
    ],
)
def test_countries_country_name__country_code(country_name, expected_country_code):
    assert lookup.get('country_code',country_name) == expected_country_code
