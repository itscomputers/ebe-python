
#   numth/factorization.py

from numth.main import gcd, padic
from numth.primality import is_prime
from numth.polynomial import polyn
from numth.rational import integer_sqrt

import math
from random import randint
import itertools
import pebble
from concurrent.futures import wait

##############################

def _default_values(cat):
    if cat == 'rho seeds':
        return [2, 3] + [ randint(4,10**10) for j in range(2) ]
    if cat == 'rho polyns':
        return [(1,0,1), (1,0,0,0,1)]
    if cat == 'p-1 seeds':
        return [2, 3] + [ randint(4,10**10) for j in range(2) ]
    if cat == 'prime base':
        return primes_in_range(2,1000)

############################################################
############################################################
#       Total Factorization
############################################################
############################################################

def find_divisor(num, rs=[], rp=[], ms=[]):
    """
    Find a divisor of a number.
    
    Args:   int:    num
            list:   rs          seeds for pollard_rho
                    rp          polynomials for pollard_rho
                    ms          seeds for pollard_p_minus_one

    Return: int:    divisor of num
    """
    if rs == []:
        rs = _default_values('rho seeds')
    if rp == []:
        rp = _default_values('rho polyns')
    if ms == []:
        ms = _default_values('p-1 seeds')

    for p, s in itertools.product(rp, rs):
        d = pollard_rho(num, s, p)
        if d < num:
            return d
    for s in ms:
        d = pollard_p_minus_one(num, s)
        if d < num:
            return d

##############################

def trivial_divisors(num, pb):
    """
    Find prime divisors of a number from a prime base.
    
    Args:   int:    num
            list:   pb          prime base

    Return: list:   primes      prime divisors of num from pb
            int:    rest        leftover after dividing num by prime divisors
    """
    primes = []
    rest = num
    for p in pb:
        if rest % p == 0:
            exp, rest = padic(rest, p)
            primes = primes + [p] * exp
    
    return primes, rest

##############################

def nontrivial_divisors(num, rs=[], rp=[], ms=[]):
    """
    Find nontrivial prime divisors of a number.

    Args:   int:    num
            list:   rs, rp, ms

    Return: list:   primes      prime divisors of num
    """
    if is_prime(num):
        return [num]
    sqrt = integer_sqrt(num)
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

def factor(num, pb=None, rs=[], rp=[], ms=[]):
    """
    Factor a number into prime divisors.
    
    Args:   int:    num
            list:   pb, rs, rp, ms

    Return: list:   primes      prime divisors of num, sorted
    """
    if num < 2:
        return None
    if is_prime(num):
        return [num]

    if prime_base is None:
        prime_base = _default_values('prime base')
    small_primes, num = trivial_divisors(num, prime_base)
    if num == 1:
        return sorted(small_primes)
    
    return sorted(small_primes + nontrivial_divisors(num, rs, rp, ms))

##############################

def find_divisor_mp(num, rs=[], rp=[], ms=[], to=None):
    """
    Find a divisor of a number using multiprocessing.
    
    Args:   int:    num, to         to: timeout value
            list:   rs, rp, ms

    Return: int:    divisor of num or num itself if timeout occurs
    """
    if rs == []:
        rs = _default_values('rho seeds')
    if rp == []:
        rp = _default_values('rho polyns')
    if ms == []:
        ms = _default_values('p-1 seeds')

    d = num
    futures = []
    with pebble.ProcessPool() as pool:
        for p, s in itertools.product(rp, rs):
            futures.append(pool.schedule( find_divisor, (num, rs, rp, ms) ))
        wait(futures, timeout=to, return_when='FIRST_COMPLETED')
        for x in futures:
            if x.done() and x.result() < num:
                d = x.result()
            else:
                x.cancel()
    return d

############################################################
############################################################
#       Pollard's rho algorithm
############################################################
############################################################

def pollard_rho(num, s, p):
    """
    Pollard's rho algorithm for factor-finding.
    
    Args:   int:        num, s          s: initial value of sequence
            list/tuple: p               polynomial used to determine sequence
                                        eg. (1,2,0,3) represents the
                                        polynomial 1 + 2*x + 3*x^3

    Return: int:        divisor of num or num itself
    """
    def f(x):
        return polyn(p).mod_eval(x, num)
    xi = f(s % num)
    x2i = f(xi)
    d = gcd(x2i - xi, num)

    while d == 1:
        xi = f(xi)
        x2i = f( f(x2i) )
        d = gcd(x2i - xi, num)

    return d

############################################################
############################################################
#       Pollard's p-1 algorithm
############################################################
############################################################

def pollard_p_minus_one(num, seed):
    """
    Pollard's p-1 algorithm for factor-finding.
    
    Args:   int:    num, seed       seed: initial value of sequence

    Return: int:    divisor of num, or num itself
    """
    d = gcd(num, seed)
    if d > 1:
        return d

    xi = seed % num
    d = gcd(xi - 1, num)
    index = 1

    while d == 1:
        index += 1
        xi = pow(xi, index, num)
        d = gcd(xi - 1, num)

    return d

############################################################
############################################################
#       Williams' p+1 algorithm
############################################################
############################################################

def williams_p_plus_one(num, quad_int):
    """William's p+1 algorithm for factor-finding."""

    ### NEED A QUADRATIC INTEGER CLASS

    return None

############################################################
############################################################
#       Rational quadratic sieve
############################################################
############################################################

def add(v1, v2):
    """Add two arrays modulo 2."""
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

############################################################
############################################################
#       Factorize class
############################################################
############################################################

class Factorize:
    """Factorize class."""

    def __init__(self, num):
        """Initialize with number."""
        self.num = num
        self.factorization = factor(num)

    ##########################

    def __repr__(self):
        """Print the factorization of num."""
        factors = []
        for prime, exp in sorted( self.multiplicity().items() ):
            if exp == 1:
                factors.append(str(prime))
            else:
                factors.append('{}^{}'.format(prime, exp))
        return ' * '.join(factors)

    ##########################

    def multiplicity(self):
        """Find factorization of num with multiplicity."""
        return { prime : self.factorization.count(prime)\
                    for prime in sorted(set(self.factorization)) }

    ##########################

    def divisors(self):
        """Find all divisors of num."""
        divs = [1]
        for p in self.factorization:
            divs = divs + [ p * d for d in divs if p * d not in divs ]
        return sorted(divs)

    ##########################

    def euler_phi(self):
        output = 1
        for p, e in self.multiplicity().items():
            ouput *= (p-1)
            for i in range(e-1):
                output *= p
        return output

    ##########################

    def carmichael_lambda(self):
        output = 1
        for p, e in self.multiplicity().items():
            output *= (p-1) // gcd(output, p-1)
            if p == 2:
                if e == 2:
                    output *= p
                elif e > 2:
                    output *= p**(e-2)
            else:
                result *= p**(e-1)
        return result

    ##########################
