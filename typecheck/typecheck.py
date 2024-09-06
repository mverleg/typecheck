from typing import List, Dict

from typing_extensions import assert_never

from typecheck.syntree import IntLiteral, Add, Sub, Mul, Div, RealLiteral, TextLiteral, Statement, FuncDecl, Expression, \
    FuncCall
from typecheck.typ import Type, Int, Real, Text, Null

TypeState = Dict[str, FuncDecl]


def check(prog: List[Statement]) -> Type | str:
    types: TypeState = {}
    last: Type = Null
    for stmt in prog:
        if isinstance(stmt, FuncDecl):
            if stmt.name in types:
                return f"function name '{stmt.name}' already declared"
            types[stmt.name] = stmt
        else:
            infer_type = infer(stmt, types)
            if isinstance(infer_type, str):
                return infer_type
            last = infer_type
    return last


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
            return f"cannot call function '{expr.name}' because no such function is known"
        func = types[expr.name]
        if len(expr.args) != len(func.params):
            return (f"cannot call function '{expr.name}' with "
                    f"{len(expr.args)} args because it expects {len(func.params)}")
        for nr, (arg, param) in enumerate(zip(expr.args, func.params)):
            arg_type = infer(arg, types)
            if not is_assignable(arg_type, param):
                return (f"cannot call function '{expr.name}' because argument {nr+1} "
                        f"is of type {arg_type}, while {param} is expected")
        return func.returns
    assert_never(expr)


def binary_nr_func(expr, types: TypeState):
    #TODO @mark: use functions for this
    left_type = infer(expr.left, types)
    right_type = infer(expr.right, types)
    if is_assignable(left_type, Int) and is_assignable(right_type, Int):
        return Int
    if is_assignable(left_type, Real) and is_assignable(right_type, Real):
        return Real
    else:
        return f'no variant of {type(expr).__name__} for arguments ({left_type}, {right_type})'


def is_assignable(value_type: Type, target_type: Type):
    return value_type == target_type


