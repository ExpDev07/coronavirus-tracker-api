import pytest

from app.utils.countries import  CountryCodeProvider

"""
Todo:
    * Test cases for capturing of stdout/stderr
"""

country_code_provider = CountryCodeProvider()

@pytest.mark.parametrize(
    "country_name,expected_country_code",
    [
        ("Germany", "DE"),

       ("Bolivia, Plurinational State of", "BO"),
        ("Korea, Democratic People's Republic of", "KP"),
        ("US", "US"),
        ("BlaBla", country_code_provider.default_code),
        ("Others", country_code_provider.default_code),
    ],
)
def test_countries_country_name__country_code(country_name, expected_country_code):
    assert country_code_provider.country_code(country_name) == expected_country_code


def test_singleton():
    a = CountryCodeProvider()
    b = CountryCodeProvider()

    assert a is not None
    assert a is b
    assert id(a) == id(b)
