#   lib/factorization/algorithms.py
#   - module for factor-finding algorithms for composite numbers

#===========================================================
from ..basic import gcd
#===========================================================
__all__ = [
    'pollard_rho_gen',
    'pollard_rho',
    'pollard_p_minus_one_gen',
    'pollard_p_minus_one',
    'williams_p_plus_one_gen',
    'williams_p_plus_one',
]
#===========================================================

def pollard_rho_gen(number, seed, func):
    """
    Generator for Pollard's rho algorithm.

    + number: int --composite
    + seed: int
    + func: Callable[[int], int]
    ~> Iterator[int]
    """
    x_i = func(seed % number)
    x_2i = func(x_i) % number

    while True:
        yield gcd(x_2i - x_i, number)
        x_i = func(x_i) % number
        x_2i = func(func(x_2i) % number) % number

#-----------------------------

def pollard_rho(number, seed, func):
    """
    Pollard's rho algorithm to find divisor of `number`.

    example: `pollard_rho(143, 2, lambda x: x**2 + 1) ~> 11`

    + number: int --composite
    + seed: int
    + func: Callable[[int], int]
    ~> int --either nontrivial divisor or number itself
    """
    gen = pollard_rho_gen(number, seed, func)
    divisor = next(gen)

    while divisor == 1:
        divisor = next(gen)

    return divisor

#=============================

def pollard_p_minus_one_gen(number, seed):
    """
    Generator for Pollard's p-1 algorithm.

    + number: int --composite
    + seed: int
    ~> Iterator[int]
    """
    x_i = seed % number
    index = 1

    while True:
        yield gcd(x_i - 1, number)
        index = index + 1
        x_i = pow(x_i, index, number)

#-----------------------------

def pollard_p_minus_one(number, seed):
    """
    Pollard's p-1 algorithm to find divisor of `number`.

    example `pollard_p_minus_one(143, 2) ~> 13`

    + number: int --composite
    + seed: int
    ~> int --either nontrivial divisor or number itself
    """
    divisor = gcd(number, seed)
    if divisor > 1:
        return divisor

    gen = pollard_p_minus_one_gen(number, seed)
    divisor = next(gen)

    while divisor == 1:
        divisor = next(gen)

    return divisor

#=============================

def williams_p_plus_one_gen(number, quadratic_seed):
    """
    Generator for Williams' p+1 algorithm.

    + number: int --composite
    + quadratic_seed: QuadraticInteger
    ~> Iterator[int]
    """
    z = quadratic_seed
    power = 1
    yield gcd(z.norm, number)

    while True:
        power = power + 1
        z = pow(z, power, number)
        yield gcd(z.imag, number)

#-----------------------------

def williams_p_plus_one(number, quadratic_seed):
    """
    Williams' p+1 algorithm to find divisor.

    example: `williams_p_plus_one(143, GaussianInteger(1, 2)) ~> 11`

    + number: int --composite
    + quadratic_seed: GaussianInteger
    ~> int --either nontrivial divisor or number itself
    """
    gen = williams_p_plus_one_gen(number, quadratic_seed)
    divisor = next(gen)

    while divisor == 1:
        divisor = next(gen)

    return divisor

