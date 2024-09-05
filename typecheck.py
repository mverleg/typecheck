
from syntree import Add, Sub, Mul, Div, Literal, IntLiteral, RealLiteral, TextLiteral, Expression


def check(expr: Expression) -> str | None:
    pass


def test_number_addition():
    assert check(Add(IntLiteral(1), IntLiteral(2))) is None


