#   numth/modular/carmichael_lambda.py
#===========================================================
from ..basic import lcm
from ..factorization import factor
#===========================================================

def carmichael_lambda(params):
    """
    Carmichael's lambda function.

    Given an integer or its factorization, calculates Carmichael's
    lambda function of the number, which is the maximum order
    of an element in the multiplicative group modulo the number.

    params
    + int or dict
        number or its prime factorization

    return
    int
    """
    if type(params) is int:
        return carmichael_lambda(factor(number))

    def l(pair):
        prime, exp = pair
        value = prime**(exp - 1) * (prime - 1)
        if prime == 2 and exp > 2:
            return value // 2
        return value

    return lcm(*map(l, params.items()))

