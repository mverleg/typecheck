
from typecheck.syntree import Expression, IntLiteral
from typecheck.typ import Type, Int


def check(expr: Expression) -> Type | str:
    if isinstance(expr, IntLiteral):
        return Int()


Literal = IntLiteral | RealLiteral | TextLiteral
#TODO: change to NumberLiteral and infer the type of number

Expression = Add | Sub | Mul | Div | Literal


