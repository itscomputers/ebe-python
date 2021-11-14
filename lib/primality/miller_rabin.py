#   lib/primality/miller_rabin.py
#   - module for miller-rabin primality testing

# ===========================================================
from random import randint

from ..basic import padic

# ===========================================================
__all__ = [
    "miller_rabin_witness",
    "miller_rabin_witnesses",
    "miller_rabin_test",
    "miller_rabin_max_cutoff",
    "miller_rabin_cutoffs",
]
# ===========================================================


def miller_rabin_witness(number, witness):
    """
    Determine if `number` is composite or probably prime
    according to Miller-Rabin `witness`.

    examples: `miller_rabin_witness(561, 101) ~> 'probable prime'`
              `miller_rabin_witness(561, 103) ~> 'probable prime'`
              `miller_rabin_witness(561, 105) ~> 'composite'`

    + number: int
    + witness: int
    ~> str
    """
    exp, rest = padic(number - 1, 2)
    x = pow(witness, rest, number)

    if x in [1, number - 1]:
        return "probable prime"

    for j in range(exp):
        x = pow(x, 2, number)

        if x == number - 1:
            return "probable prime"

        if x == 1:
            return "composite"

    return "composite"


# -----------------------------


def miller_rabin_witnesses(number, witnesses):
    """
    Determine if `number` is composite or probably prime
    according to array of Miller-Rabin `witnesses`.

    examples: `miller_rabin_witnesses(561, [101, 103]) ~> 'probable prime'`
              `miller_rabin_witnesses(561, [103, 105]) ~> 'composite'`

    + number: int
    + witnesses: List[int]
    ~> str
    """
    for witness in witnesses:
        if miller_rabin_witness(number, witness) == "composite":
            return "composite"

    return "probable prime"


# -----------------------------


def miller_rabin_test(number, num_witnesses):
    """
    Miller-Rabin test for primality of `number` with `num_witnesses` witnesses.
    If `number < 341_550_071_729_321`, test is deterministic.  Otherwise,
    `probable prime` is probabilistic with probability of incorrectness
    less than `(1/4)**num_witnesses`.

    example: `miller_rabin_test(9958780815586951, 10) ~> 'probable prime'`
        so is probably prime with certainty > 0.99999904632568359375.

    + number: int
    + num_witnesses: int
    ~> str
    """
    if number < 2:
        raise ValueError("number should be at least 2")
    if number == 2:
        return "prime"

    primality = miller_rabin_witnesses(number, _generate_witnesses(number, num_witnesses))
    if primality == "probable prime" and number < miller_rabin_max_cutoff():
        return "prime"

    return primality


# =============================


def miller_rabin_max_cutoff():
    return 341550071728321


def miller_rabin_cutoffs():
    return (
        (1, 2),
        (2047, 3),
        (1373653, 5),
        (25326001, 7),
        (3215031751, 11),
        (2152302898747, 13),
        (3474749660383, 17),
    )


def _generate_witnesses(number, num_witnesses):
    """Generate random witnesses for Miller-Rabin test."""
    if number > miller_rabin_max_cutoff():
        if num_witnesses > number:
            witnesses = set(x for x in range(2, number - 1))
        else:
            witnesses = set()
            while len(witnesses) < num_witnesses:
                witnesses = witnesses | set([randint(2, number - 1)])

    else:
        witnesses = set(p for val, p in miller_rabin_cutoffs() if number >= val)

    return witnesses
