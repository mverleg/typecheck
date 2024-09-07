from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List

from typecheck.typ import Type, Int, Real


@dataclass
class Assignment:
    name: str
    value: Expression


@dataclass
class ReadVar:
    name: str


@dataclass
class IntLiteral:
    value: int


@dataclass
class RealLiteral:
    value: float


@dataclass
class TextLiteral:
    value: str


class BinaryMathKind(Enum):
    Add = 'Add'
    Sub = 'Sub'
    Mul = 'Mul'
    Div = 'Div'


@dataclass
class BinaryMathOp:
    kind: BinaryMathKind
    left: Expression
    right: Expression

    @classmethod
    def add(cls, left: Expression, right: Expression) -> BinaryMathOp:
        return BinaryMathOp(BinaryMathKind.Add, left, right)

    @classmethod
    def sub(cls, left: Expression, right: Expression) -> BinaryMathOp:
        return BinaryMathOp(BinaryMathKind.Sub, left, right)

    @classmethod
    def mul(cls, left: Expression, right: Expression) -> BinaryMathOp:
        return BinaryMathOp(BinaryMathKind.Mul, left, right)

    @classmethod
    def div(cls, left: Expression, right: Expression) -> BinaryMathOp:
        return BinaryMathOp(BinaryMathKind.Div, left, right)

    def as_func_call(self) -> FuncCall:
        return FuncCall(self.__class__.__name__, [self.left, self.right])

    @classmethod
    def as_func_decls(cls) -> List[FuncDecl]:
        return [
            FuncDecl(cls.__name__, [Int, Int,], Int,),
            FuncDecl(cls.__name__, [Real, Real,], Real,),
        ]


@dataclass
class FuncDecl:
    name: str
    params: List[Type]
    returns: Type


@dataclass
class FuncCall:
    name: str
    args: List[Expression]


Literal = IntLiteral | RealLiteral | TextLiteral
#TODO: change to NumberLiteral and infer the type of number, or make Int assignable to Real

Expression = BinaryMathOp | Literal | FuncCall | ReadVar

Statement = FuncDecl | Assignment | Expression
# todo perhaps FuncDecl will be an expression too later

