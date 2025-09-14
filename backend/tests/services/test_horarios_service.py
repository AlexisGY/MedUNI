import pytest
from datetime import date
from app.services.HorariosService import gen_horarios

@pytest.mark.parametrize("dia, medico_id", [
    (date(2025, 9, 1), 1),
    (date(2025, 9, 2), 2),
])
def test_gen_horarios_estructura(dia, medico_id):
    horarios = gen_horarios(dia, medico_id)

    assert isinstance(horarios, list)

    if horarios:
        for h in horarios:
            assert isinstance(h, dict)
            assert "hora_inicio" in h
            assert "hora_fin" in h
            assert "disponibilidad" in h
            assert isinstance(h["disponibilidad"], bool)

@pytest.mark.parametrize("dia, medico_id", [
    (date(2025, 9, 1), 1),
    (date(2025, 9, 2), 2),
])
def test_gen_horarios_intervalos(dia, medico_id):
    horarios = gen_horarios(dia, medico_id)

    if horarios:
        for h in horarios:
            hi = h["hora_inicio"]
            hf = h["hora_fin"]
            delta = (hf.hour*60 + hf.minute) - (hi.hour*60 + hi.minute)
            assert delta == 30
            assert hi.minute in [0, 30]
