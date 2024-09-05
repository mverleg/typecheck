
from typecheck.syntree import Add, Sub, Mul, Div, Literal, IntLiteral, RealLiteral, TextLiteral, Expression
from typecheck.typecheck import check


def test_number_addition():
    assert check(Add(IntLiteral(1), IntLiteral(2))) is None


