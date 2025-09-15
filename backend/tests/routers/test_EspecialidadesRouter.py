import pytest

@pytest.mark.asyncio
async def test_get_especialidades(monkeypatch, client):
    monkeypatch.setattr("app.services.EspecialidadesService.listarEspecialidades", lambda: [
        {"id": 1, "nombre": "Cardiología", "estado": True}
    ])
    response = await client.get("/especialidades/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert "nombre" in data[0]
