#   numth/primality.py
#===========================================================
from .primality_miller_rabin import miller_rabin_test, miller_rabin_cutoffs
from .primality_lucas import lucas_test
#===========================================================

def _default_values(category):
    if category == 'miller_rabin':
        return 40 
    if category == 'lucas':
        return 10

#===========================================================

def is_prime(number, mr_wit=None, l_wit=None):
    """
    Primality test.
        (number: int, mr_wit: int, l_wit: int) -> bool
    Notes:  return_val is whether number is prime
            mr_wit is number of witnesses for miller_rabin_test
            l_wit is number of witness pairs for lucas_test
            if number < 341_550_071_728_321:
                a. only pre-designated Miller-Rabin witnesses are used
                b. the result is deterministic
            otherwise, the result is probabilistic
                incorrect with probability < (1/4)**mr_wit * (4/15)**l_wit
    """
    if number < 2:
        return False

    if number < miller_rabin_cutoffs()[-1][0]:
        return miller_rabin_test(number, 1) == 'prime'

    if mr_wit is None:
        mr_wit = _default_values('miller_rabin')
    if miller_rabin_test(number, mr_wit) == 'composite':
        return False

    if l_wit is None:
        l_wit = _default_values('lucas')
    if lucas_test(number, l_wit) == 'composite':
        return False

    return True

