import pytest
from datetime import date, time, datetime, timedelta
from app.services import HorariosService


@pytest.fixture
def fake_db_factory(monkeypatch):
    def _factory(*, horas_disponibles=True):
        class FakeCursor:
            def __init__(self):
                self._result = []

            def execute(self, query, params):
                if "disponibilidad_especialidad" in query:
                    self._result = [(time(8, 0), time(10, 0))] if horas_disponibles else []
                else:
                    self._result = [
                        (time(8, 0), time(8, 30), True),
                        (time(8, 30), time(9, 0), False),
                        (time(9, 0), time(9, 30), True),
                    ]

            def fetchall(self):
                return self._result

            def close(self):
                pass

        class FakeConnection:
            def cursor(self):
                return FakeCursor()

            def close(self):
                pass

        monkeypatch.setattr(HorariosService, "getConnection", lambda: FakeConnection())

    return _factory

@pytest.mark.parametrize("dia,medico_id", [
    (date(2025, 9, 2), 1),
    (date(2025, 9, 4), 1),
])
def test_genHorarios_formato_y_duracion(dia, medico_id, fake_db_factory):
    fake_db_factory(horas_disponibles=True)
    horarios = HorariosService.genHorarios(dia, medico_id)

    assert isinstance(horarios, list)
    if horarios:
        # están ordenados
        horas = [h["horaInicio"] for h in horarios]
        assert horas == sorted(horas)

        for h in horarios:
            assert set(h.keys()) == {"horaInicio", "horaFin", "disponibilidad"}
            assert (h["horaFin"].hour*60 + h["horaFin"].minute) - (h["horaInicio"].hour*60 + h["horaInicio"].minute) == 30
            assert isinstance(h["disponibilidad"], bool)

@pytest.mark.parametrize("dia,medico_id", [
    (date(2025, 9, 7), 1),
    (date(2025, 9, 6), 2),
])
def test_genHorarios_sin_disponibilidad(dia, medico_id, fake_db_factory):
    fake_db_factory(horas_disponibles=False)
    horarios = HorariosService.genHorarios(dia, medico_id)
    assert horarios == []


def test_genHorarios_respeta_parametro_dia(monkeypatch):
    """Verifica que los horarios generados cambian según la fecha solicitada."""

    captured_params = []

    class FakeCursor:
        def __init__(self):
            self._result = []

        def execute(self, query, params):
            if "disponibilidad_especialidad" in query:
                self._result = [(time(8, 0), time(10, 0))]
            else:
                if not isinstance(params[0], date):
                    raise AssertionError("Se esperaba que el parámetro dia fuese una fecha")
                dia = params[0]
                base_hour = 8 + (dia.day % 3)
                hora_inicio = time(base_hour, 0)
                hora_fin = (datetime.combine(dia, hora_inicio) + timedelta(minutes=30)).time()
                self._result = [(hora_inicio, hora_fin, True)]
                captured_params.append(params)

        def fetchall(self):
            return self._result

        def close(self):
            pass

    class FakeConnection:
        def cursor(self):
            return FakeCursor()

        def close(self):
            pass

    monkeypatch.setattr(HorariosService, "getConnection", lambda: FakeConnection())

    dia_1 = date(2025, 9, 2)
    dia_2 = date(2025, 9, 4)

    medico_id = 1
    horarios_dia_1 = HorariosService.genHorarios(dia_1, medico_id)
    horarios_dia_2 = HorariosService.genHorarios(dia_2, medico_id)

    assert captured_params and len(captured_params) == 2
    assert captured_params[0][0] == dia_1
    assert captured_params[1][0] == dia_2

    def expected_hour(dia):
        return time(8 + (dia.day % 3), 0)

    assert horarios_dia_1[0]["horaInicio"] == expected_hour(dia_1)
    assert horarios_dia_2[0]["horaInicio"] == expected_hour(dia_2)
    assert horarios_dia_1[0] != horarios_dia_2[0]
