from __future__ import annotations

from dataclasses import dataclass


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


Literal = IntLiteral | RealLiteral | TextLiteral
#TODO: change to NumberLiteral and infer the type of number, or make Int assignable to Real

Expression = Add | Sub | Mul | Div | Literal

