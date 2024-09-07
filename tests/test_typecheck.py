from typecheck.syntree import IntLiteral, TextLiteral, FuncDecl, FuncCall, RealLiteral, BinaryMathOp as BOp, Assignment, \
    ReadVar
from typecheck.typ import Int, Real, Null, Text
from typecheck.typecheck import check


def test_empty_program():
    assert check([]) == Null

def test_number_literal():
    assert check([IntLiteral(1)]) == Int


def test_number_addition():
    assert check([BOp.add(IntLiteral(1), IntLiteral(2))]) == Int


def test_string_addition_etc():
    assert check([BOp.add(IntLiteral(1), TextLiteral('hello'))]) == 'no variant of Add for arguments (Int, Text)'
    assert check([BOp.sub(TextLiteral('hello'), IntLiteral(1))]) == 'no variant of Sub for arguments (Text, Int)'
    assert check([BOp.mul(IntLiteral(1), TextLiteral('hello'))]) == 'no variant of Mul for arguments (Int, Text)'
    assert check([BOp.div(TextLiteral('hello'), IntLiteral(1))]) == 'no variant of Div for arguments (Text, Int)'


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
    assert check([
        Assignment('a', RealLiteral(1)),
        FuncCall('a', [RealLiteral(1),]),
    ]) == "cannot call 'a' because it is not a function"


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


def test_assign_and_read():
    assert check([
        Assignment('a', RealLiteral(1)),
        ReadVar('a'),
    ]) == Real


def test_reassign_same_type():
    assert check([
        Assignment('a', RealLiteral(1)),
        Assignment('a', RealLiteral(2)),
        ReadVar('a'),
    ]) == Real


def test_reassign_different_type():
    assert check([
        Assignment('a', RealLiteral(1)),
        Assignment('a', TextLiteral("word")),
        ReadVar('a'),
    ]) == "type err"


def test_assignment_is_not_variable():
    assert check([
        FuncDecl('f', [Int,], Null),
        Assignment('f', RealLiteral(1)),
        ReadVar('a'),
    ]) == "type err"


def test_assign_function_result():
    assert check([
        FuncDecl('f', [Int,], Real),
        Assignment('a', FuncCall('f', [IntLiteral(1)])),
        ReadVar('a')
    ]) == Int


def test_call_function_with_variable_args():
    assert check([
        FuncDecl('f', [Int,], Real),
        Assignment('a', RealLiteral(1)),
        FuncCall('f', [ReadVar('a')]),
    ]) == Real
