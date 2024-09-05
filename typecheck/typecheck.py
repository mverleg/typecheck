from typing_extensions import assert_never

from typecheck.syntree import Expression, IntLiteral, Add
from typecheck.typ import Type, Int


def check(expr: Expression) -> Type | str:
    if isinstance(expr, IntLiteral):
        return Int
    #TODO @mark: more
    assert_never(expr)


