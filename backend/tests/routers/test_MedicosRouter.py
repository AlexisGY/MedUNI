import pytest

@pytest.mark.asyncio
async def test_get_medicos(monkeypatch, client):
    monkeypatch.setattr("app.services.MedicosService.listarMedicos", lambda eid: [
        {"id": 1, "nombre": "Gregory", "apellido": "House", "especialidadId": eid}
    ])
    response = await client.get("/medicos/especialidad/1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["especialidadId"] == 1
