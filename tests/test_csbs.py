import pytest

from app.services.location import csbs
from tests.conftest import mock_client_session
from tests.conftest import mocked_session_get


def mocked_csbs_requests_get(*args, **kwargs):
    class FakeRequestsGetResponse:
        """
        Returns instance of `FakeRequestsGetResponse`
        when calling `app.services.location.csbs.requests.get()
        """

        def __init__(self):
            self.text = self.read_file()

        def read_file(self):
            """
            Mock HTTP GET-method and return text from file
            """
            filepath = "tests/example_data/covid19_county.csv"
            print("Try to read {}".format(filepath))
            with open(filepath, "r") as file:
                return file.read()

    return FakeRequestsGetResponse()


@pytest.mark.asyncio
async def test_get_locations():
    async with mock_client_session() as mocked_client_session:
        mocked_client_session.get = mocked_session_get
        data = await csbs.get_locations()

    assert isinstance(data, list)

    # check to see that Unknown/Unassigned has been filtered
    for d in data:
        assert d.county != "Unknown"
        assert d.county != "Unassigned"
