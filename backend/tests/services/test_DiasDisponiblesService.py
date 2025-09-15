import pytest
from datetime import date
from app.services import DiasDisponiblesService

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