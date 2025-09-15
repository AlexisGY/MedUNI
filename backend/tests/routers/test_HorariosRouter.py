import pytest
@pytest.mark.asyncio
async def test_get_horarios(monkeypatch, client):
    monkeypatch.setattr(
        "app.services.HorariosService.genHorarios",
        lambda self, f, m: [
            {"horaInicio": "08:00", "horaFin": "08:30", "disponibilidad": True}
        ]
    )
    response = await client.get("/horarios/1/2025-09-14")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert "horaInicio" in data[0]
