import pytest
from app.services.EspecialidadesService import listar_especialidades

@pytest.mark.parametrize("expected_keys, expected_count", [(
    ["id", "nombre", "estado"], 15)],
)
def test_listar_especialidades_keys(expected_keys, expected_count):
    especialidades = listar_especialidades()

    assert especialidades is not None
    assert isinstance(especialidades, list)
    assert len(especialidades) == expected_count

    for esp in especialidades:
        assert all(key in esp for key in expected_keys)
