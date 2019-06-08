#   numth/primality_miller_rabin.py
#===========================================================
from random import randint

from .basic import padic 
#===========================================================

def miller_rabin_witness(number, witness):
    """
    Miller-Rabin witness for primality.
        (number: int, witness: int) -> str
    Notes:  return_value is whether witness thinks number is prime or composite
    """
    exp, rest  = padic(number - 1, 2)
    x = pow(witness, rest, number)

    if x in [1, number - 1]:
        return 'probable prime'

    for j in range(exp):
        x = pow(x, 2, number)
        
        if x == number - 1:
            return 'probable prime'
        
        if x == 1:
            return 'composite'

    return 'composite'

#-----------------------------

def miller_rabin_witnesses(number, witnesses):
    """
    Combination of Miller-Rabin witnesses for primality.
        (number: int, witnesses: iterable) -> str
    """
    for witness in witnesses:
        if miller_rabin_witness(number, witness) == 'composite':
            return 'composite'

    if number < miller_rabin_cutoffs()[-1][0]:
        return 'prime'

    return 'probable prime'

#-----------------------------

def miller_rabin_test(number, num_witnesses):
    """
    Miller-Rabin test for primality.
        (number: int, num_witnesses: int) -> str
    Notes:  'composite' is definitive
            'prime' is definitive and only returned if number < 341550071728321
            'strong probable prime' is probabalistic
                and incorrect with probability < (.25) ** num_witnesses
    """
    if number < 2:
        raise ValueError('Number should be at least 2')
    if number == 2:
        return 'prime'
    
    return miller_rabin_witnesses(number, _generate_witnesses(number, num_witnesses))

#=============================

def miller_rabin_cutoffs():
    return ((1, 2),
            (2047, 3),
            (1373653, 5),
            (25326001, 7),
            (3215031751, 11),
            (2152302898747, 13),
            (3474749660383, 17),
            (341550071728321, None))

#-----------------------------

def _generate_witnesses(number, num_witnesses):
    cutoffs = miller_rabin_cutoffs()
    
    if number > cutoffs[-1][0]:
        if num_witnesses > number:
            witnesses = set(x for x in range(2, number-1))
        else:
            witnesses = set()
            while len(witnesses) < num_witnesses:
                witnesses = witnesses | set([randint(2, number - 1)])

    else:
        witnesses = set(p for val, p in cutoffs[:-1] if number >= val)

    return witnesses

