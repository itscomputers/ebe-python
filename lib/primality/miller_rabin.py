#   numth/primality/miller_rabin.py
#===========================================================
from random import randint

from ..basic import padic
#===========================================================

def miller_rabin_witness(number, witness):
    """
    Miller-Rabin witness for primality.

    Determines if number is composite or probably prime according to a witness.

    params
    + number : int
    + witness : int

    return
    str
        * 'composite' is deterministic
        * 'probable prime' is probabilistic
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

    params
    + number : int
    + witnesses : iterable of int

    return
    str
        * 'composite' if any think number is composite (deterministic)
        * 'probable prime' if all think number is prime (probabalistic)
    """
    for witness in witnesses:
        if miller_rabin_witness(number, witness) == 'composite':
            return 'composite'

    return 'probable prime'

#-----------------------------

def miller_rabin_test(number, num_witnesses):
    """
    Miller-Rabin test for primality.

    Probabalistic primality test
    using Fermat's Little Theorem and Lagrange's Theorem.

    params
    + number : int
    + num_witnesses : int

    return
    str
        * 'composite' is deterministic
        * 'prime' is deterministic (and only occurs for number < 341550071728321
        * 'probable prime' is probabalistic and
        incorrect with probabilty < (1/4) ** num_witnesses
    """
    if number < 2:
        raise ValueError('Number should be at least 2')
    if number == 2:
        return 'prime'

    primality = miller_rabin_witnesses(number, _generate_witnesses(number, num_witnesses))
    if primality == 'probable prime' and number < miller_rabin_max_cutoff():
        return 'prime'
    return primality

#=============================

def miller_rabin_max_cutoff():
    return 341550071728321

#-----------------------------

def miller_rabin_cutoffs():
    return ((1, 2),
            (2047, 3),
            (1373653, 5),
            (25326001, 7),
            (3215031751, 11),
            (2152302898747, 13),
            (3474749660383, 17))

#-----------------------------

def _generate_witnesses(number, num_witnesses):
    if number > miller_rabin_max_cutoff():
        if num_witnesses > number:
            witnesses = set(x for x in range(2, number-1))
        else:
            witnesses = set()
            while len(witnesses) < num_witnesses:
                witnesses = witnesses | set([randint(2, number - 1)])

    else:
        witnesses = set(p for val, p in miller_rabin_cutoffs() if number >= val)

    return witnesses

