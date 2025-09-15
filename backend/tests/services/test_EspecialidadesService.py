import pytest
from app.services import EspecialidadesService

def test_listarEspecialidades_formato_y_estado():
    result = EspecialidadesService.listarEspecialidades()
    assert isinstance(result, list)
    assert all(isinstance(esp, dict) for esp in result)
    assert all("id" in esp and "nombre" in esp and "estado" in esp for esp in result)
    assert all(esp["estado"] is True for esp in result)


def test_listarEspecialidades_contiene_datos():
    result = EspecialidadesService.listarEspecialidades()
    nombres = [esp["nombre"] for esp in result]
    assert len(nombres) > 0
