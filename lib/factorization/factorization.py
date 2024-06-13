#   lib/factorization/factorization.py
#   - module for factoring a number

# ===========================================================
from collections import Counter
from functools import reduce
from typing import Generator, Sequence

from ..basic import integer_sqrt, iter_primes_up_to, lcm, padic
from ..config import default
from ..primality import is_prime
from ..types import GaussianInteger, QuaternionInteger
from ..utils import combine_counters
from .algorithms import Algorithm
from .divisor_search import find_divisors
from .gaussian_divisor import _get_gaussian_divisor
from .quaternion_divisor import _get_quaternion_divisor

# ===========================================================
__all__ = [
    "Factorization",
]
# ===========================================================


class Factorization:
    """
    Factorization class.

    example:
        ```
        factorization = Factorization(550)
        dict(factorization)
            ~> {2: 1, 5: 2, 11: 1}
        factorization.factors
            ~> [2, 5, 5, 11]
        factorization.primes
            ~> {2, 5, 11}
        factorization.divisors
            ~> [1, 2, 5, 10, 11, 22, 25, 50, 55, 110, 275, 550]
        factorization.two_squares
            ~> None
        factorization.four_squares
            ~> (20, 10, 5, 5)
        factorization.euler_phi
            ~> 200
        factorization.carmichael_lambda
            ~> 20
        ```

    + number: int
    """

    # ========================
    # initialization
    # ========================

    def __init__(
        self,
        number: int,
        prime_base: Sequence[int] | None = None,
        algorithms: Sequence[Algorithm] | None = None,
    ):
        self._number = number
        self._prime_base = prime_base
        self._algorithms = algorithms
        self._factorization: dict[int, int] | None = None
        self._factors: list[int] | None = None
        self._primes: set[int] | None = None
        self._divisors: list[int] | None = None
        self._square_free_part: "Factorization" | None = None
        self._square_part: "Factorization" | None = None
        self._two_squares: tuple[int, int] | None = None
        self._four_squares: tuple[int, int, int, int] | None = None
        self._euler_phi: int | None = None
        self._carmichael_lambda: int | None = None

    # ------------------------

    @classmethod
    def from_dict(cls, factors: dict[int, int]) -> "Factorization":
        """Build factorization from dictionary of factors with multiplicity."""

        number = reduce(
            lambda acc, factor: acc * factor,
            Counter(factors).elements(),
            1,
        )
        factorization: dict[int, int] = reduce(
            lambda acc, pair: combine_counters(
                acc,
                _factor_with_divisor_search(pair[0], algorithms=None),
                1,
                pair[1],
            ),
            factors.items(),
            dict(),
        )
        instance = cls(number)
        instance._factorization = factorization
        return instance

    # ------------------------

    @classmethod
    def from_list(cls, factors: Sequence[int]) -> "Factorization":
        """Build factorization from list of factors."""

        factorization = dict(Counter(factors))
        return cls.from_dict(factorization)

    # ========================
    # casting
    # ========================

    def __iter__(self) -> Generator[tuple[int, int], None, None]:
        """Enable iteration over prime factors with multiplicity."""

        for prime, exp in self.factorization.items():
            yield prime, exp

    # ------------------------

    def __list__(self) -> list[int]:
        """Convert to list of prime factors."""

        return self.factors

    # ========================

    def __repr__(self) -> str:
        return f"Factorization(number={self.number}, factorization={self.factorization})"

    # ========================
    # properties
    # ========================

    @property
    def number(self) -> int:
        return self._number

    # ------------------------

    @property
    def factorization(self) -> dict[int, int]:
        """Prime divisors dictionary with multiplicity."""

        if self._factorization is None:
            self._factorization = _factor(
                self._number,
                self._prime_base,
                self._algorithms,
            )
        return self._factorization

    # ------------------------

    @property
    def factors(self) -> list[int]:
        """Sorted list of prime divisors with multiplicity of `self.number`."""

        if self._factors is None:
            self._factors = [
                prime
                for prime, exp in sorted(self.factorization.items())
                for _ in range(exp)
            ]
        return self._factors

    # ------------------------

    @property
    def primes(self) -> set[int]:
        """Set of prime divisors of `self.number`."""

        if self._primes is None:
            self._primes = set(self.factorization.keys())
        return self._primes

    # ------------------------

    @property
    def divisors(self) -> list[int]:
        """Sorted list of divisors of `self.number`."""

        if self._divisors is None:
            divisors = {1}
            for prime in Counter(self.factorization).elements():
                divisors = divisors | set(prime * divisor for divisor in divisors)
            self._divisors = sorted(divisors)
        return self._divisors

    # ------------------------

    @property
    def square_part(self) -> "Factorization":
        """Square part of the factorization."""

        if self._square_part is None:
            self._square_part = Factorization.from_dict(
                {
                    prime: exp - exp % 2
                    for prime, exp in self.factorization.items()
                    if exp > 1
                },
            )
        return self._square_part

    # ------------------------

    @property
    def square_free_part(self) -> "Factorization":
        """Square-free part of the factorization."""

        if self._square_free_part is None:
            self._square_free_part = Factorization.from_dict(
                {prime: 1 for prime, exp in self.factorization.items() if exp % 2 == 1},
            )
        return self._square_free_part

    # ------------------------

    def is_sum_of_two_squares(self) -> bool:
        """Determine whether `self.number` can be expressed as the sum of two squares."""

        return not any(prime % 4 == 3 for prime in self.square_free_part.primes)

    # ------------------------

    @property
    def two_squares(self) -> tuple[int, int] | None:
        """Find two integers whose squares sum to `self.number`, if possible."""

        if self._two_squares is None:
            if not self.is_sum_of_two_squares():
                return None

            gaussian = reduce(
                lambda acc, divisor: acc * divisor,
                map(_get_gaussian_divisor, self.square_free_part.primes),
                GaussianInteger(1, 0),
            )
            gaussian *= _get_sqrt(self.square_part).number

            self._two_squares = tuple(sorted(map(abs, gaussian.components), reverse=True))

        return self._two_squares

    # ------------------------

    @property
    def four_squares(self) -> tuple[int, int, int, int]:
        """Find four integers whose squares sum to `self.number`."""

        if self._four_squares is None:
            quaternion: QuaternionInteger = reduce(
                lambda acc, divisor: acc * divisor,
                map(_get_quaternion_divisor, self.square_free_part.primes),
                QuaternionInteger(1, 0, 0, 0),
            )
            quaternion *= _get_sqrt(self.square_part).number

            self._four_squares = tuple(
                sorted(map(abs, quaternion.components), reverse=True),
            )

        return self._four_squares

    # ------------------------

    @property
    def euler_phi(self) -> int:
        """Euler's phi function."""

        if self._euler_phi is None:
            self._euler_phi = reduce(
                lambda acc, number: acc * number,
                map(_phi, self.factorization.items()),
                1,
            )
        return self._euler_phi

    # ------------------------

    @property
    def carmichael_lambda(self) -> int:
        """Carmichael's lambda function."""

        if self._carmichael_lambda is None:
            self._carmichael_lambda = lcm(*map(_lambda, self.factorization.items()))
        return self._carmichael_lambda


