import pytest
from app.services import UserService


@pytest.mark.parametrize(
    "username,password,expected",
    [
        ("20234044I", "111111", True),
        ("20240010E", "111111", True),
        ("20244017D", "111111", True),
        ("20234044I", "000000", False),
        ("20250000A", "123456", False),
    ]
)
def test_loginUsuario(username, password, expected):
    result = UserService.loginUsuario(username, password)
    assert result is expected


@pytest.mark.parametrize(
    "codigo,exists",
    [
        ("20234044I", True),
        ("20240010E", True),
        ("20244017D", True),
        ("20250000A", False),
    ]
)
def test_getUsuario(codigo, exists):
    result = UserService.getUsuario(codigo)

    if exists:
        assert isinstance(result, dict)
        assert result["codEstudiante"] == codigo
        for key in ("nombres", "apellidos", "correo"):
            assert key in result
    else:
        assert result is None
