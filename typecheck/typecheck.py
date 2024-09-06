from typing import List, Dict

from typing_extensions import assert_never

from typecheck.syntree import IntLiteral, Add, Sub, Mul, Div, RealLiteral, TextLiteral, Statement, FuncDecl, Expression, \
    FuncCall
from typecheck.typ import Type, Int, Real, Text


TypeState = Dict[str, FuncDecl]


def check(prog: List[Statement]) -> None | str:
    types: TypeState = {}
    for stmt in prog:
        if isinstance(stmt, FuncDecl):
            if stmt.name in types:
                return f"function name '{stmt.name}' already declared"
            types[stmt.name] = stmt
        else:
            infer_type = infer(stmt, types)
            if isinstance(infer_type, str):
                return infer_type


def infer(expr: Expression, types: TypeState) -> Type | str:
    if isinstance(expr, IntLiteral):
        return Int
    elif isinstance(expr, RealLiteral):
        return Real
    elif isinstance(expr, TextLiteral):
        return Text
    elif isinstance(expr, (Add, Sub, Mul, Div,)):
        return binary_nr_func(expr, types)
    elif isinstance(expr, FuncCall):
        if expr.name not in types:
            return f"cannot call function '{expr.name}' because it is not known"
        func = types[expr.name]
        return func.returns
    assert_never(expr)


def binary_nr_func(expr, types: TypeState):
    left_type = infer(expr.left, types)
    right_type = infer(expr.right, types)
    if left_type == right_type == Int:
        return Int
    elif left_type == right_type == Real:
        return Real
    else:
        return f'no variant of {type(expr).__name__} for arguments ({left_type}, {right_type})'


