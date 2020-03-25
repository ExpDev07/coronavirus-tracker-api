
import pytest

@pytest.mark.parametrize("route",["/", "/docs", "/openapi.json"])
def test_swagger(api_client, route):
    """Test that the swagger ui, redoc and openapi json are available."""
    response = api_client.get(route)
    print(f"GET {route} {response}\n\n{response.content}")
    assert response.status_code == 200
