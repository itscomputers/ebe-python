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
    """
    Fibonacci sequence with optional modulus.

    The sequence is defined as follows:
        F[0] = 0
        F[1] = 1
        F[k+1] = F[k] + F[k-1]

    example:
        ```
        seq = FibonacciSequence()
        seq.value
            ~> 0
        next(seq).value
            ~> 1
        next(seq).value
            ~> 1
        next(seq).value
            ~> 2
        next(seq).value
            ~> 3
        next(seq).value
            ~> 5
        next(seq).value
            ~> 8
        ```

    + modulus: int | None
    """

    def __init__(self, *, modulus: int | None = None):
        self._modulus = modulus
        self._idx = 0
        self._prev = 1
        self._value = 0

    # ========================

    @classmethod
    def at_index(cls, index: int, modulus: int | None = None) -> "FibonacciSequence":
        """
        Initialize the Fibonacci sequence at an index.

        example:
            `FibonacciSequence.at_index(10).value ~> 55`

        + index: int
        + modulus: int | None
        ~> FibonacciSequence --at given index
        """

        lucas_seq = LucasSequence.at_index(index, p=1, q=-1, modulus=modulus)
        seq = cls(modulus=modulus)
        seq._idx = index
        seq._prev = lucas_seq._prev.u
        seq._value = lucas_seq._value.u
        return seq

    # ========================

    def __repr__(self) -> str:
        return f"FibonacciSequence(index={self._idx}, value={self._value})"

    # ------------------------

    def __next__(self) -> "FibonacciSequence":
        """Advance sequence to the next stage."""

        self._prev, self._value = self._value, self.next_value()
        self._idx += 1
        return self

    # ------------------------

    @property
    def value(self) -> int:
        """Value of the sequence at the current stage."""

        return self._value

    # ------------------------

    @property
    def index(self) -> int:
        """Index of the current stage."""

        return self._idx

    # ------------------------

    def next_value(self) -> int:
        """Value of the sequence at the next stage."""

        return self._reduce(self._prev + self._value)

    # ========================

    def _reduce(self, value: int) -> int:
        """Reduce a value by the given modulus, if present."""

        if self._modulus is not None:
            return value % self._modulus
        return value
