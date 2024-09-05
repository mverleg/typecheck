from dataclasses import dataclass

@dataclass
class Int:
    @classmethod
    def initialize(Cls):
        return 0

@dataclass
class Real:
    @classmethod
    def initialize(Cls):
        return 0.0

@dataclass
class Text:
    @classmethod
    def initialize(Cls):
        return None


Type = Int | Real | Text

