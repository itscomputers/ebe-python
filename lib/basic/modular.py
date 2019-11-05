#   lib/basic/modular.py
#   - contains basic functions related to modular arithmetic

#===========================================================
from functools import reduce
import itertools as it

from .division import bezout, gcd, padic
#===========================================================
__all__ = [
    'jacobi',
    'euler_criterion',
    'mod_inverse',
    'mod_power',
    'chinese_remainder_theorem',
    'prime_to',
]
#===========================================================

def jacobi(a, b):
    """
    Jacobi symbol `(a | b)`, a generalization of Lagrange symbol.

    a: int
    b: int --odd
        ~>  int -- 0, 1, or -1
    """

    if b % 2 == 0:
        raise ValueError('jacobi(_, even) is undefined')
    if b == 1:
        return 1
    if gcd(a, b) != 1:
        return 0

    sign = 1
    sign_change = [
        (0, 3, 3), (0, 3, 7),
        (1, 1, 3), (1, 1, 5),
        (1, 3, 5), (1, 3, 7)
    ]
    while b != 1:
        e, r = padic(a % b, 2)
        if (e % 2, r % 4, b % 8) in sign_change:
            sign *= -1
        a, b = b, r

    return sign

#-----------------------------

def euler_criterion(a, p):
    """
    Euler's criterion to compute Lagrange symbol `(a | p)`, which is
    1 if `a` is a square modulo `p`,
    0 if `a` is divisible by `p`, and
    -1 otherwise.

    (Its main purpose here is for testing `lib.basic.modular.jacobi`,
    since the jacobi symbol is both faster and more versatile.)

    a: int
    p: int --prime
        ~>  `int` -- 0, 1, or -1
    """

    result = mod_power(a, (p - 1) // 2, p)
    if result == p - 1:
        return -1

    return 1

#=============================

def mod_inverse(number, modulus):
    """
    Computes multiplicative inverse of `number` relative to `modulus`,
    ie, satisfying
        `(number * inverse) % modulus == 1`.

    number: int --relatively prime to modulus
    modulus: int --at least 2
        ~>  `inverse: int`

    example:
        `mod_inverse(3, 13) ~> 9` and
        `mod_inverse(9, 13) ~> 3`
        since `(3 * 9) % 13 == 1`
    """

    if modulus < 2:
        raise ValueError('modulus must be at least 2')

    inverse = bezout(number, modulus)[0]

    if (number * inverse) % modulus not in [1, -1]:
        raise ValueError('{} not invertible modulo {}'.format(number, modulus))

    if inverse < 0:
        inverse += modulus

    return inverse

#-----------------------------

def mod_power(number, exponent, modulus):
    """
    Computes `(number ** exponent) % modulus`.

    number: int
    exponent: int --negative allowed if number is invertible
    modulus: int --at least 2
        ~>  inverse: int

    example:
        `mod_power(7, -5, 13) ~> 6` and
        `mod_power(2, 5, 13) ~> 6`
        since `7**(-5) % 13 == 2**5 % 13 == 6`.
    """

    if modulus < 2:
        raise ValueError('Modulus must be at least 2')

    if exponent < 0:
        return pow(mod_inverse(number, modulus), -exponent, modulus)

    return pow(number, exponent, modulus)

#=============================

def chinese_remainder_theorem(residues, moduli):
    """
    Computes the unique solution modulo the product of `moduli`
    of the system
        `x % modulus == residue % modulus`
    for each pair `(residue, modulus)` in `zip(residues, moduli)`.

    residues: List[int]
    moduli: List[int] --pairwise relatively prime
        ~>  int

    example:
        `chinese_remainder_theorem([4, 2], [6, 7]) ~> 16`
        since
            `16 % 6 == 4` and
            `16 % 7 == 2`
    """

    moduli_product = reduce(lambda x, y: x * y, moduli, 1)

    return sum(map(
        lambda x, y: (x * y) % moduli_product,
        map(lambda modulus: _coeffs(modulus, moduli_product), moduli),
        residues)
    ) % moduli_product

#-----------------------------

def prime_to(factorization):
    """
    Computes the integers up to the number associated to `factorization`
    which are relatively prime to the number.

    factorization: Dict[int, int] --with shape {prime: exponent}
        ~>  List[int]

    example:
        `prime_to({2: 3, 3: 1}) ~> [1, 5, 7, 11, 13, 17, 19, 23]`
        since these are the numbers between 0 and 24 which are relatively
        prime to `2**3 * 3 == 24`.
    """

    prime_powers = [p**e for (p, e) in factorization.items()]
    number = reduce(lambda x, y: x * y, prime_powers, 1)

    return sorted(
        sum(map(
            lambda x, y: (x * y) % number,
            map(lambda modulus: _coeffs(modulus, number), prime_powers),
            residues
        )) % number for residues in _residues(factorization)
    )

#- - - - - - - - - - - - - - -

def _relatively_prime_to_prime_power(pair):
    return (x for x in range(1, pair[0]**pair[1]) if x % pair[0] != 0)

#- - - - - - - - - - - - - - -

def _residues(factorization):
    return it.product(
        *map(_relatively_prime_to_prime_power, factorization.items())
    )

#- - - - - - - - - - - - - - -

def _coeffs(modulus, moduli_product):
    partial = moduli_product // modulus
    return (partial * mod_inverse(partial, modulus)) % moduli_product

