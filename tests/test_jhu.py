from unittest import mock

import pytest

from app import location
from app.services.location import jhu
from tests.conftest import mock_client_session
from tests.conftest import mocked_session_get
from tests.conftest import mocked_strptime_isoformat

DATETIME_STRING = "2020-03-17T10:23:22.505550"


@pytest.mark.asyncio
@mock.patch("app.services.location.jhu.datetime")
async def test_get_locations(mock_datetime):
    mock_datetime.utcnow.return_value.isoformat.return_value = DATETIME_STRING
    mock_datetime.strptime.side_effect = mocked_strptime_isoformat

    async with mock_client_session() as mocked_client_session:
        mocked_client_session.get = mocked_session_get
        output = await jhu.get_locations()

        assert isinstance(output, list)
        assert isinstance(output[0], location.Location)

        # `jhu.get_locations()` creates id based on confirmed list
        location_confirmed = await jhu.get_category("confirmed")
        assert len(output) == len(location_confirmed["locations"])
