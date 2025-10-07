import pytest
from password_validator.validator import validate_password, PasswordValidationError, _has_sequence

# -- testes unitários para utilitário de sequência (cobertura isolada) ---
def test_has_sequence_detects_alpha_sequence():
    assert _has_sequence("xxabcdyy") is True

def test_has_sequence_detects_numeric_sequence():
    assert _has_sequence("xx1234yy") is True

def test_has_sequence_returns_false_for_non_sequence():
    assert _has_sequence("a1b2c3") is False

# -- testes positivos (casos válidos) ---
def test_validate_password_success_minimum_requirements():
    pwd = "Aa1!aaaa"  # 8 chars, has upper, lower, digit, special
    assert validate_password(pwd) is True

def test_validate_password_success_long_with_two_specials():
    pwd = "A" + "a"*30 + "1!"  # length 33, includes 2 specials required (here only one '!' so adjust)
    # make two specials:
    pwd = "A" + "a"*30 + "1!@"  # now length 34 and two specials
    assert validate_password(pwd) is True

# -- testes de falha (cada regra deve lançar uma mensagem apropriada) ---
@pytest.mark.parametrize("pwd, msg_sub", [
    (None, "nula"),  # nulo
    (12345, "string"),  # tipo errado
])
def test_validate_password_invalid_type_or_none(pwd, msg_sub):
    with pytest.raises(PasswordValidationError) as exc:
        validate_password(pwd)
    assert msg_sub in str(exc.value).lower()

def test_validate_password_too_short():
    with pytest.raises(PasswordValidationError) as exc:
        validate_password("Aa1!")  # 4 chars
    assert "entre 8 e 64" in str(exc.value).lower()

def test_validate_password_too_long():
    long_pwd = "A" * 65 + "a1!"  # >64 (this will be >64)
    with pytest.raises(PasswordValidationError) as exc:
        validate_password(long_pwd)
    assert "entre 8 e 64" in str(exc.value).lower()

def test_validate_password_contains_space():
    with pytest.raises(PasswordValidationError) as exc:
        validate_password("Aa1! aaaa")
    assert "não pode conter espaços" in str(exc.value).lower()

def test_validate_password_missing_uppercase():
    with pytest.raises(PasswordValidationError) as exc:
        validate_password("aa1!aaaa")
    assert "maiúscula" in str(exc.value).lower()

def test_validate_password_missing_lowercase():
    with pytest.raises(PasswordValidationError) as exc:
        validate_password("AA1!AAAA")
    assert "minúscula" in str(exc.value).lower()

def test_validate_password_missing_digit():
    with pytest.raises(PasswordValidationError) as exc:
        validate_password("Aa!aaaaa")
    assert "dígito" in str(exc.value).lower()

def test_validate_password_missing_special():
    with pytest.raises(PasswordValidationError) as exc:
        validate_password("Aa1aaaaa")
    assert "caractere especial" in str(exc.value).lower()

def test_validate_password_common_password():
    # 'password' está na lista de common_passwords.txt
    with pytest.raises(PasswordValidationError) as exc:
        validate_password("password")
    assert "muito comum" in str(exc.value).lower()

def test_validate_password_sequence_alpha_detected():
    with pytest.raises(PasswordValidationError) as exc:
        validate_password("Abcd1!aa")  # contém 'abcd' (case-insensitive)
    assert "sequências simples" in str(exc.value).lower()

def test_validate_password_sequence_digits_detected():
    with pytest.raises(PasswordValidationError) as exc:
        validate_password("Aa1234!a")
    assert "sequências simples" in str(exc.value).lower()

def test_validate_password_long_requires_two_specials():
    # length 33 with only one special -> should fail
    pwd = "A" + "a"*30 + "1!"  # only one special '!'
    # ensure length > 32
    assert len(pwd) > 32
    with pytest.raises(PasswordValidationError) as exc:
        validate_password(pwd)
    assert "requerem pelo menos 2 caracteres especiais" in str(exc.value).lower()
