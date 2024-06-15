#   lib/primality/prime_search.py
#   - module for prime searching

# ===========================================================
from functools import reduce

from ..basic import prime_to
from ..config import default
from .algorithms import is_prime

# ===========================================================
__all__ = [
    "next_prime",
    "next_primes",
    "prev_prime",
    "prev_primes",
    "primes_in_range",
    "goldbach_partition",
    "PrimeSearch",
    "Window",
]
# ===========================================================


def next_prime(number: int) -> int:
    """
    Get prime after `number`.

    + number: int
    ~> int
    """

    return PrimeSearch(number).next().value


# ----------------------------


def next_primes(number: int, count: int) -> list[int]:
    """
    Get list of `count` primes after `number`.

    + number: int
    + count: int
    ~> list[int]
    """

    prime_search = PrimeSearch(number)
    return [prime_search.next().value for _ in range(count)]


# ----------------------------


def prev_prime(number: int) -> int | None:
    """
    Get prime before `number`, if any.

    + number: int
    ~> int | None
    """

    prime_search = PrimeSearch(number)
    if prime_search.prev().has_value():
        return prime_search.value
    return None


# ----------------------------


def prev_primes(number: int, count: int) -> list[int]:
    """
    Get list of `count` primes before `number`, if any.

    + number: int
    + count: int
    ~> list[int]
    """

    prime_search = PrimeSearch(number)
    primes = []
    for _ in range(count):
        if prime_search.prev().has_value():
            primes.append(prime_search.value)
        else:
            continue

    return primes


# ----------------------------


def primes_in_range(lower: int, upper: int) -> list[int]:
    """
    Get list of primes in `range(lower, upper)`.

    + lower: int
    + upper: int
    ~> list[int]
    """

    prime_search = PrimeSearch(lower - 1)
    primes = []
    while prime_search.next().value < upper:
        primes.append(prime_search.value)
    return primes


# ============================


