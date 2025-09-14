import pytest
from app.services import UserService

@pytest.mark.parametrize(
    "username,password,expected",
    [
        ("20234044I", "111111", True),
        ("20240010E", "123456", True),
        ("20234044I", "11111", False),
        ("20240010E", "l23456", False),
        ("20244044I", "111111", False),
        ("20240100E", "123456", False),
    ]
)
def test_login_user(username, password, expected):
    result = UserService.login_user(username, password)
    assert result == expected

@pytest.mark.parametrize(
    "codigo,exists",
    [
        ("20234044I", True),
        ("20240010E", True),
        ("20244044I", False),
        ("20240100E", False),
    ]
)
def test_get_me(codigo, exists):
    result = UserService.get_me(codigo)

    if exists:
        assert result is not None
        assert result["cod_estudiante"] == codigo
        assert "nombres" in result
        assert "apellidos" in result
        assert "correo" in result
    else:
        assert result is None
