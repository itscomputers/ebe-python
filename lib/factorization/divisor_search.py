#   lib/factorization/divisor_search.py
#   - module for searching for a divisor using sequence of algorithms

# ===========================================================
from typing import Generator, Sequence

from ..config import default
from .algorithms import Algorithm

# ===========================================================
__all__ = [
    "find_divisors",
    "DivisorSearch",
]
# ===========================================================


def find_divisors(
    number: int,
    algorithms: Sequence[Algorithm] | None = None,
) -> set[int]:
    """
    Find a set of divisors of `number` using given algorithms.

    + number: int --composite
    + algorithms: Sequence[Algorithm] | None
        default None falls back to _default_algorithms()
    ~> set[int] --first divisors found using given algorithms
    """

    if algorithms is None:
        algorithms = _default_algorithms()

    return {
        divisor
        for divisor in DivisorSearch(number, algorithms).search().divisors
        if 1 < divisor < number
    }


# -----------------------------


class DivisorSearch:
    """
    Search for divisors of `number` using given algorithms.

    At each step, the next potential divisor from an algorithm is inspected; if equal to
    `number`, the algorithm is essentially discarded; if greater than 1, at least one
    non-trivial divisor has been found.

    + number: int --composite
    + algorithms: Sequence[Algorithm]
    """

    def __init__(self, number: int, algorithms: Sequence[Algorithm]):
        self.number = number
        self.algorithms = algorithms
        self._generators = [algorithm.generator(number) for algorithm in algorithms]
        self.divisors = [1 for algorithm in algorithms]
        self._divisor_found = False

    def search(self) -> "DivisorSearch":
        """Perform search for non-trivial divisors."""

        while not self._divisor_found:
            for idx, gen in enumerate(self._generators):
                divisor = next(gen)
                self.divisors[idx] = divisor
                if divisor == self.number:
                    self._generators[idx] = self._trivial_generator()
                elif divisor > 1:
                    self._divisor_found = True
        return self

    def _trivial_generator(self) -> Generator[int, None, None]:
        """Trivial generator to replace generator from a failed algorithm."""

        while True:
            yield self.number


# =============================


def _default_algorithms() -> list[Algorithm]:
    """Get list of default algorithms."""

    return [
        *[
            Algorithm.build("rho", seed=seed, func=lambda x: x**2 + 1)
            for seed in default("rho_seeds")
        ],
        *[Algorithm.build("p-1", seed=seed) for seed in default("minus_seeds")],
    ]
