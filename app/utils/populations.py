"""app.utils.populations.py"""
import logging

import requests

LOGGER = logging.getLogger(__name__)

# Fetching of the populations.
def fetch_populations():
    """
    Returns a dictionary containing the population of each country fetched from the GeoNames.
    https://www.geonames.org/

    :returns: The mapping of populations.
    :rtype: dict
    """
    LOGGER.info("Fetching populations...")

    # Mapping of populations
    mappings = {}

    # Fetch the countries.
    countries = requests.get("http://api.geonames.org/countryInfoJSON?username=dperic").json()["geonames"]

    # Go through all the countries and perform the mapping.
    for country in countries:
        mappings.update({country["countryCode"]: int(country["population"]) or None})

    # Finally, return the mappings.
    return mappings


# Mapping of alpha-2 codes country codes to population.
POPULATIONS = fetch_populations()

# Retrieving.
def country_population(country_code, default=None):
    """
    Fetches the population of the country with the provided country code.

    :returns: The population.
    :rtype: int
    """
    return POPULATIONS.get(country_code, default)
