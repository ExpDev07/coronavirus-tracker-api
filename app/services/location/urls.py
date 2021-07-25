import enum

# Encapsulate urls into one class, clas URLs serve as aggregate root.
class URLs(str, enum.Enum):

    JHU = "https://raw.githubusercontent.com/CSSEGISandData/2019-nCoV/master/csse_covid_19_data/csse_covid_19_time_series/"
    CSBS = "https://facts.csbs.org/covid-19/covid19_county.csv"
    NYT = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"