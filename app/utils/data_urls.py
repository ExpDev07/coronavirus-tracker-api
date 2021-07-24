"""app.utils.data_urls.py"""

import enum


class DataURLs(str, enum.Enum):
    """
    URLs available for retrieving data from each possible source.
    """

    JHU = "https://raw.githubusercontent.com/CSSEGISandData/2019-nCoV/master/csse_covid_19_data/csse_covid_19_time_series/"
    CSBS = "https://facts.csbs.org/covid-19/covid19_county.csv"
    NYT = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
