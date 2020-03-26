import pytest

from app.utils import continents, countries

@pytest.mark.parametrize(
    "country_name,expected_continent_codes_list",
    [
        ("Germany",                                ["EUR"]),
        ("Bolivia, Plurinational State of",        ["SAC"]),
        ("Korea, Democratic People's Republic of", ["ASI"]),
        ("BlaBla",                                 ["CCC"]),
        ("United States Minor Outlying Islands",   ["OCE", "NAC"]),
        ("Russian Federation",                     ["EUR", "ASI"]),
        ("Armenia",                                ["EUR", "ASI"]),
        ("Georgia",                                ["EUR", "ASI"]),
        ("Cyprus",                                 ["EUR", "ASI"]),
        ("Turkey",                                 ["EUR", "ASI"]),
        ("Kazakhstan",                             ["EUR", "ASI"]),
        ("Azerbaijan",                             ["EUR", "ASI"]),
        (" Azerbaijan",                             ["EUR", "ASI"]),
    ],
)
def test_country_name__continent_codes_list(country_name, expected_continent_codes_list):
    country_code = countries.country_code(country_name)
    continent_codes_list = continents.continent_codes_list(country_code)
    assert continent_codes_list == expected_continent_codes_list