# =============================


def _factor(
    number: int,
    prime_base: Sequence[int] | None,
    algorithms: Sequence[Algorithm] | None,
) -> dict[int, int]:
    """
    Factor `number` into primes using prime base and division search.

    example:
        `_factor(1200) ~> {2: 4, 3: 1, 5: 2}`

    + number: int
    + prime_base: Sequence[int] | None
    + algorithms: Sequence[Algorithm] | None
    ~> dict[int, int] --keys are primes, values are exponents
    """

    number, factorization = _factor_out_prime_base(number, prime_base)
    return {
        **factorization,
        **_factor_with_divisor_search(number, algorithms),
    }


# -----------------------------


def _factor_with_divisor_search(
    number: int,
    algorithms: Sequence[Algorithm] | None,
) -> dict[int, int]:
    """
    Factor `number` into primes using divisor search.

    example:
        `_factor_with_divisor_search(1200) ~> {2: 4, 3: 1, 5: 2}`

    + number: int
    + algorithms: Sequence[Algorithm] | None
    ~> dict[int, int] --keys are prime number, values are exponents
    """

    if number == 1:
        return dict()

    if is_prime(number):
        return {number: 1}

    sqrt = integer_sqrt(number)
    if sqrt**2 == number:
        return combine_counters(
            dict(),
            _factor_with_divisor_search(sqrt, algorithms),
            1,
            2,
        )

    remaining = number
    factorization: dict[int, int] = dict()

    divisors = find_divisors(remaining, algorithms)
    for divisor in divisors:
        exp, remaining = padic(remaining, divisor)
        factorization = combine_counters(
            factorization,
            _factor_with_divisor_search(divisor, algorithms),
            1,
            exp,
        )

    return combine_counters(
        factorization,
        _factor_with_divisor_search(remaining, algorithms),
    )


# -----------------------------


def _factor_out_prime_base(
    number: int,
    prime_base: Sequence[int] | None = None,
) -> tuple[int, dict[int, int]]:
    """
    Factor out `prime_base` primes from `number` using trial division.

    example:
        `_factor_out_prime_base(1200, [2, 3, 7]) ~> (25, {2: 4, 3: 1})`

    + number: int
    + prime_base: Sequence[int] | None
    ~> (remaining, factorization): tuple[int, dict[int, int]]
    """
    factorization = dict()
    for prime in prime_base or iter_primes_up_to(default("prime_base_max")):
        exp, number = padic(number, prime)
        if exp > 0:
            factorization[prime] = exp

    return number, factorization


# =============================


def _phi(prime_with_multiplicity: tuple[int, int]) -> int:
    """
    Euler's phi function for a power of a prime.

    + (prime, exp): tuple[int, int]
    ~> int
    """

    prime, exp = prime_with_multiplicity
    return prime ** (exp - 1) * (prime - 1)


# -----------------------------


def _lambda(prime_with_multiplicity: tuple[int, int]) -> int:
    """
    Carmichael's lambda function for a power of a prime.

    + (prime, exp): tuple[int, int]
    ~> int
    """

    phi = _phi(prime_with_multiplicity)
    prime, exp = prime_with_multiplicity
    if prime == 2 and exp > 2:
        return phi // 2
    return phi


# =============================


def _get_sqrt(factorization: Factorization) -> Factorization:
    return Factorization.from_dict(
        {prime: exp // 2 for prime, exp in factorization},
    )
