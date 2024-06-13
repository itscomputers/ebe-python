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
    index: int
    u: int
    v: int
    q: int

    def terms(self) -> tuple[int, int]:
        return self.u, self.v


class LucasSequence:
    @classmethod
    def at_index(
        cls,
        index: int,
        *,
        p: int,
        q: int,
        modulus: int | None = None,
    ) -> "LucasSequence":
        seq = cls(p=p, q=q, modulus=modulus)
        if index == 0:
            return seq
        if index % 2 == 1:
            return next(cls.at_index(index - 1, p=p, q=q, modulus=modulus))
        return cls.at_index(index // 2, p=p, q=q, modulus=modulus).double_index()

    def __init__(self, *, p: int, q: int, modulus: int | None = None):
        self._modulus = modulus
        self.p = p
        self.q = q
        self._disc = self.p**2 - 4 * self.q
        self._value = self._zero()
        self._prev = self._zero()

    def __repr__(self) -> str:
        return f"LucasSequence(value={self._value})"

    def __next__(self) -> "LucasSequence":
        self._prev, self._value = self._value, self.next_value()
        return self

    def _reduce(self, value: int) -> int:
        if self._modulus is not None:
            return value % self._modulus
        return value

    def _half(self, value: int) -> int:
        if self._modulus is not None:
            return (((self._modulus + 1) * value) // 2) % self._modulus
        return value // 2

    @property
    def value(self) -> LucasValue:
        return self._value

    @property
    def index(self) -> int:
        return self._value.index

    def next_value(self) -> LucasValue:
        if self._value.index == 0:
            return self._one()
        return LucasValue(
            index=self._value.index + 1,
            u=self._reduce(self.p * self._value.u - self.q * self._prev.u),
            v=self._reduce(self.p * self._value.v - self.q * self._prev.v),
            q=self._reduce(self.q * self._value.q),
        )

    def double_index(self) -> "LucasSequence":
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

    def _zero(self) -> LucasValue:
        return LucasValue(index=0, u=0, v=2, q=1)

    def _one(self) -> LucasValue:
        return LucasValue(index=1, u=1, v=self._reduce(self.p), q=self._reduce(self.q))
