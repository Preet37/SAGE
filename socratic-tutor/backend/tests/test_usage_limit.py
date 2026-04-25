import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.usefixtures("_low_usage_limit")
async def test_usage_limit_enforced(client: AsyncClient, auth_headers: dict):
    """With daily limit set to 2, the 3rd chat request should return 429."""
    body = {
        "messages": [{"role": "user", "content": "hello"}],
        "lesson_id": "nonexistent",
    }

    for _ in range(2):
        resp = await client.post("/tutor/chat", json=body, headers=auth_headers)
        # 404 is expected because the lesson doesn't exist, but the usage
        # counter still increments since enforce_usage_limit runs first.
        assert resp.status_code == 404

    resp = await client.post("/tutor/chat", json=body, headers=auth_headers)
    assert resp.status_code == 429
    assert "limit" in resp.json()["detail"].lower()
