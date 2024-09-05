
import typing
from dataclasses import dataclass


@dataclass
class Scalar:
    kind: typing.Literal['int', 'real', 'text']


Int = Scalar('int')
Real = Scalar('real')
Text = Scalar('text')

Type = typing.Union[Int, Real, Text]

