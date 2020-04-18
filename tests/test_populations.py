"""tests.test_populations.py"""
import pytest
import requests.exceptions
import responses

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


@responses.activate
@pytest.mark.parametrize(
    "body_arg, json_arg",
    [(NOT_FOUND_HTML, None), (None, {"foo": "bar"}), (requests.exceptions.Timeout("Forced Timeout"), None)],
)
def test_fetch_populations(body_arg, json_arg):
    responses.add(responses.GET, app.utils.populations.GEONAMES_URL, body=body_arg, json=json_arg)

    assert app.utils.populations.fetch_populations()
