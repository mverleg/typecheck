
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


Literal = IntLiteral | RealLiteral | TextLiteral
#TODO: change to NumberLiteral and infer the type of number

Expression = Add | Literal
