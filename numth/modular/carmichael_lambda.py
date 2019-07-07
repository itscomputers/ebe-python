#   numth/modular/carmichael_lambda.py
#===========================================================
from ..basic import lcm
from ..factorization import factor
#===========================================================
def carmichael_lambda_from_factorization(factorization):
    """
    Carmichael's lambda function.

    Given a factorization, calculates Carmichael's lambda function of 
    the corresponding number.

    params
    + factorization : dict
        prime divisors of a number with multiplicity

    return
    int
    """
    def l(pair):
        prime, exp = pair
        value = prime**(exp - 1) * (prime - 1)
        if prime == 2 and exp > 2:
            return value // 2
        return value

    return lcm(*map(l, factorization.items()))

#-----------------------------

def carmichael_lambda(number):
    """
    Carmichael's lambda function.

    Calculates the maximum order of an element of the multiplicative
    group modulo number.

    params
    + number : int 

    return
    int
    """
    return carmichael_lambda_from_factorization(factor(number))

