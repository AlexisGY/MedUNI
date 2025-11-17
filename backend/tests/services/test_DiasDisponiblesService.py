import pytest
from datetime import date, timedelta

from app.services import DiasDisponiblesService


class DummyCursor:
    def __init__(self):
        self._params = None

    def execute(self, query, params):  # pragma: no cover - simple stub
        self._params = params

    def fetchall(self):  # pragma: no cover - simple stub
        inicio, fin, _ = self._params
        dias = []
        actual = inicio
        while actual <= fin:
            dias.append((actual, True))
            actual += timedelta(days=1)
        return dias

    def close(self):  # pragma: no cover - simple stub
        pass


class DummyConnection:
    def cursor(self):  # pragma: no cover - simple stub
        return DummyCursor()

    def close(self):  # pragma: no cover - simple stub
        pass


@pytest.fixture(autouse=True)
def mock_db(monkeypatch):
    monkeypatch.setattr(DiasDisponiblesService, "getConnection", lambda: DummyConnection())


@pytest.mark.parametrize("especialidadId,semanas", [
    (1, 1),
    (2, 2),
    (9999, 1),
])
def test_listarDiasSemana_formato_y_longitud(especialidadId, semanas):
    result = DiasDisponiblesService.listarDiasSemana(especialidadId, semanas)
    assert isinstance(result, list)
    assert len(result) == 7 * semanas
    assert all(isinstance(d["fecha"], date) for d in result)
    assert all(isinstance(d["disponible"], bool) for d in result)


def test_listarDiasSemana_inicia_en_lunes(monkeypatch):
    class FakeDate(date):
        @classmethod
        def today(cls):
            # Miércoles
            return date(2024, 2, 7)

    monkeypatch.setattr(DiasDisponiblesService, "date", FakeDate)

    result = DiasDisponiblesService.listarDiasSemana(especialidadId=1, semanas=1)

    assert result[0]["fecha"].weekday() == 0