def goldbach_partition(number: int) -> tuple[int, int] | tuple[int, int, int]:
    """
    Get Goldbach partition of 2 or 3 primes that sum to `number`.

    If `number` is even, the unproven conjecture is that it is the sum of two primes. This
    has been proven for `number < 4 * 10**18`, so this function is not guaranteed to
    terminate beyond that.

    If a `number` is odd, the weak Goldbach conjecture is that it is the sum of at most 3
    primes. The same bound applies to to this as well.

    + number: int
    ~> tuple[int, int] | tuple[int, int, int]
    """

    if number < 4:
        raise ValueError("Must be at least 4")

    if number % 2 == 1:
        if is_prime(number - 2):
            return (number - 2, 2)

        prime = prev_prime(number - 4)
        assert prime is not None
        p, q, r = sorted(
            [prime, *goldbach_partition(number - prime)],
            reverse=True,
        )
        return p, q, r

    prime_search = PrimeSearch(number // 2 - 1)
    prime = prime_search.next().value

    while not is_prime(number - prime):
        prime = prime_search.next().value

    p, q = sorted([number - prime, prime], reverse=True)
    return p, q


# ============================


class PrimeSearch:
    """
    Class for searching both forwards and backwards for primes.

    example:
        ```
        prime_search = PrimeSearch(50)
        prime_search.next().value
            ~> 53
        prime_search.next().value
            ~> 59
        prime_search.next().value
            ~> 61
        prime_search.prev().value
            ~> 59
        prime_search.prev().value
            ~> 53
        prime_search.prev().value
            ~> 47
        ```

    + number: int
    + sieve_primes: list[int] | None --reduces the number of potential primes in a window
    """

    def __init__(self, number: int, sieve_primes: list[int] | None = None):
        self._number = number
        self._sieve_primes = sieve_primes or default("sieve_primes")
        self._window = Window(self._number, self._sieve_primes)

    # ------------------------

    def __repr__(self) -> str:
        if self.has_value():
            return f"PrimeSearch(value={self.value})"
        return "PrimeSearch(value=None)"

    # ------------------------

    @property
    def value(self) -> int:
        """Get value of current prime."""

        if self._window.value is not None:
            return self._window.value

        raise AttributeError("No value available. Try calling `.next()` or `.prev()`")

    # ------------------------

    def has_value(self) -> bool:
        """Determine whether there is a current prime."""

        return self._window.value is not None

    # ------------------------

    def next(self) -> "PrimeSearch":
        """Move to the next prime."""

        while not is_prime(self._window.next().value):
            continue
        return self

    # ------------------------

    def prev(self) -> "PrimeSearch":
        """Move to the previous prime."""

        while self._window.prev().value is not None and not is_prime(self._window.value):
            continue
        return self


# ============================


class Window:
    """
    Sliding window of potential primes.

    For example, if `sieve_primes == [2, 3]`, then the size of the window is 6. The first
    block is a block of primes, namely `[2, 3, 5]`. Each subsequent block only contains
    numbers not divisible by 2 or 3, ie, numbers that are 1 or 5 modulo 6, eg,
    the subsequent blocks of potential primes are
        [7, 11], [13, 17], [19, 23], [25, 29], [31, 35], [37, 41], ...

    example:
        ```
        window = Window(50)
        window._block
            ~> [49, 53]
        window.next().value
            ~> 53
        window.next().value
            ~> 55
        window.next().value
            ~> 59
        window.prev().value
            ~> 55
        window.prev().value
            ~> 53
        window.prev().value
            ~> 49
        ```
    """

    def __init__(self, number: int, sieve_primes: list[int]):
        self._number = max(1, number)
        self._sieve_primes = sieve_primes
        self._diameter = reduce(lambda acc, prime: acc * prime, sieve_primes)
        self._base_block = prime_to({prime: 1 for prime in sieve_primes})
        self._prime_block = [*sieve_primes, *self._base_block[1:]]
        self._offset = self._number // self._diameter
        self._block = self._get_block(self._offset)
        self._index: int | None = None

    # ------------------------

    def __repr__(self) -> str:
        return f"Window(value={self.value}, block={self._block})"

    # ------------------------

    def next(self) -> "Window":
        """
        Move to the next potential prime, adjusting the block an offset as necessary.

        Note that `self._index` is set here if it is `None`.
        """

        if self._index is None:
            if self._number < self._block[0]:
                self._index = 0
                return self
            elif self._number == self._block[-1]:
                self._index = 0
            else:
                self._index = next(
                    idx for idx, value in enumerate(self._block) if value > self._number
                )
        else:
            self._index = self._next_index()
        if self._index == 0:
            self._block = self._next_block()
            self._offset += 1
        return self

    # ------------------------

    def prev(self) -> "Window":
        """
        Move to the previous potential prime, adjusting the block an offset as
        necessary.

        Note that `self._index` is set here if it is `None`.
        """

        prev_block = self._prev_block()
        if self._index is None:
            if self._number <= self._block[0]:
                self._index = len(prev_block) - 1
            else:
                self._index = next(
                    idx
                    for idx, value in reversed(list(enumerate(self._block)))
                    if value < self._number
                )
        else:
            if self._index == -1:
                return self
            self._index = self._prev_index()
        if self._index == len(prev_block) - 1:
            self._block = prev_block
            self._offset -= 1
        return self

    # ------------------------

    @property
    def value(self) -> int | None:
        """Get the current potential prime."""

        if self._index is None or self._index == -1:
            return None
        return self._block[self._index]

    # ========================

    def _next_block(self) -> list[int]:
        """Get the next block of potential primes."""

        return self._get_block(self._next_offset())

    # ------------------------

    def _prev_block(self) -> list[int]:
        """Get the previous block of potential primes."""

        return self._get_block(self._prev_offset())

    # ------------------------

    def _next_offset(self) -> int:
        """Get the nxt offset."""

        return self._offset + 1

    # ------------------------

    def _prev_offset(self) -> int:
        """Get the previous offset."""

        return max(-1, self._offset - 1)

    # ------------------------

    def _next_index(self) -> int:
        """Get the next index."""

        if self._index == len(self._block) - 1:
            return 0
        if self._index == -1:
            return 0
        assert self._index is not None
        return self._index + 1

    # ------------------------

    def _prev_index(self) -> int:
        """Get the previous index."""

        if self._index == 0:
            return len(self._prev_block()) - 1
        assert self._index is not None
        return max(-1, self._index - 1)

    # ------------------------

    def _get_block(self, offset: int) -> list[int]:
        """
        Get list of potential primes from an offset.

        + offset: int
        ~> list[int]
        """

        if offset < 0:
            return []
        if offset == 0:
            return self._prime_block
        return [value + self._diameter * offset for value in self._base_block]
