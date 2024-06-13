#   lib/sequences/lucas.py
#   - module for lucas sequences w/ optional modulus

# ===========================================================
from dataclasses import dataclass

# ===========================================================
__all__ = [
    "LucasValue",
    "LucasSequence",
]
# ===========================================================


@dataclass
class LucasValue:
    """
    Values at a stage of a Lucas sequence.

    + index: int --the stage of the sequence
    + u: int --the value of the sequence U[index]
    + v: int --the value of the sequence V[index]
    + q: int --the value of the sequence Q[index]
    """

    index: int
    u: int
    v: int
    q: int


# ============================


class LucasSequence:
    """
    Lucas sequence with optional modulus.

    Has two parameters `p` and `q` and tracks three sequences U[k], V[k], Q[k].
    The sequences are as follows:
        U[0] = 0
        U[1] = 1
        U[k+1] = p * U[k] - q * U[k-1]

        V[0] = 2
        V[1] = p
        V[k+1] = p * V[k] - q * V[k-1]

        Q[0] = 1
        Q[k+1] = q * Q[k] == q**(k+1)

    example:
        ```
        p = 1
        q = -1
        # U[k] is the Fibonacci numbers
        # V[k] is the Lucas numbers

        seq = LucasSequence(p=p, q=q)
        seq.value
            ~> LucasValue(index=0, u=0, v=2, q=1)
        next(seq).value
            ~> LucasValue(index=1, u=1, v=1, q=-1)
        next(seq).value
            ~> LucasValue(index=2, u=1, v=3, q=1)
        next(seq).value
            ~> LucasValue(index=3, u=2, v=4, q=-1)
        next(seq).value
            ~> LucasValue(index=4, u=3, v=7, q=1)
        next(seq).value
            ~> LucasValue(index=5, u=5, v=11, q=-1)
        next(seq).value
            ~> LucasValue(index=6, u=8, v=18, q=1)
        ```

    + p: int
    + q: int
    + modulus: int | None
    """

    def __init__(self, *, p: int, q: int, modulus: int | None = None):
        self._modulus = modulus
        self.p = p
        self.q = q
        self._disc = self.p**2 - 4 * self.q
        self._value = self._zero()
        self._prev = self._zero()

    # ========================

    @classmethod
    def at_index(
        cls,
        index: int,
        *,
        p: int,
        q: int,
        modulus: int | None = None,
    ) -> "LucasSequence":
        """
        Initialize a Lucas sequence at an index.

        example:
            `LucasSequence.at_index(10, p=1, q=-1).value
                ~> LucasValue(index=10, u=55, v=123, q=1)`

        + index: int
        + p: int
        + q: int
        + modulus: int | None
        ~> LucasSequence --at given index
        """

        seq = cls(p=p, q=q, modulus=modulus)
        if index == 0:
            return seq
        if index % 2 == 1:
            return next(cls.at_index(index - 1, p=p, q=q, modulus=modulus))
        return cls.at_index(index // 2, p=p, q=q, modulus=modulus).double_index()

    # ========================

    def __repr__(self) -> str:
        return f"LucasSequence(value={self._value})"

    # ------------------------

    def __next__(self) -> "LucasSequence":
        """Advance sequence to the next stage."""

        self._prev, self._value = self._value, self.next_value()
        return self

    # ------------------------

    @property
    def value(self) -> LucasValue:
        """Value of the sequence at the current stage."""

        return self._value

    # ------------------------

    @property
    def index(self) -> int:
        """Index of the current stage."""

        return self._value.index

    # ========================

    def next_value(self) -> LucasValue:
        """Value of the sequence at the next stage."""

        if self._value.index == 0:
            return self._one()
        return LucasValue(
            index=self._value.index + 1,
            u=self._reduce(self.p * self._value.u - self.q * self._prev.u),
            v=self._reduce(self.p * self._value.v - self.q * self._prev.v),
            q=self._reduce(self.q * self._value.q),
        )

    # ========================

    def double_index(self) -> "LucasSequence":
        """Advance the sequence to stage where index is double the current index."""

        self._prev = LucasValue(
            index=2 * self._value.index - 1,
            u=self._reduce(self._value.u * self._prev.v - self._prev.q),
            v=self._reduce(self._value.v * self._prev.v - self._prev.q * self.p),
            q=self._reduce(self.q * self._prev.q**2),
        )
        self._value = LucasValue(
            index=2 * self._value.index,
            u=self._reduce(self._value.u * self._value.v),
            v=self._reduce(self._value.v**2 - 2 * self._value.q),
            q=self._reduce(self._value.q**2),
        )
        return self

    # ========================

    def _reduce(self, value: int) -> int:
        """Reduce a value by the given modulus, if present."""

        if self._modulus is not None:
            return value % self._modulus
        return value

    # ------------------------

    def _zero(self) -> LucasValue:
        """0th value of the sequence."""

        return LucasValue(index=0, u=0, v=2, q=1)

    # ------------------------

    def _one(self) -> LucasValue:
        """1st value of the sequence."""

        return LucasValue(index=1, u=1, v=self._reduce(self.p), q=self._reduce(self.q))
