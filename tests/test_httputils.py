import pytest

from app.utils import httputils


@pytest.mark.asyncio
async def test_setup_teardown_client_session():
    with pytest.raises(AttributeError):
        # Ensure client_session is undefined prior to setup
        httputils.CLIENT_SESSION

    await httputils.setup_client_session()

    assert httputils.CLIENT_SESSION

    await httputils.teardown_client_session()
    assert httputils.CLIENT_SESSION.closed

    del httputils.CLIENT_SESSION
