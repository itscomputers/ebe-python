#   lib/modular/multiplicative_functions.py
#   - module for multiplicative functions relative to a modulus

#===========================================================
from functools import reduce

from ..basic import lcm
from ..factorization import factor
#===========================================================
__all__ = [
    'carmichael_lambda',
    'euler_phi',
]
#===========================================================

def _phi(prime_power_pair):
    """
    Euler's phi function for a power of a prime.

    + (prime, exp): List[int, int]
    ~> int
    """
    prime, exp = prime_power_pair
    return prime**(exp - 1) * (prime - 1)

def _lambda(prime_power_pair):
    """
    Carmichael's lambda function for a power of a prime.

    + (prime, exp): List[int, int]
    ~> int
    """
    if prime_power_pair[0] == 2 and prime_power_pair[1] > 2:
        return _phi(prime_power_pair) // 2
    return _phi(prime_power_pair)

#=============================

def euler_phi_from_factorization(factorization):
    """
    Compute Euler's phi function from `factorization`.

    + factorization: Dict[int, int]
    ~> int
    """
    return reduce(lambda x, y: x * y, map(_phi, factorization.items()), 1)

#-----------------------------

def euler_phi(number_or_factorization):
    """
    Compute Euler's phi function for `number`, which is
    the size of the multiplicative group modulo the `number`.

    example: `euler_phi({2: 3, 5: 2}) ~> 80`
             `euler_phi(200) ~> 80`

    + number_or_factorization: Union[int, Dict[int, int]]
    ~> int
    """
    if isinstance(number_or_factorization, int):
        factorization = factor(number_or_factorization)
    else:
        factorization = number_or_factorization

    return euler_phi_from_factorization(factorization)

#=============================

def carmichael_lambda_from_factorization(factorization):
    """
    Compute Carmichael's lambda function from `factorization`.

    + factorization: Dict[int, int]
    ~> int
    """
    return lcm(*map(_lambda, factorization.items()))

#-----------------------------

def carmichael_lambda(number_or_factorization):
    """
    Compute Carmichale's lambda function for `number`, which is the maximum
    order of an element of the multiplicative group modulo the `number`.

    example: `carmichael_lambda({2: 3, 5: 2}) ~> 20`
             `carmichael_lambda(200) ~> 20`

    + number_or_factorization: Union[int, Dict[int, int]]
    ~> int
    """
    if isinstance(number_or_factorization, int):
        factorization = factor(number_or_factorization)
    else:
        factorization = number_or_factorization

    return carmichael_lambda_from_factorization(factorization)

