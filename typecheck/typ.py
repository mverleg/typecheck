from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Union


class Scalar(Enum):
    Int = 'int'
    Real = 'real'
    Text = 'text'

    def __str__(self):
        return self.name


@dataclass
class Function(Enum):
    args: List[Type]
    result: List[Type]


Int = Scalar.Int
Real = Scalar.Real
Text = Scalar.Text


Type = Union[Scalar]

