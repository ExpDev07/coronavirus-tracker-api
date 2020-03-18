from unittest import mock
import pytest

from app import coordinates

@pytest.mark.parametrize("latitude, longitude",
                         [("1", "2"),
                          (100, "2"),
                          (-3, 0),
                          (-10, -10000000)])
def test_coordinates_class(latitude, longitude):
    coord_obj = coordinates.Coordinates(latitude=latitude,
                                        longitude=longitude)

    #validate serialize
    check_obj = {'latitude' : latitude,
                 'longitude': longitude}

    assert coord_obj.serialize() == check_obj
