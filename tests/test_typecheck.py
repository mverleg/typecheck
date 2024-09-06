from typecheck.syntree import Add, Sub, Mul, Div, IntLiteral, TextLiteral, FuncDecl
from typecheck.typ import Int, Real
from typecheck.typecheck import check, infer


def test_number_literal():
    assert infer(IntLiteral(1)) == Int


def test_number_addition():
    assert infer(Add(IntLiteral(1), IntLiteral(2))) == Int


def test_string_addition_etc():
    assert infer(Add(IntLiteral(1), TextLiteral('hello'))) == 'no variant of Add for arguments (Int, Text)'
    assert infer(Sub(TextLiteral('hello'), IntLiteral(1))) == 'no variant of Sub for arguments (Text, Int)'
    assert infer(Mul(IntLiteral(1), TextLiteral('hello'))) == 'no variant of Mul for arguments (Int, Text)'
    assert infer(Div(TextLiteral('hello'), IntLiteral(1))) == 'no variant of Div for arguments (Text, Int)'


def test_function_call():
    check([
        FuncDecl('addi', [Int, Int,], [Int,]),
        FuncDecl('addr', [Real, Real,], [Real,]),
    ])
