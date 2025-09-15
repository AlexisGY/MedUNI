import pytest
from datetime import date, time
from app.services import HorariosService

@pytest.mark.parametrize("dia,medico_id", [
    (date(2025, 9, 2), 1),
    (date(2025, 9, 4), 1),
])
def test_genHorarios_formato_y_duracion(dia, medico_id):
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
def test_genHorarios_sin_disponibilidad(dia, medico_id):
    horarios = HorariosService.genHorarios(dia, medico_id)
    assert horarios == []
