#   numth/factorization/algorithms.py
#===========================================================
from ..basic import gcd
#===========================================================

def pollard_rho_gen(number, seed, func):
    """
    Generator for Pollard's rho algorithm.

    params
    + number : int
        composite number to be factored
    + seed : int
        initial seed for the sequence
    + func : function
        function of one variable for generating the sequence

    return
    generator -> int
    """
    x_i = func(seed % number)
    x_2i = func(x_i) % number
    
    while True:
        divisor = gcd(x_2i - x_i, number)
        yield divisor
        x_i = func(x_i) % number
        x_2i = func(func(x_2i) % number) % number

#-----------------------------

def pollard_rho(number, seed, func):
    """
    Pollard's rho algorithm to find a divisor.

    params
    + number : int
        composite number to be factored
    + seed : int
        initial seed for the sequence
    + func : function
        function of one variable for generating the sequence

    return
    divisor : int
        either a nontrivial divisor or the number itself
    """
    gen = pollard_rho_gen(number, seed, func)
    divisor = next(gen)

    while divisor == 1:
        divisor = next(gen)

    return divisor

#=============================

def pollard_p_minus_one_gen(number, seed):
    """
    Generator for Pollard's ``p - 1`` algorithm.

    params
    + number : int
        composite number to be factored
    + seed : int
        initial seed for the sequence

    return
    generator -> int
    """
    x_i = seed % number
    index = 1

    while True:
        divisor = gcd(x_i - 1, number)
        yield divisor
        index = index + 1
        x_i = pow(x_i, index, number)

#-----------------------------

def pollard_p_minus_one(number, seed):
    """
    Pollard's ``p - 1`` algorithm to find a divisor.

    params
    + number : int
        composite number to be factored
    + seed : int
        initial seed for the sequence

    return
    divisor : int
        either a nontrivial divisor or the number itself
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

def williams_p_plus_one(number, quadratic_seed):
    """
    Williams' ``p + 1`` algorithm to find a divisor.

    params
    + number : int
        composite number to be factored
    + quadratic_seed : Quadratic
        initial quadratic number seed for the sequence

    return
    divisor : int
        either a nontrivial divisor or the number itself
    """
    z = quadratic_seed
    divisor = gcd(z.norm, number)

    power = 1
    while divisor == 1:
        power = power + 1
        z = pow(z, power, number)
        divisor = gcd(z.imag, number)

    return divisor

