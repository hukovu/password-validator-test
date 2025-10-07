# Password Validator (Python)

Pequena aplicação Python que valida senhas segundo regras de negócio definidas e possui uma suíte de testes unitários (pytest) com cobertura (pytest-cov).

## Conteúdo entregue
- Código-fonte da aplicação em `src/password_validator/`
- Testes unitários em `tests/test_validator.py`
- Arquivo `common_passwords.txt` com exemplos de senhas comuns
- Instruções para executar e gerar relatório de cobertura

## Regras de Negócio Testadas

1. A senha deve ter entre **8** e **64** caracteres (inclusive).
2. Deve conter **pelo menos uma letra maiúscula**.
3. Deve conter **pelo menos uma letra minúscula**.
4. Deve conter **pelo menos um dígito**.
5. Deve conter **pelo menos um caractere especial** (não alfanumérico, sem contar espaço).
6. Não pode conter **espaços em branco**.
7. Não pode ser uma **senha comum** (lista em `common_passwords.txt`).
8. Não pode conter **sequências simples** (alfabéticas ou numéricas) de 4 caracteres em ordem crescente, por exemplo `abcd` ou `1234`.
9. Se a senha tiver **mais de 32** caracteres, deve conter **pelo menos 2 caracteres especiais**.

Todos os itens acima possuem testes que gerenciam tanto casos de sucesso quanto de falha, conforme o arquivo `tests/test_validator.py`.

## Como rodar localmente

### Pré-requisitos
- Python 3.10+ instalado
- (Opcional) Poetry para gerenciar dependências ou pip + venv

### Com pip + venv
```bash
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
.venv\Scripts\activate      # Windows PowerShell

pip install -U pip
pip install pytest pytest-cov
