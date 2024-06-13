#   lib/primality/lucas.py
#   - module for lucas primalit testing
# ===========================================================
from random import randint

from ..basic import gcd, is_square, jacobi, padic
from ..sequences import LucasSequence

# ===========================================================
__all__ = [
    "lucas_witness_pair",
    "lucas_witness_pairs",
    "lucas_test",
]
# ===========================================================


def lucas_witness_pair(number: int, p: int, q: int):
    """
    Determine if `number` is composite or probably prime
    according `(p, q)`-Lucas sequence pair.

    examples: `lucas_witness_pair(561, 4, 8) ~> ('probable prime', True)`
              `lucas_witness_pair(561, 13, 2) ~> ('probable prime', False)`
              `lucas_witness_pair(561, 3, 5) ~> ('composite', False)`

    + number: int
    + p: int
    + q: int
    ~> (primality, strong): Tuple[str, bool]
    """
    disc = p**2 - 4 * q

    valid = _good_parameters(number, p, q, disc)
    if valid is False:
        raise ValueError("Bad parameters")
    if type(valid) is int:
        return "composite", False

    delta = number - jacobi(disc, number)
    s, d = padic(delta, 2)
    strong = False

    seq = LucasSequence.at_index(d, p=p, q=q, modulus=number)
    q_k = seq.value.q
    if seq.value.u == 0:
        strong = True

    for j in range(s - 1):
        seq.double_index()
        q_k = seq.value.q
        if seq.value.v == 0:
            strong = True

    seq.double_index()
    if seq.value.u == 0:
        if _trivially_composite(seq.value.v, q, q_k, number, delta):
            return "composite", False
        return "probable prime", strong

    return "composite", False


# -----------------------------


def lucas_witness_pairs(number, witness_pairs):
    """
    Determine if `number` is composite or probably prime
    according `witness_pairs` number of Lucas sequence pairs.

    examples:
        `lucas_witness_pair(561, [4, 8], [13, 2]) ~> ('probable prime', True)`
        `lucas_witness_pair(561, [13, 2], [14, -1]) ~> ('probable prime', False)`
        `lucas_witness_pair(561, [4, 8], [3, 5]) ~> ('composite', False)`

    + number: int
    + witness_pairs: int
    ~> (primality, strong): Tuple[str, bool]
    """
    strong = False
    for pair in witness_pairs:
        primality, witness_strong = lucas_witness_pair(number, *pair)
        if primality == "composite":
            return "composite", False
        if witness_strong:
            strong = True

    return "probable prime", strong


# -----------------------------


def lucas_test(number, num_witnesses):
    """
    Lucas test for primality of `number` with `num_witnesses` witness pairs.
    The test returns `composite`, `probable prime`, or `strong probable prime`.
    The probability of incorrectness is less than `(4/15)**num_witnesses`.

    example: `lucas_test(9958780815586951, 10) ~> 'strong probable prime'`
        so is probably prime with certainty > 0.99999818160879269759.

    + number: int
    + num_witnesses: int
    ~> str
    """
    if number < 3:
        raise ValueError("Number should be at least 3")
    if number % 2 == 0:
        return "composite"

    witness_pairs = _generate_witness_pairs(number, num_witnesses)
    primality, strong = lucas_witness_pairs(number, witness_pairs)

    if primality == "composite" or strong is False:
        return primality

    return "strong probable prime"


# =============================


def _generate_witness_pairs(number, num_witnesses):
    """Generate witness pairs for Lucas test."""
    witnesses = set()

    if not is_square(number):
        D = 5
        sgn = 1
        while len(witnesses) < num_witnesses // 2 + 1:
            if jacobi(D * sgn, number) == -1:
                witnesses = witnesses | set([(1, (1 - D * sgn) // 4)])
            D += 2
            sgn *= -1

    while len(witnesses) < num_witnesses:
        P = randint(1, 100 * num_witnesses)
        Q = randint(1, 100 * num_witnesses)
        if P % number != 0 and Q % number != 0 and (P**2 - 4 * Q) % number != 0:
            witnesses = witnesses | set([(P, Q)])

    return witnesses


# =============================


def _good_parameters(number: int, p: int, q: int, disc: int) -> int | bool:
    """Validate parameters are good."""
    for d in (gcd(p, number), gcd(q, number), gcd(disc, number)):
        if d == number:
            return False
        if d > 1:
            return d
    return True


# -----------------------------


def _trivially_composite(v: int, q: int, q_power: int, number: int, delta: int) -> bool:
    """Determine if `number` is trivially composite."""
    if delta == number + 1:
        if v != (2 * q) % number:
            return True
        if q_power != (q * jacobi(q, number)) % number:
            return True
    else:
        if q_power != jacobi(q, number) % number:
            return True

    return False
