import pytest

from app.utils import httputils


@pytest.mark.asyncio
async def test_setup_teardown_client_session():
    with pytest.raises(AttributeError):
        # Ensure client_session is undefined prior to setup
        testSession = httputils.Session()

    await testSession.setup_client_session()

    assert testSession.getClientSession()

    await testSession.teardown_client_session()
    assert testSession.getClientSession().closed

    del testSession
