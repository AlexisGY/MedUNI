import pytest
from app.services.medicos_service import listar_medicos

# Tests para listar_medicos()
@pytest.mark.parametrize(
    "especialidad_id, expected_count",
    [
        (1, 2),
        (2, 0),
        (3, 0)
    ]
)
def test_listar_medicos(especialidad_id, expected_count):
    medicos = listar_medicos(especialidad_id)

    assert isinstance(medicos, list)

    if expected_count > 0:
        assert len(medicos) == expected_count

        for m in medicos:
            assert isinstance(m, dict)
            assert set(m.keys()) == {"id", "nombres", "apellidos", "especialidad_id"}

            assert isinstance(m["id"], int)
            assert isinstance(m["nombres"], str)
            assert isinstance(m["apellidos"], str)
            assert m["nombres"] != ""
            assert m["apellidos"] != ""

            assert m["especialidad_id"] == especialidad_id
    else:
        assert medicos == []
