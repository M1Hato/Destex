import pytest

@pytest.mark.asyncio
async def test_register_user_api(client, db_session):
    # Дані для нового користувача
    user_data = {
        "email": "api_regtest@gmail.com",
        "username": "api_tester",
        "password": "password123"
    }
    response = await client.post("/auth/register", json=user_data)

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "api_regtest@gmail.com"
    assert "id" in data