#   numth/modular/euler_phi.py
#===========================================================
from functools import reduce

from ..factorization import factor
#===========================================================

def euler_phi(params):
    """
    Euler's phi function.

    Given an integer or itsfactorization, calculates Euler's phi function of 
    the corresponding number, which is the size of the multiplicative group
    modulo the number.

    params
    + int or dict
        number or its prime factorization

    return
    int
    """
    if type(params) is int:
        return euler_phi(factor(params))

    def euler(prime_power):
        prime, exp = prime_power
        return prime**(exp - 1) * (prime - 1)

    return reduce(lambda x, y: x * y, map(euler, params.items()), 1)

