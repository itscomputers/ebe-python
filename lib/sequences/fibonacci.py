#   lib/sequences/fibonacci.py
#   - module for fibonacci sequences w/ optional modulus

# ===========================================================
from .lucas import LucasSequence

# ===========================================================
__all__ = [
    "FibonacciSequence",
]
# ===========================================================


class FibonacciSequence:
    @classmethod
    def at_index(cls, index: int, modulus: int | None = None) -> "FibonacciSequence":
        lucas_seq = LucasSequence.at_index(index, p=1, q=-1, modulus=modulus)
        seq = cls(modulus=modulus)
        seq._idx = index
        seq._prev = lucas_seq._prev.u
        seq._value = lucas_seq._value.u
        return seq

    def __init__(self, *, modulus: int | None = None):
        self._modulus = modulus
        self._idx = 0
        self._prev = 1
        self._value = 0

    def __repr__(self) -> str:
        return f"FibonacciSequence(index={self._idx}, value={self._value})"

    def __next__(self) -> "FibonacciSequence":
        self._prev, self._value = self._value, self.next_value()
        self._idx += 1
        return self

    @property
    def value(self) -> int:
        return self._value

    @property
    def index(self) -> int:
        return self._idx

    def next_value(self) -> int:
        return self._reduce(self._prev + self._value)

    def _reduce(self, value: int) -> int:
        if self._modulus is not None:
            return value % self._modulus
        return value
