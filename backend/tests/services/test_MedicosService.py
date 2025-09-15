import pytest
from app.services import MedicosService


@pytest.mark.parametrize("especialidadId", [1, 6, 7, 11, 13])
def test_listarMedicos_devuelve_medicos_validos(especialidadId):
    result = MedicosService.listarMedicos(especialidadId)
    assert isinstance(result, list)
    assert all(isinstance(m, dict) for m in result)
    assert all("id" in m and "nombre" in m and "apellido" in m and "especialidadId" in m for m in result)
    assert all(m["especialidadId"] == especialidadId for m in result)
    assert len(result) >= 1


@pytest.mark.parametrize("especialidadId", [999, -1, 0, 69])
def test_listarMedicos_especialidad_inexistente(especialidadId):
    result = MedicosService.listarMedicos(especialidadId)
    assert isinstance(result, list)
    assert result == []
