from dataclasses import dataclass

@dataclass
class Int:
    default = 0

@dataclass
class Real:
    default = 0.0

@dataclass
class Text:
    default = None


Type = Int | Real | Text

