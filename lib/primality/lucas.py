#   lib/primality/lucas.py
#   - module for lucas primalit testing
# ===========================================================
from random import randint

from ..basic import gcd, is_square, jacobi, padic
from ..lucas_sequence import lucas_mod_by_index, lucas_mod_double_index

# ===========================================================
__all__ = [
    "lucas_witness_pair",
    "lucas_witness_pairs",
    "lucas_test",
]
# ===========================================================


def lucas_witness_pair(number, P, Q):
    """
    Determine if `number` is composite or probably prime
    according `(P, Q)`-Lucas sequence pair.

    examples: `lucas_witness_pair(561, 4, 8) ~> ('probable prime', True)`
              `lucas_witness_pair(561, 13, 2) ~> ('probable prime', False)`
              `lucas_witness_pair(561, 3, 5) ~> ('composite', False)`

    + number: int
    + P: int
    + Q: int
    ~> (primality, strong): Tuple[str, bool]
    """
    D = P ** 2 - 4 * Q

    valid = _good_parameters(number, P, Q, D)
    if valid is False:
        raise ValueError("Bad parameters")
    if type(valid) is int:
        return "composite", False

    delta = number - jacobi(D, number)
    s, d = padic(delta, 2)
    strong = False

    U, V, Q_k = lucas_mod_by_index(d, P, Q, number)
    if U == 0:
        strong = True

    for j in range(s - 1):
        U, V, Q_k = lucas_mod_double_index(U, V, Q_k, number)
        if V == 0:
            strong = True

    U, V, Q_ = lucas_mod_double_index(U, V, Q_k, number)
    if U == 0:
        if _trivially_composite(V, Q, Q_k, number, delta):
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
        if P % number != 0 and Q % number != 0 and (P ** 2 - 4 * Q) % number != 0:
            witnesses = witnesses | set([(P, Q)])

    return witnesses


# =============================


def _good_parameters(number, P, Q, D):
    """Validate parameters are good."""
    for d in (gcd(P, number), gcd(Q, number), gcd(D, number)):
        if d == number:
            return False
        if d > 1:
            return d
    return True


# -----------------------------


def _trivially_composite(V, Q, Q_power, number, delta):
    """Determine if `number` is trivially composite."""
    if delta == number + 1:
        if V != (2 * Q) % number:
            return True
        if Q_power != (Q * jacobi(Q, number)) % number:
            return True
    else:
        if Q_power != jacobi(Q, number) % number:
            return True

    return False
