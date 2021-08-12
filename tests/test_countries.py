import pytest

from app.location import country

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
    assert countries.country_code(country_name) == expected_country_code

__shared_instance = None
@staticmethod
def getInstance():
    """Static Access Methods """
    if Country.__shared_instance == None:
        Country()
    return Country.__shared_instance

def __init__(self) -> None:
    """ Virtual Private Constructor"""
    if Country.__shared_instance != None:
        raise Exception("Singleton Class already initialized. Please use getInstance()")
    else:
        Country.__shared_instance = self
