from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class Student:
    id: int
    name: str

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class Assignment:
    id: int
    title: str
    weight: float = 1.0

    def to_dict(self) -> Dict:
        return asdict(self)
