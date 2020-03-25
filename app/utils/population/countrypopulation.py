import requests
import csv
from io import StringIO, BytesIO
from cachetools import cached, TTLCache
from zipfile import ZipFile, ZipInfo
from ...utils.countrycodes import *


@cached(cache=TTLCache(maxsize=1024, ttl=3600))
def get_population_dict():
    """
    Creates a dictionary containing the population of each country.
    The data is cached for 1 hour.

    :returns: a dictionary of format country code: population.
    :rtype: dict
    """

    # download file and save it to a buffer
    URL = 'http://api.worldbank.org/v2/en/indicator/SP.POP.TOTL?downloadformat=csv'
    zip_data = BytesIO(requests.get(URL).content)

    #load buffer as ZipFile object
    zipfile = ZipFile(zip_data, mode='r')

    # isolate the and open csv file as StringIO object
    target_file = [x for x in zipfile.namelist() if not x.startswith('Metadata')][0]
    csv_file = StringIO(zipfile.read(target_file).decode('utf-8'))

    # parse csv file as csv.reader
    csv_reader = csv.reader(csv_file, delimiter=',')
    popluation_dict = {}

    for row in csv_reader:

        # verify that row exists 
        if len(row) > 0:

            # verify that country is in database
            if country_in_database(row[0]):

                # Populate dict with last non-None value (https://stackoverflow.com/a/18533669)
                key = country_code(row[0], verbose=False)
                popluation_dict.update({key: int(next((el for el in row[::-1] if el), None))})

    return popluation_dict

