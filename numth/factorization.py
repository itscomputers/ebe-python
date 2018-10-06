
#   numth/factorization.py

import numth.numth as numth
import numth.primality as primality
import numth.polynomial as polynomial
import numth.rational as rational

import math
from random import randint
import itertools
from concurrent.futures import TimeoutError, wait
import pebble

##############################

def _default_values(cat):
    if cat == 'small primes bound':
        return 100
    if cat == 'rho seeds':
        return [2, 3] + [ randint(4,10**10) for j in range(2) ]
    if cat == 'rho polyns':
        return [(1,0,1), (1,0,0,0,1)]
    if cat == 'p-1 seeds':
        return [2, 3] + [ randint(4,10**10) for j in range(2) ]
    if cat == 'divisor timeout':
        return 1
    if cat == 'prime base':
        return primality.primes_in_range(2,1000)

##############################

def find_divisor(num, rs=[], rp=[], ms=[], mp=False):
    """Find a divisor of a number."""
    if rs == []:
        rs = _default_values('rho seeds')
    if rp == []:
        rp = _default_values('rho polyns')
    if ms == []:
        ms = _default_values('p-1 seeds')

    if not mp:
        for s, p in itertools.product(rs, rp):
            d = pollard_rho(num, s, p)
            if d < num:
                return d
        for s in ms:
            d = pollard_p_minus_one(num, s)
            if d < num:
                return d
    else:
        futures = []
        divisor = num
        with pebble.ProcessPool() as pool:
            for s, p in itertools.product(rs, rp):
                futures.append(pool.schedule( pollard_rho, (num, s, p) ))
            for s in ms:
                futures.append(pool.schedule( pollard_p_minus_one, (num, s) ))
            while divisor == num:
                wait(futures, return_when='FIRST_COMPLETED')
                for x in futures:
                    if x.done():
                        divisor = x.result()
                        if divisor == num:
                            futures.remove(x)
            for x in futures:
                x.cancel()
        return divisor

##############################

def trivial_divisors(num, prime_base):
    """Find prime divisors of a number up to a given bound."""
    primes = []
    for p in prime_base:
        if num % p == 0:
            exp, num = numth.padic(num, p)
            primes = primes + [p] * exp
    
    return primes, num

##############################

def nontrivial_divisors(num, rs=[], rp=[], ms=[]):
    """Find nontrivial prime divisors of a number."""
    if primality.is_prime(num):
        return [num]
    sqrt = rational.integer_sqrt(num)
    if sqrt**2 == num:
        primes = nontrivial_divisors(sqrt, rs, rp, ms)
        return 2*primes
    else:
        divisor = find_divisor(num, rs, rp, ms)
        primes = []
        for n in [divisor, num // divisor]:
            primes = primes + nontrivial_divisors(n, rs, rp, ms)
        
        return primes

##############################

def factor(num, prime_base=None, rs=[], rp=[], ms=[]):
    """Factor a number into prime divisors."""
    if num < 2:
        return None
    if primality.is_prime(num):
        return [num]

    if prime_base is None:
        prime_base = _default_values('prime base')
    small_primes, num = trivial_divisors(num, prime_base)
    if num == 1:
        return sorted(small_primes)
    
    return sorted(small_primes + nontrivial_divisors(num, rs, rp, ms))



    




############################################################
#       Pollard's rho algorithm
############################################################

def pollard_rho(num, seed, polyn):
    """Pollard's rho algorithm for factor-finding."""
    if not isinstance(polyn, polynomial.Polynomial):
        polyn = polynomial.polyn(polyn)
    def f(x):
        return polyn.mod_eval(x, num)
    xi = f(seed % num)
    x2i = f(xi)
    d = numth.gcd(x2i - xi, num)

    while d == 1:
        xi = f(xi)
        x2i = f( f(x2i) )
        d = numth.gcd(x2i - xi, num)

    return d

############################################################
#       Pollard's p-1 algorithm
############################################################

def pollard_p_minus_one(num, seed):
    """Pollard's p-1 algorithm for factor-finding."""
    d = numth.gcd(num, seed)
    if d > 1:
        return d

    xi = seed % num
    d = numth.gcd(xi - 1, num)
    index = 1

    while d == 1:
        index += 1
        xi = pow(xi, index, num)
        d = numth.gcd(xi - 1, num)

    return d

############################################################
#       Williams' p+1 algorithm
############################################################

def williams_p_plus_one(num, quad_int):
    """William's p+1 algorithm for factor-finding."""

    ### NEED A QUADRATIC INTEGER CLASS

    return None

############################################################
#       Rational quadratic sieve
############################################################

def add(v1, v2):
    """Add two arrays modulo 2"""
    return [ b1 ^ b2 for b1, b2 in zip(v1, v2) ]

##############################

def append_new_row(new_row, nums):
    """
    Append a new dict to a list of dicts.
    
    This is for finding relations among the exponent vectors.
    """
    num, vector = new_row
    relation = [0] * len(nums)
    reduced = list(vector)
    
    nums_copy = [row for row in nums]
    for row in nums_copy:
        if row['pivot'] is not None and vector[row['pivot']] == 1:
            reduced = add(reduced, row['reduced'])
            relation = add(relation, row['relation'])
    relation.append(1)

    try:
        pivot = reduced.index(1)
    except ValueError:
        pivot = None

    for row in nums_copy:
        row['relation'].append(0)
        if pivot is not None\
                and row['pivot'] is not None\
                and row['pivot'] < pivot\
                and row['reduced'][pivot] == 1:
            row['relation'] = add(row['relation'], relation)
            row['reduced'] = add(row['reduced'], reduced)
    
    nums_copy.append({
        'number'    :   num,
        'vector'    :   vector,
        'reduced'   :   reduced,
        'pivot'     :   pivot,
        'relation'  :   relation,
    })

    return nums_copy

##############################




