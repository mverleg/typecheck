from typecheck.syntree import Add, Sub, Mul, Div, IntLiteral, TextLiteral, FuncDecl, FuncCall, RealLiteral
from typecheck.typ import Int, Real, Null
from typecheck.typecheck import check, infer


def test_empty_program():
    assert check([]) == Null

def test_number_literal():
    assert check([IntLiteral(1)]) == Int


def test_number_addition():
    assert check([Add(IntLiteral(1), IntLiteral(2))]) == Int


def test_string_addition_etc():
    assert check([Add(IntLiteral(1), TextLiteral('hello'))]) == 'no variant of Add for arguments (Int, Text)'
    assert check([Sub(TextLiteral('hello'), IntLiteral(1))]) == 'no variant of Sub for arguments (Text, Int)'
    assert check([Mul(IntLiteral(1), TextLiteral('hello'))]) == 'no variant of Mul for arguments (Int, Text)'
    assert check([Div(TextLiteral('hello'), IntLiteral(1))]) == 'no variant of Div for arguments (Text, Int)'


def test_function_call_valid():
    assert check([
        FuncDecl('add_i', [Int, Int,], Int),
        FuncDecl('add_r', [Real, Real,], Real),
        FuncCall('add_r', [RealLiteral(1), RealLiteral(2),]),
        FuncCall('add_i', [IntLiteral(1), IntLiteral(2),]),
    ]) is Int

#TODO @mark: test call before declare

