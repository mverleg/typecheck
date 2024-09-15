from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Union


class Scalar(Enum):
    Null = 'null'   # todo maybe temporary
    Int = 'int'
    Real = 'real'
    Text = 'text'

    def type_name(self) -> str:
        return self.value


@dataclass
class Function:
    params: List[Type]
    result: Type

    def type_name(self) -> str:
        return "fun({}) -> {}".format(','.join(arg.type_name() for arg in self.params), self.result.type_name())


Null = Scalar.Null
Int = Scalar.Int
Real = Scalar.Real
Text = Scalar.Text


Type = Scalar | Function

