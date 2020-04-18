"""tests.test_populations.py"""
import pytest
import requests.exceptions
import responses

import app.io
import app.utils.populations

NOT_FOUND_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Error</title>
</head>
<body>
<pre>Not Found</pre>
</body>
</html>"""

SAMPLE_GEONAMES_JSON = {
    "geonames": [
        {
            "continent": "EU",
            "capital": "Andorra la Vella",
            "languages": "ca",
            "geonameId": 3041565,
            "south": 42.42874300100004,
            "isoAlpha3": "AND",
            "north": 42.65576500000003,
            "fipsCode": "AN",
            "population": "77006",
            "east": 1.786576000000025,
            "isoNumeric": "020",
            "areaInSqKm": "468.0",
            "countryCode": "AD",
            "west": 1.413760001000071,
            "countryName": "Andorra",
            "continentName": "Europe",
            "currencyCode": "EUR",
        },
        {
            "continent": "AS",
            "capital": "Abu Dhabi",
            "languages": "ar-AE,fa,en,hi,ur",
            "geonameId": 290557,
            "south": 22.6315119400001,
            "isoAlpha3": "ARE",
            "north": 26.0693916590001,
            "fipsCode": "AE",
            "population": "9630959",
            "east": 56.381222289,
            "isoNumeric": "784",
            "areaInSqKm": "82880.0",
            "countryCode": "AE",
            "west": 51.5904085340001,
            "countryName": "United Arab Emirates",
            "continentName": "Asia",
            "currencyCode": "AED",
        },
    ]
}


@responses.activate
@pytest.mark.parametrize(
    "body_arg, json_arg",
    [
        (None, SAMPLE_GEONAMES_JSON),
        (NOT_FOUND_HTML, None),
        (None, {"foo": "bar"}),
        (requests.exceptions.Timeout("Forced Timeout"), None),
    ],
)
def test_fetch_populations(body_arg, json_arg):
    responses.add(responses.GET, app.utils.populations.GEONAMES_URL, body=body_arg, json=json_arg)

    assert app.utils.populations.fetch_populations()
