#   lib/modular/sqrt.py
#   - module for modular square roots

# ===========================================================
from functools import reduce

from ..basic import jacobi, padic
from ..primality import is_prime
from ..types import QuadraticInteger

# ===========================================================
__all__ = [
    "mod_sqrt",
    "mod_sqrt_minus_one_wilson",
    "mod_sqrt_minus_one_legendre",
    "mod_sqrt_when_three_mod_four",
    "mod_sqrt_tonelli_shanks",
    "mod_sqrt_cipolla",
]
# ===========================================================


def mod_sqrt(number, prime):
    """
    Compute square roots of `number` modulo `prime`,
    which exist for odd `prime` if and only if `jacobi(numer, prime) == 1`.

    example: `mod_sqrt(2, 7) ~> (3, 4)`
        since `3**2 % 7 == 4**2 % 7 == 2`

    + number: int
    + prime: int --prime
    ~> Tuple[int, int]
    """
    if not is_prime(prime):
        raise ValueError("{} must be prime".format(prime))

    if prime == 2 or number % prime == 0:
        return (number, number)

    if jacobi(number, prime) != 1:
        return None

    if prime % 4 == 3:
        return mod_sqrt_when_three_mod_four(number, prime)

    s, q = padic(prime - 1, 2)
    m = len(bin(prime)[2:])

    if s * (s - 1) > 8 * m + 20:
        return mod_sqrt_cipolla(number, prime)

    return mod_sqrt_tonelli_shanks(number, prime, s, q, m)


# =============================


def mod_sqrt_minus_one_wilson(prime):
    """
    Compute square roots of -1 modulo `prime` using Wilson's Theorem,
    which exist if and only if `prime % 4 == 1`.

    example: `mod_sqrt_minus_one_wilson(13) ~> (5, 8)`
        since `5**2 % 13 == 8**2 % 13 == -1 % 13`

    + prime: int --prime
    ~> Tuple[int, int]
    """
    if prime == 2:
        return (1, 1)

    if prime % 4 == 3:
        raise ValueError("-1 is not a square modulo {}".format(prime))

    val = reduce(lambda x, y: (x * y) % prime, range(2, (prime - 1) // 2 + 1), 1)
    return tuple(sorted([val, prime - val]))


# -----------------------------


def mod_sqrt_minus_one_legendre(prime):
    """
    Compute square roots of -1 modulo `prime` using Legendre's method,
    which exist if and only if `prime % 4 == 1`.

    examples: `mod_sqrt_minus_one_legendre(13) ~> (5, 8)`
        since `5**2 % 13 == 8**2 % 13 == -1 % 13`

    + prime: int --prime
    ~> Tuple[int, int]
    """
    if prime == 2:
        return (1, 1)

    if prime % 4 == 3:
        raise ValueError("-1 is not a square modulo {}".format(prime))

    for x in range(2, prime - 1):
        if jacobi(x, prime) == -1:
            val = pow(x, (prime - 1) // 4, prime)
    return tuple(sorted([val, prime - val]))


# -----------------------------


def mod_sqrt_when_three_mod_four(number, prime):
    """
    Compute square roots of `number` modulo `prime` if `prime % 4 == 3`.

    example: `mod_sqrt_when_three_mod_four(3, 11) ~> (5, 6)`

    + number: int
    + prime: int --prime and 3 modulo 4
    ~> Tuple[int, int]
    """
    if prime % 4 != 3:
        raise ValueError("Use a different mod_sqrt function")

    val = pow(number, (prime + 1) // 4, prime)
    return tuple(sorted([val, prime - val]))


# -----------------------------


def mod_sqrt_cipolla(number, prime):
    """
    Compute square roots of `number` modulo `prime`
    using Cipolla algorithm.

    example: `mod_sqrt_cipolla(8, 17) ~> (5, 12)`

    + number: int
    + prime: int --prime and 3 modulo 4
    ~> Tuple[int, int]
    """
    for y in range(2, prime):
        root = (y ** 2 - number) % prime
        if jacobi(root, prime) == -1:
            break

    val = pow(QuadraticInteger(y, 1, root), (prime + 1) // 2, prime).real
    return tuple(sorted([val, prime - val]))


# -----------------------------


def mod_sqrt_tonelli_shanks(number, prime, *params):
    """
    Compute square roots of `number` modulo `prime`
    using Tonelli-Shanks algorithm.

    example: `mod_sqrt_tonelli_shanks(8, 17) ~> (5, 12)`

    + number: int
    + prime: int --prime and 3 modulo 4
    + params: List[int] --can be pre-computed
    ~> Tuple[int, int]
    """
    if params == ():
        s, q = padic(prime - 1, 2)
        m = len(bin(prime)[2:])
    else:
        s, q, m = params

    for z in range(1, prime):
        if jacobi(z, prime) == -1:
            break

    m = s
    c = pow(z, q, prime)
    t = pow(number, q, prime)
    val = pow(number, (q + 1) // 2, prime)

    while t != 1:
        m, c, t, val = _tonelli_shanks_helper(m, c, t, val, prime)

    return tuple(sorted([val, prime - val]))


# =============================


def _tonelli_shanks_helper(m, c, t, val, prime):
    _t = t
    for _m in range(1, m):
        _t = pow(_t, 2, prime)
        if _t == 1:
            break

    b = pow(c, 2 ** (m - _m - 1), prime)
    _c = pow(b, 2, prime)
    _t = (t * _c) % prime
    _val = (val * b) % prime

    return _m, _c, _t, _val
