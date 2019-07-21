#   numth/basic/modular.py
#===========================================================
from functools import reduce
from itertools import product

from .division import bezout, gcd, padic
#===========================================================

def jacobi(a, b):
    """
    Jacobi symbol.
    
    Computes the Jacobi symbol (a | b), generalization of Lagrange symbol.

    params:
    + a : int
    + b : int
        odd

    return
    int
        1, 0, or -1
    """
    if b % 2 == 0:
        raise ValueError(
                'Jacobi symbol is undefined when second argument is even')

    if b == 1:
        return 1
    if gcd(a, b) != 1:
        return 0

    return _jacobi_helper(a, b)

# - - - - - - - - - - - - - - 

def _jacobi_helper(a, b):
    sign = 1
    while b != 1:
        e, r = padic(a % b, 2)
        if (e % 2, r % 4, b % 8) in [
            (0, 3, 3),
            (0, 3, 7),
            (1, 1, 3),
            (1, 1, 5),
            (1, 3, 5),
            (1, 3, 7)
        ]:
            sign *= -1
        a, b = b, r

    return sign

#-----------------------------

def euler_criterion(a, p):
    """
    Euler criterion.

    Computes the Lagrange symbol (a | p) for p prime.
        * same as jacobi(a | p)
        * jacobi symbol is faster, this is primarily for testing purposes

    params:
    + a : int
        relatively prime to p
    + p : int
        prime

    return
    int
        * 1 if a is a square modulo p
        * -1 if a is not a square modulo p
    """
    result = mod_power(a, (p-1)//2, p)

    if result == p - 1:
        return -1
    
    return 1

#=============================

def mod_inverse(number, modulus):
    """
    The inverse of under modular multiplication.

    Computes inverse such that ``number * inverse % modulus == 1``

    params
    + number : int
        relatively prime to modulus
    + modulus : int
        greater than 1

    return
    int
    """
    if modulus < 2:
        raise ValueError('Modulus must be at least 2')

    inverse = bezout(number, modulus)[0]
    
    if number * inverse % modulus not in [1, -1]:
        raise ValueError(
                '{} is not invertible modulo {}'
                .format(number, modulus))

    if inverse < 0:
        inverse += modulus

    return inverse

#-----------------------------

def mod_power(number, exponent, modulus):
    """
    Power of a number relative to a modulus.
    
    Computes ``number ** exponent % modulus``, even for negative exponent.

    params
    + number : int
    + exponent : int
    + modulus : int
        greater than 1

    return
    int
    """
    if modulus < 2:
        raise ValueError('Modulus must be at least 2')

    if exponent < 0:
        return pow(mod_inverse(number, modulus), -exponent, modulus)
    
    return pow(number, exponent, modulus)

#=============================

def chinese_remainder_theorem(residues, moduli):
    """
    Chinese remainder theorem.

    Computes the unique solution modulo product of moduli to the system 
        ``x % modulus == residue % modulus``
        for each pair in ``zip(residues, moduli)``

    params
    residues : iterable(int)
    moduli : interable(int)
        all greater than 1 and pair-wise relatively prime

    return
    int
    """
    moduli_product = reduce(lambda x, y: x * y, moduli, 1)
    
    return sum(map(
        lambda x, y: (x * y) % moduli_product,
        _chinese_remainder_coeffs(moduli, moduli_product),
        residues)
    ) % moduli_product

#- - - - - - - - - - - - - - -

def _chinese_remainder_coeffs(moduli, moduli_product):
    def coeff(modulus):
        partial = moduli_product // modulus
        return (partial * mod_inverse(partial, modulus)) % moduli_product

    return map(coeff, moduli)

#-----------------------------

def prime_to(factorization):
    """
    List of numbers which are relatively prime to given prime factorization.

    Computes list of x for x < associated number such that
    ``gcd(x, number) == 1``.

    params
    + factorization : dict
        has the shape {prime : power} for distinct primes

    return
    list(int)
    """
    prime_powers = [p**e for (p, e) in factorization.items()]
    number = reduce(lambda x, y: x * y, prime_powers, 1)

    return sorted(
        sum(map(
            lambda x, y: (x * y) % number,
            _chinese_remainder_coeffs(prime_powers, number),
            residues
        )) % number for residues in _residues(factorization)
    )

#- - - - - - - - - - - - - - -

def _prime_to_prime_power(pair):
    return (x for x in range(1, pair[0]**pair[1]) if x % pair[0] != 0)

#- - - - - - - - - - - - - - -

def _residues(factorization):
    return product(*map(_prime_to_prime_power, factorization.items()))

