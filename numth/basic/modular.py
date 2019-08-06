#   numth/basic/modular.py
#===========================================================
from functools import reduce
from itertools import product
from typing import Dict, Iterator, List, Tuple

from .division import bezout, gcd, padic
#===========================================================

def jacobi(a: int, b: int) -> int:
    """
    Computes Jacobi symbol `(a | b)`, a generalization of Lagrange symbol.

    params:
        `a : int`,
        `b : int --odd`

    returns:
        `1, 0, or -1`
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

def euler_criterion(a: int, p: int) -> int:
    """
    Uses Euler's criterion to compute Lagrange symbol `(a | p)`,
    which is equal to `1` if `a` is a square modulo `p` and `-1` otherwise.
    (Its main purpose here is for testing `numth.basic.modular.jacobi`,
    since the jacobi symbol is both faster and more versatile.)

    params:
        `a : int`,
        `p : int --prime`

    returns:
        `1 or -1`
    """
    result = mod_power(a, (p - 1) // 2, p)
    if result == p - 1:
        return -1

    return 1

#=============================

def mod_inverse(number: int, modulus: int) -> int:
    """
    Computes `inverse` of `number` relative to `modulus`, satisfying
        `(number * inverse) % modulus == 1`.

    example:
        `mod_inverse(7, 13) => 2` and
        `mod_inverse(2, 13) => 7`
        since `(7 * 2) % 13 == 1`

    params:
        `number : int`,
        `modulus : int --at least 2`

    returns:
        `inverse : int`
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

def mod_power(number: int, exponent: int, modulus: int) -> int:
    """
    Computes `(number ** exponent) % modulus`
    where `exponent` can be positive or negative.

    example:
        `mod_power(7, -5, 13) => 6` and
        `mod_power(2, 5, 13) => 6`
        since `7**(-5) % 13 == 2**5 % 13 == 6`.

    params:
        `number : int`,
        `exponent : int`,
        `modulus : int --at least 2`

    returns:
        `int`
    """
    if modulus < 2:
        raise ValueError('Modulus must be at least 2')

    if exponent < 0:
        return pow(mod_inverse(number, modulus), -exponent, modulus)

    return pow(number, exponent, modulus)

#=============================

def chinese_remainder_theorem(residues: List[int], moduli: List[int]) -> int:
    """
    Computes the unique solution modulo the product of `moduli`
    of the system
        `x % modulus == residue % modulus`
    for each pair `(residue, modulus)` in `zip(residues, moduli)`.

    example:
        `chinese_remainder_theorem([4, 2], [6, 7]) => 16`
        since
            `16 % 6 == 4` and
            `16 % 7 == 2`

    params:
        `residues : list of int`,
        `moduli : list of int --each at least 2 and pair-wise relatively prime`

    returns:
        `int`
    """
    moduli_product = reduce(lambda x, y: x * y, moduli, 1)

    return sum(map(
        lambda x, y: (x * y) % moduli_product,
        map(lambda modulus: _coeffs(modulus, moduli_product), moduli),
        residues)
    ) % moduli_product

#-----------------------------

def prime_to(factorization: Dict[int, int]) -> List[int]:
    """
    Computes the integers up to the number associated to `factorization`
    which are relatively prime to the number.

    example:
        `prime_to({2: 3, 3: 1}) => [1, 5, 7, 11, 13, 17, 19, 23]`
        since these are the numbers between 0 and 24 which are relatively
        prime to `2**3 * 3 == 24`.

    params:
        `factorization : dict` --with shape `{prime : exponent}`

    returns:
        `list of int`
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

def _prime_to_prime_power(pair: Tuple[int, int]) -> Iterator[int]:
    return (x for x in range(1, pair[0]**pair[1]) if x % pair[0] != 0)

#- - - - - - - - - - - - - - -

def _residues(factorization: Dict[int, int]) -> Iterator[Tuple[int, ...]]:
    return product(*map(_prime_to_prime_power, factorization.items()))

#- - - - - - - - - - - - - - -

def _coeffs(modulus: int, moduli_product: int) -> int:
    partial = moduli_product // modulus
    return (partial * mod_inverse(partial, modulus)) % moduli_product
