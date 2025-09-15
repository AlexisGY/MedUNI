import pytest

@pytest.mark.asyncio
async def test_login_exitoso(monkeypatch, client):
    monkeypatch.setattr("app.routers.Auth.loginUsuario", lambda u, p: True)
    response = await client.post("/auth/login", json={"username": "test", "password": "123"})
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert data["user"] == "test"


@pytest.mark.asyncio
async def test_login_fallido(monkeypatch, client):
    monkeypatch.setattr("app.services.UserService.loginUsuario", lambda u, p: False)
    response = await client.post("/auth/login", json={"username": "bad", "password": "wrong"})
    assert response.status_code == 401
