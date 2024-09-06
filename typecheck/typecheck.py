from typing import List

from typing_extensions import assert_never

from typecheck.syntree import IntLiteral, Add, Sub, Mul, Div, RealLiteral, TextLiteral, Statement, FuncDecl
from typecheck.typ import Type, Int, Real, Text


def check(prog: List[Statement]) -> Type | str:
    for stmt in prog:
        if isinstance(stmt, FuncDecl):
            return 'error'
        if isinstance(stmt, IntLiteral):
            return Int
        elif isinstance(stmt, RealLiteral):
            return Real
        elif isinstance(stmt, TextLiteral):
            return Text
        elif isinstance(stmt, (Add, Sub, Mul, Div,)):
            return binary_nr_func(stmt)
        #TODO @mark: more
        assert_never(stmt)


def binary_nr_func(expr):
    left_type = check(expr.left)
    right_type = check(expr.right)
    if left_type == right_type == Int:
        return Int
    elif left_type == right_type == Real:
        return Real
    else:
        return f'no variant of {type(expr).__name__} for arguments ({left_type}, {right_type})'


