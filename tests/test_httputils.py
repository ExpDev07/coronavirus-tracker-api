import pytest

from app.utils import httputils


@pytest.mark.asyncio
async def test_setup_teardown_client_session():
    with pytest.raises(AttributeError):
        # Ensure client_session is undefined prior to setup
        httputils.Session.getClientSession()

    await httputils.Session.setup_client_session()

    assert httputils.Session.getClientSession()

    await httputils.Session.teardown_client_session()
    assert httputils.Session.getClientSession().closed

    del httputils.Session.getClientSession()

    del httputils.Session.getClientSession()
