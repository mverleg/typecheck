from typing_extensions import assert_never

from typecheck.syntree import Expression, IntLiteral, Add, RealLiteral, TextLiteral
from typecheck.typ import Type, Int, Real, Text


def check(expr: Expression) -> Type | str:
    if isinstance(expr, IntLiteral):
        return Int
    elif isinstance(expr, RealLiteral):
        return Real
    elif isinstance(expr, TextLiteral):
        return Text
    elif isinstance(expr, Add):
        left_type = check(expr.left)
        right_type = check(expr.right)
        if left_type == right_type == Int:
            return Int
        elif left_type == right_type == Real:
            return Real
        else:
            return f'no variant of Add for arguments ({left_type}, {right_type})'
    #TODO @mark: more
    assert_never(expr)


