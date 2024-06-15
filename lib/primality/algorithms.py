#   lib/primality/algorithms.py
#   - module for primality testing algorithms

# ===========================================================
import abc
from dataclasses import dataclass
from random import randint
from typing import Generator, Literal, Iterable, Type

from ..basic import gcd, is_square, jacobi, padic
from ..config import default
from ..sequences import LucasSequence

# ===========================================================
__all__ = [
    "is_prime",
    "lucas_test",
    "miller_rabin_test",
    "LucasWitness",
    "MillerRabinWitness",
    "Observation",
]
# ===========================================================


def is_prime(number, miller_rabin_count=None, lucas_count=None):
    """
    Determine if `number` is prime.
    - a return value of `False` is always correct.
    - if `number < 341_550_071_728_321`, only the pre-determined Miller-Rabin
        witnesses are used and the result is deterministic.
    - otherwise, the result is probabalistic with probability of incorrectness
        less than
        `(1/4)**miller_rabin_count * (4/15)**lucas_count`.

    + number: int
    + miller_rabin_count: int --number of Miller-Rabin witnesses
    + lucas_count: int --number of Lucas witness pairs
    ~> bool
    """
    if number < 2:
        return False

    if number == 2:
        return True

    if number % 2 == 0:
        return False

    if number < MillerRabinWitness.MAX_CUTOFF:
        return miller_rabin_test(number, witness_count=1).value == "prime"

    if miller_rabin_count is None:
        miller_rabin_count = default("miller_rabin_witness_count")
    if miller_rabin_test(number, witness_count=miller_rabin_count).value == "composite":
        return False

    if lucas_count is None:
        lucas_count = default("lucas_witness_pair_count")
    if lucas_test(number, witness_count=lucas_count).value == "composite":
        return False

    return True


# -----------------------------


def miller_rabin_test(number: int, witness_count: int) -> "Observation":
    """
    Miller-Rabin test for primality of `number` with `witness_count` witnesses.

    If `number < 341_550_071_729_321`, the test is deterministic and returns an
    observation of `prime` or `composite`.  Otherwise, the test is probabilistic and
    returns an observation of `probable_prime` or `composite`. A `composite` observation
    is a true result while a `probable_prime` observation is a probabilistic result, where
    the probability of being incorrect is less than `(1/4)**witness_count`.

    example:
        `miller_rabin(9958780815586951, witness_count=10)
            ~> Observation(value="probable_prime"`
        so is likely prime with probability > 0.99999904632568359375.

    + number: int
    + witness_count: int
    ~> Observation
    """

    return _observe(number, witness_count, MillerRabinWitness)


# -----------------------------


def lucas_test(number: int, witness_count: int) -> "Observation":
    """
    Lucas test for primality of `number` with `witness_count` witnesses.

    The test is probabilistic and returns an observation of `prime`, `composite`,
    `probable_prime`, or `strong_probable_prime`. A `prime` or `composite` observation is
    a true result while the other two are probabalistic results. In the case of
    `probable_prime`, the probability of incorrectness is less than
    `(4/15)**witness_count`.

    example:
        `lucas_test(9958780815586951, witness_count=10)
            ~> Observation("strong_probable_prime")`
        so is likely prime with probability > 0.99999818160879269759.

    + number: int
    + witness_count: int
    ~> str
    """

    return _observe(number, witness_count, LucasWitness)


# =============================


def _observe(number: int, count: int, cls: Type["PrimalityWitness"]) -> "Observation":
    """
    Combine the observations of `count` witnesses of the given type to provide an
    observation for whether `number` is `composite`, `prime`, `probable_prime` or
    `strong_probable_prime`.

    + number: int
    + count: int
    + cls: Type[PrimalityWitness]
    ~> Observation
    """

    if number < 2:
        raise ValueError("number should be at least 2")
    if number == 2:
        return Observation.prime()
    if number % 2 == 0:
        return Observation.composite()
    return Observation.compose(
        witness.observe(number) for witness in cls.generate(number, count)
    )


# =============================


@dataclass
class Observation:
    """
    Class to hold an observation of primality of a number according to a primality
    witness or a collection of witnesses.

    + value: str
    """

    value: Literal["prime", "probable_prime", "strong_probable_prime", "composite"]

    # ------------------------

    @classmethod
    def prime(cls) -> "Observation":
        return Observation(value="prime")

    # ------------------------

    @classmethod
    def probable_prime(cls, strong: bool = False) -> "Observation":
        if strong:
            return Observation(value="strong_probable_prime")
        return Observation(value="probable_prime")

    # ------------------------

    @classmethod
    def composite(cls) -> "Observation":
        return Observation(value="composite")

    # ------------------------

    @classmethod
    def compose(cls, observations: Iterable["Observation"]) -> "Observation":
        """
        Combine `observations` into a single observation.

        + observations: Iterable[Observation]
        ~> Observation
        """

        strong = False
        prime = False
        for observation in observations:
            if observation.value == "composite":
                return observation
            if observation.value == "prime":
                prime = True
            if observation.value == "strong_probable_prime":
                strong = True
        if prime:
            return Observation.prime()
        return Observation.probable_prime(strong=strong)


# =============================


class PrimalityWitness(abc.ABC):
    """Abstract base class for a primality witness."""

    def observe(self, number: int) -> Observation:
        """
        Observe the primality of a number.

        + number: int
        ~> Observation
        """

        return NotImplemented

    # ------------------------

    @classmethod
    def generate(
        cls,
        number: int,
        count: int,
    ) -> Generator["PrimalityWitness", None, None]:
        """
        Generate a collection of primality witnesses.

        + number: int --number to test primality of
        + count: int --number of witnesses to generate
        ~> Generator[PrimalityWitness]
        """

        return NotImplemented


