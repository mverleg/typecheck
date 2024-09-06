from __future__ import annotations

from dataclasses import dataclass
from typing import List

from mypyc.ir.func_ir import FuncDecl

from typecheck.typ import Type


@dataclass
class IntLiteral:
    value: int


@dataclass
class RealLiteral:
    value: float


@dataclass
class TextLiteral:
    value: str


@dataclass
class Add:
    left: Expression
    right: Expression


@dataclass
class Sub:
    left: Expression
    right: Expression


@dataclass
class Mul:
    left: Expression
    right: Expression


@dataclass
class Div:
    left: Expression
    right: Expression


@dataclass
class FuncDecl:
    name: str
    params: List[Type]
    returns: List[Type]


@dataclass
class FuncCall:
    args: List[Expression]
    result: List[Expression]


Literal = IntLiteral | RealLiteral | TextLiteral
#TODO: change to NumberLiteral and infer the type of number, or make Int assignable to Real

Expression = Add | Sub | Mul | Div | Literal

Statement = FuncDecl | Expression
# todo perhaps FuncDecl will be an expression too later

