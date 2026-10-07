"""Calculadora de expressões digitadas.

Python 3.8+ | Sem dependências externas.
Operações: + - * / e parênteses (inclui sinais unários, ex.: -3 + 5).
Usa `ast` em vez de `eval`, então só aceita matemática, nunca código arbitrário.
"""

import ast
import operator

OPERADORES_BINARIOS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}
OPERADORES_UNARIOS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _avaliar(no):
    if isinstance(no, ast.Expression):
        return _avaliar(no.body)
    if isinstance(no, ast.Constant) and type(no.value) in (int, float):
        return no.value
    if isinstance(no, ast.BinOp) and type(no.op) in OPERADORES_BINARIOS:
        return OPERADORES_BINARIOS[type(no.op)](_avaliar(no.left), _avaliar(no.right))
    if isinstance(no, ast.UnaryOp) and type(no.op) in OPERADORES_UNARIOS:
        return OPERADORES_UNARIOS[type(no.op)](_avaliar(no.operand))
    raise ValueError("expressão inválida (use apenas números, + - * / e parênteses)")


def calcular(expressao):
    """Resolve uma expressão como '2 + 3 * (4 - 1)' e devolve o resultado."""
    expressao = expressao.strip().replace(",", ".")  # aceita vírgula decimal
    if not expressao:
        raise ValueError("expressão vazia")
    try:
        arvore = ast.parse(expressao, mode="eval")
    except SyntaxError:
        raise ValueError("sintaxe inválida") from None
    try:
        return _avaliar(arvore)
    except ZeroDivisionError:
        raise ValueError("divisão por zero") from None


def formatar(resultado):
    """Mostra 6.0 como 6 e limita casas decimais para evitar 0.30000000000000004."""
    if isinstance(resultado, float):
        resultado = round(resultado, 10)
        if resultado.is_integer():
            return str(int(resultado))
    return str(resultado)


def main():
    print("Calculadora — digite uma expressão (ex.: 2 + 3 * (4 - 1)). 'sair' encerra.")
    while True:
        try:
            entrada = input(">>> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if entrada.strip().lower() in ("sair", "exit", "q"):
            break
        try:
            print("=", formatar(calcular(entrada)))
        except ValueError as erro:
            print(f"Erro: {erro}")
    print("Até mais!")


if __name__ == "__main__":
    main()
