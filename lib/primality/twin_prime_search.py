#   lib/primality/twin_prime_search.py
#   - module for twin prime searching

# ===========================================================
from ..config import default
from .prime_search import PrimeSearch

# ===========================================================
__all__ = [
    "next_twin_prime",
    "prev_twin_prime",
    "TwinPrimeSearch",
]
# ===========================================================


def next_twin_prime(number: int) -> tuple[int, int]:
    """
    Get pair of twin primes (that differ by 2) after `number`.

    Not guaranteed to exist eventually, theoretically. This is a practically safe
    function, however, since the largest twin primes have 388,342 digits.

    + number: int
    ~> tuple[int, int]
    """

    twin_prime_search = TwinPrimeSearch(number - 2)
    if not twin_prime_search.has_value():
        twin_prime_search.next()
    return twin_prime_search.value


# ----------------------------


def prev_twin_prime(number: int) -> tuple[int, int] | None:
    """
    Get pair of twin primes (that differ by 2) before `number`, if any.

    + number: int
    ~> tuple[int, int] | None
    """

    twin_prime_search = TwinPrimeSearch(number - 1)
    if not twin_prime_search.has_value():
        twin_prime_search.next()
    if twin_prime_search.prev().has_value():
        return twin_prime_search.value
    return None


# ============================


class TwinPrimeSearch:
    """
    Class for searching both forwards and backwards for twin primes.

    example:
        ```
        twin_prime_search = TwinPrimeSearch(50)
        twin_prime_search.next().value
            ~> (59, 61)
        twin_prime_search.next().value
            ~> (71, 73)
        twin_prime_search.next().value
            ~> (101, 103)
        twin_prime_search.prev().value
            ~> (71, 73)
        twin_prime_search.prev().value
            ~> (59, 61)
        twin_prime_search.prev().value
            ~> (41, 43)
        ```

    + number: int
    + sieve_primes: list[int] | None --reduces the number of potential primes in a window
    """

    def __init__(self, number: int, sieve_primes: list[int] | None = None):
        self._number = number
        self._sieve_primes = sieve_primes or default("sieve_primes")
        self._prime_search = PrimeSearch(number, sieve_primes)
        self._prev: int | None = self._prime_search.next().value
        self._curr = self._prime_search.next().value

    # ------------------------

    def __repr__(self) -> str:
        if self.has_value():
            return f"TwinPrimeSearch(value={self.value})"
        return "TwinPrimeSearch(value=None)"

    # ------------------------

    @property
    def value(self) -> tuple[int, int]:
        """Get the current twin prime pair."""

        if self.has_value():
            assert self._prev is not None
            return (self._prev, self._curr)

        raise AttributeError("Value unavailable; try calling `.next()` or `.prev()`")

    # ------------------------

    def has_value(self) -> bool:
        return self._is_twin_prime()

    # ------------------------

    def next(self) -> "TwinPrimeSearch":
        """Move to next twin prime pair."""

        self._forward()
        while not self._is_twin_prime():
            self._forward()
        return self

    # ------------------------

    def prev(self) -> "TwinPrimeSearch":
        """Move to previous twin prime pair."""

        self._back()
        while not self._is_twin_prime() and self._prev is not None:
            self._back()
        return self

    # ========================

    def _is_twin_prime(self) -> bool:
        """Determine if the current pair is a pair of twin primes."""

        if self._prev is None:
            return False
        return self._curr == self._prev + 2

    # ------------------------

    def _forward(self) -> "TwinPrimeSearch":
        """Move forward to the next potential pair of twin primes."""

        self._prev = self._curr
        self._curr = self._prime_search.next().value
        return self

    # ------------------------

    def _back(self) -> "TwinPrimeSearch":
        """Move back to the previous potential pair of twin primes."""

        if self._prev is None:
            return self
        self._curr = self._prev
        if self._prime_search.prev().has_value():
            self._prev = self._prime_search.value
        else:
            self._prev = None
        return self
