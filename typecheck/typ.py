
from dataclasses import dataclass


@dataclass
class Int:
    @classmethod
    def initialize(cls):
        return 0

@dataclass
class Real:
    @classmethod
    def initialize(cls):
        return 0.0

@dataclass
class Text:
    @classmethod
    def initialize(cls):
        return None


Type = Int | Real | Text

