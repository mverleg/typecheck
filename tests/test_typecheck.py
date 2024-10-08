from typecheck.syntree import BinaryMathOp as BOp, Assignment, ReadVar
from typecheck.syntree import IntLiteral, TextLiteral, FuncDecl, FuncCall, RealLiteral
from typecheck.typ import Int, Real, Null, Text
from typecheck.typecheck import check


def test_empty_program():
    assert check([]) == Null


def test_number_literal():
    assert check([IntLiteral(1)]) == Int
    assert check([IntLiteral(1)]).type_name() == 'int'


def test_number_addition():
    assert check([BOp.add(IntLiteral(1), IntLiteral(2))]) == Int


def test_string_addition_etc():
    assert check([BOp.add(IntLiteral(1), TextLiteral('hello'))]) == "none of 2 variants of 'add' accept argument of types (int, text)"
    assert check([BOp.sub(TextLiteral('hello'), IntLiteral(1))]) == "none of 2 variants of 'sub' accept argument of types (text, int)"
    assert check([BOp.mul(IntLiteral(1), TextLiteral('hello'))]) == "none of 2 variants of 'mul' accept argument of types (int, text)"
    assert check([BOp.div(TextLiteral('hello'), IntLiteral(1))]) == "none of 2 variants of 'div' accept argument of types (text, int)"


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
        Assignment('a', None, RealLiteral(1)),
        FuncCall('a', [RealLiteral(1),]),
    ]) == "cannot call 'a' because it is a real, not a function"


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
    ]) == "cannot call function 'f' because argument 1 is of type real, while int is expected"
    assert check([
        FuncDecl('f', [Int, Text,], Null),
        FuncCall('f', [IntLiteral(1), IntLiteral(1),]),
    ]) == "cannot call function 'f' because argument 2 is of type int, while text is expected"


def test_assign_and_read_infer():
    assert check([
        Assignment('a', None, RealLiteral(1)),
        ReadVar('a'),
    ]) == Real


def test_assign_and_read_declared():
    assert check([
        Assignment('a', Real, RealLiteral(1)),
        ReadVar('a'),
    ]) == Real


def test_backpropagate_type_assignment_simple():
    #TODO @mark: actually this just forward propagates because type of 'a' is known
    # it needs to use some unknowns and sybtyping, e.g. if beginning only knows 'a' is Number, but 'c' is integer
    assert check([
        Assignment('a', None, IntLiteral(1)),
        Assignment('b', None, ReadVar('a')),
        FuncDecl('f', [Int,], Real),
        FuncCall('f', [ReadVar('b')]),
        ReadVar('a'),
    ]) == Int


def test_backpropagate_type_assignment_binop():
    #TODO @mark: see test_backpropagate_type_assignment_simple ^
    assert check([
        Assignment('a', None, IntLiteral(1)),
        Assignment('b', None, IntLiteral(1)),
        Assignment('c', None, BOp.add(ReadVar('b'), ReadVar('a'))),
        Assignment('d', None, BOp.add(ReadVar('a'), ReadVar('c'))),
        FuncDecl('f', [Int,], Real),
        FuncCall('f', [ReadVar('d')]),
        ReadVar('a'),
    ]) == Int


def test_declare_self_ref():
    assert check([
        Assignment('a', Text, ReadVar('a')),
    ]) == "variable 'a' not found"


def test_assign_wrong_type():
    assert check([
        Assignment('a', Text, RealLiteral(1)),
    ]) == "cannot declare 'a' with expression of type 'real', because it is not compatible with the declared type 'text'"


def test_assign_and_read_different_type():
    assert check([
        Assignment('a', None, RealLiteral(1)),
        Assignment('b', Text, ReadVar('a')),
    ]) == "cannot declare 'b' with expression of type 'real', because it is not compatible with the declared type 'text'"


def test_assign_to_self():
    assert check([
        Assignment('a', None, IntLiteral(1)),
        Assignment('a', None, ReadVar('a')),
        BOp.add(ReadVar('a'), ReadVar('a')),
    ]) == Int


def test_redeclare_same_var():
    assert check([
        Assignment('a', Int, IntLiteral(1)),
        Assignment('a', Int, IntLiteral(1)),  # compatible
    ]) == ("variable 'a' cannot be declared because it is already declared (as variable of type 'int') "
           "(interpreting as declaration because of 'int' type annotation)")
    assert check([
        Assignment('a', Int, IntLiteral(1)),
        Assignment('a', Real, RealLiteral(1)),  # incompatible
    ]) == ("variable 'a' cannot be declared because it is already declared (as variable of type 'int') "
           "(interpreting as declaration because of 'real' type annotation)")


def test_redeclare_func_as_var():
    assert check([
        FuncDecl('q', [Int,], Real),
        Assignment('q', Int, IntLiteral(1)),
    ]) == ("variable 'q' cannot be declared because it is already declared (as variable of type 'fun(int) -> real') "
           "(interpreting as declaration because of 'int' type annotation)")
    assert check([
        Assignment('q', Int, IntLiteral(1)),
        FuncDecl('q', [Int,], Real),
    ]) == "function name 'q' already declared (as int)"


def test_reassign_same_type():
    assert check([
        Assignment('a', None, RealLiteral(1)),
        Assignment('a', None, RealLiteral(2)),
        ReadVar('a'),
    ]) == Real


def test_reassign_different_type():
    assert check([
        Assignment('a', None, RealLiteral(1)),
        Assignment('a', None, TextLiteral("word")),
        ReadVar('a'),
    ]) == ("cannot assign expression of type 'text' to variable 'a' because its "
           "previously declared or inferred type should be 'real'")


def test_assignment_is_not_variable():
    assert check([
        FuncDecl('f', [Int,], Null),
        Assignment('f', None, RealLiteral(1)),
        ReadVar('a'),
    ]) == "cannot assign variable 'f' because it is not mutable"


def test_assign_function_result_infer():
    assert check([
        FuncDecl('f', [Int,], Real),
        Assignment('a', None, FuncCall('f', [IntLiteral(1)])),
        ReadVar('a')
    ]) == Real


def test_assign_function_result_declared():
    assert check([
        FuncDecl('f', [Int,], Real),
        Assignment('a', Real, FuncCall('f', [IntLiteral(1)])),
        ReadVar('a')
    ]) == Real


def test_call_function_with_variable_args():
    assert check([
        FuncDecl('f', [Real,], Real),
        Assignment('a', None, RealLiteral(1)),
        FuncCall('f', [ReadVar('a')]),
    ]) == Real


