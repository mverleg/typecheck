from typecheck.syntree import Add, IntLiteral, TextLiteral
from typecheck.typ import Int
from typecheck.typecheck import check


def test_number_literal():
    assert check(IntLiteral(1)) == Int


def test_number_addition():
    assert check(Add(IntLiteral(1), IntLiteral(2))) == Int


def test_string_addition():
    assert check(Add(IntLiteral(1), TextLiteral('hello'))) == 'no variant of Add for arguments (Int, Text)'


