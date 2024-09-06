from typecheck.syntree import Add, Sub, Mul, Div, IntLiteral, TextLiteral, FuncDecl, FuncCall, RealLiteral
from typecheck.typ import Int, Real, Null, Text
from typecheck.typecheck import check


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
    ]) == Int


def test_function_call_wrong_name():
    assert check([
        FuncDecl('f', [Int,], Null),
        FuncCall('g', [RealLiteral(1),]),
    ]) == "cannot call function 'g' because no such function is known"


def test_function_call_is_not_func():
    #TODO @mark: impl variables or other named things first
    pass


def test_function_call_wrong_arg_cnt():
    assert check([
        FuncDecl('f', [Int, Int,], Null),
        FuncCall('f', [RealLiteral(1),]),
    ]) == "cannot call function 'f' with 1 args because it expects 2"
    assert check([
        FuncDecl('f', [], Null),
        FuncCall('f', [RealLiteral(1),]),
    ]) == "cannot call function 'f' with 1 args because it expects 0"


def test_function_call_wrong_arg_type():
    assert check([
        FuncDecl('f', [Int,], Null),
        FuncCall('f', [RealLiteral(1),]),
    ]) == "cannot call function 'f' because argument 1 is of type Real, while Int is expected"
    assert check([
        FuncDecl('f', [Int, Text,], Null),
        FuncCall('f', [IntLiteral(1), IntLiteral(1),]),
    ]) == "cannot call function 'f' because argument 2 is of type Int, while Text is expected"


