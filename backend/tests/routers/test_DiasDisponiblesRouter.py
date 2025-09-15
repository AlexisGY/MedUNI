import pytest
from datetime import date

@pytest.mark.asyncio
async def test_get_dias(monkeypatch, client):
    monkeypatch.setattr("app.services.DiasDisponiblesService.listarDiasSemana", lambda eid, s: [
        {"fecha": str(date.today()), "disponible": True}
    ])
    response = await client.get("/disponibilidad/1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert "fecha" in data[0]
    assert "disponible" in data[0]
