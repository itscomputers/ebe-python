#   lib/lucas_sequence/modular.py
#   - module for lucas sequences relative to a modulus

# ===========================================================
from dataclasses import dataclass

# ===========================================================
__all__ = [
    "lucas_mod_gen",
    "lucas_mod_by_index",
    "lucas_mod_double_index",
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


def lucas_mod_gen(P, Q, modulus):
    """
    Generator for `(P, Q)`-Lucas sequence triple relative to `modulus`.

    Produces sequences U_k, V_k
        * both satifying `next = P * curr - Q * prev`
        * U_0, U_1 = 0, 1
        * V_0, V_1 = 2, P
    and sequence Q_k = Q**k % modulus.

    + P: int
    + Q: int
    + modulus: int --at least 2
    ~> Iterator[Tuple[int, int, int]]
    """
    prev = _term_zero(P, Q, modulus)
    curr = _term_one(P, Q, modulus)

    yield prev
    while True:
        yield curr
        prev, curr = curr, _next_term(prev, curr, P, Q, modulus)


# =============================


def lucas_mod_by_index(k, P, Q, modulus):
    """
    Compute `k`th term of `(P, Q)`-Lucas sequence triple relative to `modulus`
    without computing all preceding terms.

    + k: int
    + P: int
    + Q: int
    + modulus: int
    ~> (U_k, V_k, Q_k): Tuple[int, int, int]
    """
    if k == 0:
        return _term_zero(P, Q, modulus)
    elif k == 1:
        return _term_one(P, Q, modulus)
    elif k % 2 == 0:
        return lucas_mod_double_index(*lucas_mod_by_index(k // 2, P, Q, modulus), modulus)
    return lucas_mod_index_plus_one(
        *lucas_mod_by_index(k - 1, P, Q, modulus), P, Q, modulus
    )


# -----------------------------


def lucas_mod_double_index(U_k, V_k, Q_k, modulus):
    """
    Compute `2k`th term of Lucas sequence triple from `k`th term.

    + U_k: int
    + V_k: int
    + Q_k: int
    + modulus: int
    ~> (U_2k, V_2k, Q_2k): Tuple[int, int, int]
    """
    U = (U_k * V_k) % modulus
    V = (V_k * V_k - 2 * Q_k) % modulus

    return U, V, pow(Q_k, 2, modulus)


# -----------------------------


def lucas_mod_index_plus_one(U_k, V_k, Q_k, P, Q, modulus):
    """
    Compute `k+1`th term of Lucas sequence triple from `k`th term.

    + U_k: int
    + V_k: int
    + Q_k: int
    + P: int
    + Q: int
    + modulus: int
    ~> (U_k1, V_k1, Q_k1): Tuple[int, int, int]
    """
    U = ((P * U_k + V_k) * (modulus + 1) // 2) % modulus
    V = (((P**2 - 4 * Q) * U_k + P * V_k) * (modulus + 1) // 2) % modulus

    return U, V, (Q_k * Q) % modulus


# ===========================================================


def _term_zero(P, Q, modulus):
    return (0, 2, 1)


def _term_one(P, Q, modulus):
    return (1, P % modulus, Q % modulus)


def _next_term(prev, curr, P, Q, modulus):
    U, V = map(lambda x, y: (P * x - Q * y) % modulus, curr[:2], prev[:2])
    return (U, V, (Q * curr[2]) % modulus)
