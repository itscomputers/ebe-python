#   lib/factorization/algorithms.py
#   - module for factor-finding algorithms for composite numbers

# ===========================================================
from typing import Callable, Generator, Literal

from ..basic import gcd
from ..types import GaussianInteger

# ===========================================================
__all__ = [
    "Algorithm",
    "PollardRho",
    "PollardPMinusOne",
    "WilliamsPPlusOne",
]
# ===========================================================


class Algorithm:
    """Abstract base class for division algorithms."""

    @classmethod
    def build(cls, algorithm: Literal["rho", "p-1", "p+1"], **kwargs) -> "Algorithm":
        """Builder shortcut for an algorithm."""

        if algorithm == "p-1":
            return PollardPMinusOne(**kwargs)
        if algorithm == "p+1":
            return WilliamsPPlusOne(**kwargs)
        return PollardRho(**kwargs)

    def generator(self, number: int) -> Generator[int, None, None]:
        """Generator for potential divisors."""

        return NotImplemented

    def find_divisor(self, number: int) -> int:
        """
        Finds a divisor of `number`.

        + number: int --composite
        ~> int --either nontrivial divisor or number itself
        """

        gen = self.generator(number)
        divisor = next(gen)
        while divisor == 1:
            divisor = next(gen)
        return divisor


# -----------------------------


class PollardRho(Algorithm):
    """
    Pollard's rho algorithm to find divisor of an integer.

    example:
        `PollardRho(seed=2, func=lambda x: x**2 + 1).find_divisor(143) ~> 11`

    + seed: int
    + func: Callable[[int], int]
    """

    def __init__(self, seed: int = 2, func: Callable[[int], int] = lambda x: x**2 + 1):
        self.seed = seed
        self.func = func

    def generator(self, number: int) -> Generator[int, None, None]:
        """Generator for potential divisors."""

        x_i = self.func(self.seed % number)
        x_2i = self.func(x_i) % number

        while True:
            yield gcd(x_2i - x_i, number)
            x_i = self.func(x_i) % number
            x_2i = self.func(self.func(x_2i) % number) % number


# -----------------------------


class PollardPMinusOne(Algorithm):
    """
    Pollard's p-1 algorithm to find divisor of an integer.

    example:
        `PollardPMinusOne(seed=2).find_divisor(143) ~> 13`

    + seed: int
    """

    def __init__(self, seed: int = 2):
        self.seed = seed

    def generator(self, number: int) -> Generator[int, None, None]:
        """Generator for potential divisors."""

        yield gcd(self.seed, number)

        x_i = self.seed % number
        index = 1

        while True:
            yield gcd(x_i - 1, number)
            index = index + 1
            x_i = pow(x_i, index, number)


# -----------------------------


class WilliamsPPlusOne(Algorithm):
    """
    Williams' p+1 algorithm to find divisor of an integer.

    example:
        `WilliamsPPlusOne(seed=GaussianInteger(1, 2)).find_divisor(143) ~> 11`

    + seed: GaussianInteger
    """

    def __init__(self, seed: GaussianInteger = GaussianInteger(1, 2)):
        self.seed = seed

    def generator(self, number: int) -> Generator[int, None, None]:
        """Generator for potential divisors."""

        z = self.seed
        power = 1
        yield gcd(z.norm, number)

        while True:
            power = power + 1
            z = pow(z, power, number)
            yield gcd(z.imag, number)
