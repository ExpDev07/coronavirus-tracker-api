"""app.utils.populations.py"""
import json
import logging

import requests

import app.io

LOGGER = logging.getLogger(__name__)
GEONAMES_URL = "http://api.geonames.org/countryInfoJSON"
GEONAMES_BACKUP_PATH = "geonames_population_mappings.json"

# Fetching of the populations.
def fetch_populations(save=False):
    """
    Returns a dictionary containing the population of each country fetched from the GeoNames.
    https://www.geonames.org/

    TODO: only skip writing to the filesystem when deployed with gunicorn, or handle concurent access, or use DB.

    :returns: The mapping of populations.
    :rtype: dict
    """
    LOGGER.info("Fetching populations...")

    # Mapping of populations
    mappings = {}

    # Fetch the countries.
    try:
        countries = requests.get(GEONAMES_URL, params={"username": "dperic"}, timeout=1.25).json()[
            "geonames"
        ]
        # Go through all the countries and perform the mapping.
        for country in countries:
            mappings.update({country["countryCode"]: int(country["population"]) or None})

        if mappings and save:
            LOGGER.info(f"Saving population data to {app.io.save(GEONAMES_BACKUP_PATH, mappings)}")
    except (json.JSONDecodeError, KeyError, requests.exceptions.Timeout) as err:
        LOGGER.warning(f"Error pulling population data. {err.__class__.__name__}: {err}")
        mappings = app.io.load(GEONAMES_BACKUP_PATH)
        LOGGER.info(f"Using backup data from {GEONAMES_BACKUP_PATH}")
    # Finally, return the mappings.
    LOGGER.info("Fetched populations")
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
