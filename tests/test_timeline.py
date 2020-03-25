from collections import OrderedDict
from unittest import mock

import pytest

from app import timeline


def test_timeline_class():
    # Unordered timeseries.
    timeseries = {
        "1/24/20": 5,
        "1/22/20": 2,
        "1/25/20": 7,
        "1/23/20": 3,
    }

    history_data = timeline.Timeline(history=timeseries)

    # validate last value
    assert history_data.latest == 7

    # validate order
    assert list(dict(history_data.timeline).keys()) == ["1/22/20", "1/23/20", "1/24/20", "1/25/20"]

    # validate serialize
    check_serialize = {
        "latest": 7,
        "timeline": OrderedDict([("1/22/20", 2), ("1/23/20", 3), ("1/24/20", 5), ("1/25/20", 7),]),
    }

    assert dict(history_data.serialize()) == check_serialize
