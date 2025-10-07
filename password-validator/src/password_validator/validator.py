import re
from pathlib import Path
from typing import List

BASE_DIR = Path(__file__).parent
COMMON_PASSWORDS_FILE = BASE_DIR / "common_passwords.txt"

class PasswordValidationError(ValueError):
    """Erro lançado quando a senha é inválida segundo as regras de negócio."""

def _load_common_passwords() -> List[str]:
    try:
        with COMMON_PASSWORDS_FILE.open("r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

COMMON_PASSWORDS = _load_common_passwords()

# regex patterns
UPPER_RE = re.compile(r"[A-Z]")
LOWER_RE = re.compile(r"[a-z]")
DIGIT_RE = re.compile(r"\d")
SPECIAL_RE = re.compile(r"[^A-Za-z0-9]")  # inclui pontuação, mas não espaço
WHITESPACE_RE = re.compile(r"\s")

def _has_sequence(password: str, length: int = 4) -> bool:
    """
    Detecta sequências simples alfabéticas ou numéricas em ordem crescente,
    por exemplo 'abcd', '1234'.
    Retorna True se encontrar qualquer sequência de 'length' caracteres.
    """
    s = password.lower()
    # check alphabetic sequences
    alpha = "abcdefghijklmnopqrstuvwxyz"
    for i in range(len(alpha) - length + 1):
        seq = alpha[i:i+length]
        if seq in s:
            return True
    # check digit sequences
    digits = "0123456789"
    for i in range(len(digits) - length + 1):
        seq = digits[i:i+length]
        if seq in s:
            return True
    return False

def validate_password(password: str) -> bool:
    """
    Valida a senha de acordo com as regras de negócio.
    Retorna True quando válida. Lança PasswordValidationError com mensagem descritiva quando inválida.
    """
    if password is None:
        raise PasswordValidationError("Senha não pode ser nula")

    if not isinstance(password, str):
        raise PasswordValidationError("Senha deve ser uma string")

    length = len(password)
    if length < 8 or length > 64:
        raise PasswordValidationError("Senha deve ter entre 8 e 64 caracteres")

    if WHITESPACE_RE.search(password):
        raise PasswordValidationError("Senha não pode conter espaços em branco")

    if not UPPER_RE.search(password):
        raise PasswordValidationError("Senha deve conter pelo menos uma letra maiúscula")

    if not LOWER_RE.search(password):
        raise PasswordValidationError("Senha deve conter pelo menos uma letra minúscula")

    if not DIGIT_RE.search(password):
        raise PasswordValidationError("Senha deve conter pelo menos um dígito")

    if not SPECIAL_RE.search(password):
        raise PasswordValidationError("Senha deve conter pelo menos um caractere especial")

    # regra extra: mais de 32 caracteres requer pelo menos 2 caracteres especiais
    if length > 32:
        specials = len(SPECIAL_RE.findall(password))
        if specials < 2:
            raise PasswordValidationError("Senhas com mais de 32 caracteres requerem pelo menos 2 caracteres especiais")

    # checar se é senha comum (case-insensitive)
    if password.lower() in (p.lower() for p in COMMON_PASSWORDS):
        raise PasswordValidationError("Senha é muito comum")

    # checar sequências simples
    if _has_sequence(password, length=4):
        raise PasswordValidationError("Senha não pode conter sequências simples de 4 caracteres (ex.: 'abcd' ou '1234')")

    return True
