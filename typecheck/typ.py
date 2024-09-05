import typing
from enum import Enum


class Scalar(Enum):
    Int = 'int'
    Real = 'real'
    Text = 'text'


Int = Scalar.Int
Real = Scalar.Real
Text = Scalar.Text


Type = typing.Union[Scalar]

