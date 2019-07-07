#   numth/modular/euler_phi.py
#===========================================================
from functools import reduce

from ..factorization import factor
#===========================================================

def euler_phi_from_factorization(factorization):
    """
    Euler's phi function.

    Given a factorization, calculates Euler's phi function of 
    the corresponding number.

    params
    + factorization : dict
        prime divisors of a number with multiplicity

    return
    int
    """
    def euler(prime_power):
        prime, exp = prime_power
        return prime**(exp - 1) * (prime - 1)

    return reduce(lambda x, y: x * y, map(euler, factorization.items()), 1)

#-----------------------------

def euler_phi(number):
    """
    Euler's phi function.

    Calculates the number of integers between 0 and number that are
    relatively prime to number, ie, the size of the multiplicative
    group modulo number.

    params
    + number : int

    return
    int
    """
    return euler_phi_from_factorization(factor(number))

