from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List

from typecheck.typ import Type, Int, Real


@dataclass
class Assignment:
    name: str
    # typ=None means infer (it could be a reassignment)
    # if type is given then it must be declaration of a new var
    typ: Type | None
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
    Add = 'add'
    Sub = 'sub'
    Mul = 'mul'
    Div = 'div'


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
        return FuncCall(self.kind.value, [self.left, self.right])

    def as_func_decls(self) -> List[FuncDecl]:
        return [
            FuncDecl(self.kind.value, [Int, Int,], Int,),
            FuncDecl(self.kind.value, [Real, Real,], Real,),
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