# =============================


class MillerRabinWitness(PrimalityWitness):
    """
    Witness for the Miller-Rabin primality test.

    + value: int --witness value
    + assured: bool --whether a positive result is `prime` or `probable_prime`
    """

    MAX_CUTOFF = 341550071728321
    CUTOFFS = (
        (1, 2),
        (2047, 3),
        (1373653, 5),
        (25326001, 7),
        (3215031751, 11),
        (2152302898747, 13),
        (3474749660383, 17),
    )

    def __init__(self, value: int, assured: bool = False):
        self._value = value
        self._assured = assured

    # ------------------------

    def __repr__(self) -> str:
        return f"MillerRabinWitness(value={self._value}, assured={self._assured})"

    # ------------------------

    def observe(self, number: int) -> Observation:
        """
        Observe the primality of a number, according to a Miller-Rabin witness.

        Possible observations:
            - prime
            - probable_prime
            - composite

        + number: int
        ~> Observation
        """

        exp, rest = padic(number - 1, 2)
        x = pow(self._value, rest, number)

        if x == 1 or x == number - 1:
            if self._assured:
                return Observation.prime()
            return Observation.probable_prime()

        for _ in range(exp):
            x = pow(x, 2, number)

            if x == number - 1:
                if self._assured:
                    return Observation.prime()
                return Observation.probable_prime()

            if x == 1:
                return Observation.composite()

        return Observation.composite()

    # ------------------------

    @classmethod
    def generate(
        cls,
        number: int,
        count: int,
    ) -> Generator["MillerRabinWitness", None, None]:
        """
        Generate a collection of Miller-Rabin witnesses.

        + number: int --number to test primality of
        + count: int --number of witnesses to generate
        ~> Generator[MillerRabinWitness]
        """

        if number > MillerRabinWitness.MAX_CUTOFF:
            if count > number:
                for value in range(2, number - 1):
                    yield MillerRabinWitness(value, assured=True)
            else:
                values: set[int] = set()
                while len(values) < count:
                    value = randint(2, number - 1)
                    if value not in values:
                        values.add(value)
                        yield MillerRabinWitness(value)

        else:
            for value, prime in MillerRabinWitness.CUTOFFS:
                if number >= value:
                    yield MillerRabinWitness(prime, assured=True)


# =============================


class LucasWitness(PrimalityWitness):
    """
    Witness for the Lucas primality test.

    + p: int --Lucas sequence parameter
    + q: int --Lucas sequence parameter
    """

    def __init__(self, p: int, q: int):
        self._p = p
        self._q = q
        self._disc = p**2 - 4 * q
        self._strong = False

    # ------------------------

    def __repr__(self) -> str:
        return f"LucasWitness(value=({self._p}, {self._q}))"

    # ------------------------

    def observe(self, number: int) -> Observation:
        """
        Observe the primality of a number, according to a Lucas witness.

        Possible observations:
            - probable_prime
            - strong_probable_prime
            - composite

        + number: int
        ~> Observation
        """

        observation = self._first_observation(number)
        if observation is not None:
            return observation

        delta = number - jacobi(self._disc, number)
        upper, index = padic(delta, 2)
        seq = LucasSequence.at_index(index, p=self._p, q=self._q, modulus=number)
        q = seq.value.q

        if seq.value.u == 0:
            self._strong = True

        for _ in range(upper - 1):
            seq.double_index()
            q = seq.value.q
            if seq.value.v == 0:
                self._strong = True

        seq.double_index()
        if seq.value.u == 0:
            if delta == number + 1:
                if seq.value.v != 2 * self._q % number:
                    return Observation.composite()
                if q != self._q * jacobi(self._q, number) % number:
                    return Observation.composite()
            elif q != jacobi(self._q, number) % number:
                return Observation.composite()
            return Observation.probable_prime(strong=self._strong)

        return Observation.composite()

    # ------------------------

    @classmethod
    def generate(
        cls,
        number: int,
        count: int,
    ) -> Generator["LucasWitness", None, None]:
        """
        Generate a collection of Lucas witnesses.

        + number: int --number to test primality of
        + count: int --number of witnesses to generate
        ~> Generator[LucasWitness]
        """

        result_count = 0
        if not is_square(number):
            d = 5
            sgn = 1
            while result_count < count // 2 + 1:
                if jacobi(d * sgn, number) == -1:
                    result_count += 1
                    yield LucasWitness(1, (1 - d * sgn) // 4)
                d += 2
                sgn *= -1

        while result_count < count:
            p = randint(1, 100 * count)
            q = randint(1, 100 * count)
            if _good_parameters(number, p, q) > 0:
                result_count += 1
                yield LucasWitness(p, q)

    # ========================

    def _first_observation(self, number: int) -> Observation | None:
        """
        Initial observation that might be composite.

        + number: int
        - raises ValueError if the Lucas parameters are ill-suited for `number`
        ~> Observation | None
        """
        fit = _good_parameters(number, self._p, self._q, self._disc)

        if fit == 0:
            raise ValueError(f"Bad witness for {number}")
        if fit > 1:
            return Observation.composite()
        return None


# =============================


def _good_parameters(number: int, p: int, q: int, disc: int | None = None) -> int:
    """
    Determine if Lucas parameters are a bad fit for a number.

    return value:
        0 ~> bad fit
        1 ~> good fit
        > 1 ~> detected a divisor

    + number: int
    + p: int
    + q: int
    + disc: int
    ~> int
    """

    if disc is None:
        disc = p**2 - 4 * q
    for divisor in (gcd(p, number), gcd(q, number), gcd(disc, number)):
        if divisor == number:
            return 0
        if divisor > 1:
            return divisor

    return 1
