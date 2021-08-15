import pytest

from app.utils import countries_population

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

__instance = None
def getInstance():
     """ Static access method. """
    if countries_population.__instance == None:
        countries_populaiton()
    return countries_population.__instance
    
def __init__(self):
        """ Virtually private constructor. """
      if countries_population.__instance != None:
         raise Exception("This class is a singleton!")
      else:
         countries_population.__instance = self
        
def test_countries_country_name__country_code(country_name, expected_country_code):
    assert countries.country_code(country_name) == expected_country_code
