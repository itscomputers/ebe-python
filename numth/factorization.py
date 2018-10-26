
#   numth/factorization.py

from numth.main import gcd, padic
from numth.primality import is_prime, primes_in_range
from numth.polynomial import polyn
from numth.rational import integer_sqrt
from numth.quadratic import gaussian, gaussian_divisor
from numth.quaternion import prime_as_norm

import math
from functools import reduce
from random import randint, shuffle
import itertools
import pebble
from concurrent.futures import ProcessPoolExecutor, TimeoutError, wait
import asyncio

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

    if pb is None:
        pb = _default_values('prime base')
    small_primes, num = trivial_divisors(num, pb)
    if num == 1:
        return sorted(small_primes)
    
    return sorted(small_primes + nontrivial_divisors(num, rs, rp, ms))

############################################################
############################################################
#       Factorization w/ multiprcoessing #1
############################################################
############################################################

def find_divisor_mp(num, rs=[], rp=[], ms=[], mw=4, to=None):
    """
    Find a divisor of a number using multiprocessing.
    
    Args:   int:    num, to, mw         to: timeout value
                                        mw: max workers
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
    with pebble.ProcessPool(max_workers=mw) as pool:
        for p, s in itertools.product(rp, rs):
            futures.append(pool.schedule( pollard_rho, (num, s, p) ))
        for s in ms:
            futures.append(pool.schedule( pollard_p_minus_one, (num, s) ))
        while d == num:
            wait(futures, timeout=to, return_when='FIRST_COMPLETED')
            for x in futures:
                if x.done():
                    if x.result() < num:
                        d = x.result()
                    futures.remove(x)
        if d < num:
            for x in futures:
                x.cancel()
    return d

##############################

def nontrivial_divisors_mp(num, rs=[], rp=[], ms=[], mw=4, to=None):
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
        primes = nontrivial_divisors_mp(sqrt, rs, rp, ms, mw, to)
        return 2*primes
    else:
        divisor = find_divisor_mp(num, rs, rp, ms, mw, to)
        primes = []
        for n in [divisor, num // divisor]:
            primes = primes + nontrivial_divisors_mp(n, rs, rp, ms, mw, to)
        
        return primes

##############################

def factor_mp(num, pb=None, rs=[], rp=[], ms=[], mw=4, to=None):
    if num < 2:
        return None
    if is_prime(num):
        return [num]

    if pb is None:
        pb = _default_values('prime base')
    small_primes, num = trivial_divisors(num, pb)
    if num == 1:
        return sorted(small_primes)

    return sorted(small_primes +\
            nontrivial_divisors_mp(num, rs, rp, ms, mw, to))

############################################################
############################################################
#       Factorization w/ multiprocessing #2
############################################################
############################################################

class PollardRho:

    def __init__(self, num, s, p):
        self.num = num
        self.s = s
        self.p = p
        self.interrupted = False

    def __repr__(self):
        return 'seed {}, polynomial {}'.format(self.s, self.p)

    def __call__(self):
        num = self.num
        s = self.s
        p = self.p
        def f(x):
            return polyn(p).mod_eval(x, num)
        xi = f(s % num)
        x2i = f(xi)
        d = gcd(x2i - xi, num)

        while d == 1:
            if self.interrupted:
                print('interrupted: {}'.format(self))
                break
            xi = f(xi)
            x2i = f( f(x2i) )
            d = gcd(x2i - xi, num)

        if d == 1:
            print('got interrupted')
            return num
        return d

    def interrupt(self):
        print('received interrupt call: {}'.format(self))
        self.interrupted = True

def find_divisor_mp2(num, rs=[], rp=[], to=None):
    from time import time
    d = num
    print(num)
    with ProcessPoolExecutor() as pool:
        tasks = [ PollardRho(num, s, p) for s, p in itertools.product(rs, rp) ]
        t0 = time()
        futures = [ pool.submit(x) for x in tasks ]
        done, not_done = wait(\
                futures, timeout=to, return_when='FIRST_COMPLETED')
        while len(not_done) > 0:
            t1 = time()
            print('elapsed {}, done = {}, not done = {}'\
                    .format(t1-t0, len(done), len(not_done)))
            for x in done:
                d = x.result()
                if d < num:
                    print('found one! {}'.format(d))
                    stop_process_pool(pool)
            done, not_done = wait(\
                not_done, timeout=to, return_when='FIRST_COMPLETED')
    return d

def test(d, rs, rp, to):
    from numth.primality import next_prime
    p = next_prime(randint(10**d, 10**(d+1)))
    q = next_prime(randint(10**d, 10**(d+1)))
    n = p * q
    return find_divisor_mp2(n, rs, rp, to)

############################################################
############################################################
#       Factorization w/ iterators
############################################################
############################################################

def rho_gen(num, s, p):
    def f(x):
        return polyn(p).mod_eval(x, num)
    xi = f(s % num)
    x2i = f(xi)
    while True:
        d = gcd(x2i - xi, num)
        yield d
        xi = f(xi)
        x2i = f( f(x2i) )

##############################

def p_minus_one_gen(num, s):
    if gcd(s, num) > 1:
        yield gcd(s, num)

    xi = s % num
    index = 1
    while True:
        d = gcd(xi - 1, num)
        yield d
        index += 1
        xi = pow(xi, index, num)

##############################

def find_divisor_w_gen(num, rs, rp, ms, extra=False):
    rg = [ [(s,p), rho_gen(num, s, p)] for s, p in itertools.product(rs, rp) ]
    mg = [ [s, p_minus_one_gen(num, s)] for s in ms ]
    gens = rg + mg
    d = 1
    if extra:
        i = 0
    while True:
        for seed, gen in gens:
            if extra:
                i += 1
            d = next(gen)
            if d > 1:
                if d == num:
                    gens.remove(gen)
                else:
                    if extra:
                        return i, seed, d 
                    return d

def get_num(d, r):
    from numth.primality import next_prime
    from functools import reduce
    from operator import mul
    primes = [ next_prime(randint(10**d, 10**(d+1))) for i in range(r) ]
    return reduce(mul, primes)

def find_good_seeds(d, r, k, rs, rp, ms):
    nums = [get_num(d, r) for j in range(k)]
    seeds = dict()
    
#   with ProcessPoolExecutor() as pool:
#       futures = []
#       for j in range(k):
#           futures.append(pool.submit( get_num, d, r ))
#       wait(futures)
#       for x in futures:
#           nums.append(x.result())

    with ProcessPoolExecutor() as pool:
        futures = []
        for n in nums:
            futures.append(pool.submit(find_divisor_w_gen, n, rs, rp, ms, True))
        wait(futures)
        for x in futures:
            i, s, d = x.result()
            if isinstance(s, int):
                s, p = s, tuple()
            else:
                s, p = s
            if s in seeds:
                seeds[s] = seeds[s] + (p, i)
            else:
                seeds[s] = (p, i)
    
    return seeds 

def seeds_to_check():
    rs = [2, 3, 4, 5, 6, 7, 8, 9]
    rp = [(1,0,1), (1,0,0,1), (1,0,0,0,1)]
    ms = [2]

    return rs, rp, ms





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
        self.multiplicity = self._multiplicity() 
        self.euler_phi = self._euler_phi()
        self.carmichael_lambda = self._carmichael_lambda()
        self.square_part = []
        self.square_free = []
        self.primes_one = []
        self.primes_three = []
        self.bad_primes = []
        self.is_sum_of_squares = True
        self.split_primes()
        
    ##########################

    def __repr__(self):
        """Print the factorization of num."""
        factors = []
        for prime, exp in sorted( self.multiplicity.items() ):
            if exp == 1:
                factors.append(str(prime))
            else:
                factors.append('{}^{}'.format(prime, exp))
        return ' * '.join(factors)

    ##########################

    def _multiplicity(self):
        """Find factorization of num with multiplicity."""
        return { prime : self.factorization.count(prime)\
                    for prime in sorted(set(self.factorization)) }

    ##########################

    def split_primes(self):
        """Split primes into classifications."""
        for p, e in self.multiplicity.items():
            if p == 2 or p % 4 == 1:
                self.primes_one += [p]*e
            else:
                if e % 2 == 1:
                    self.bad_primes += [p]*e
                    self.is_sum_of_squares = False
                else:
                    self.primes_three += [p]*(e//2)
            if e % 2 == 1:
                self.square_free.append(p)
            self.square_part += [p] * (e - (e % 2))

    ##########################

    def divisors(self):
        """Find all divisors of num."""
        divs = [1]
        for p in self.factorization:
            divs = divs + [ p * d for d in divs if p * d not in divs ]
        return sorted(divs)

    ##########################

    def _euler_phi(self):
        """Euler's phi function (totient)."""
        def e(pair):
            p, e = pair
            return p**(e-1) * (p - 1)
        def p(x, y):
            return x * y
        return reduce(p, map(e, self.multiplicity.items()), 1)

    ##########################

    def _carmichael_lambda(self):
        """Carmichael's lambda function."""
        result = 1
        for p, e in self.multiplicity.items():
            result *= (p-1) // gcd(result, p-1)
            if p == 2:
                if e == 2:
                    result *= p
                elif e > 2:
                    result *= p**(e-2)
            else:
                result *= p**(e-1)
        return result

    ##########################

    def two_squares(self, RANDOM=True):
        """Write number as sum of two squares."""
        if self.is_sum_of_squares:
            g = reduce(lambda x, y : x*y, self.primes_three, 1)
            g = gaussian(g, 0)
            for p in self.primes_one:
                d = gaussian_divisor(p)
                if RANDOM:
                    if randint(0,1) == 1:
                        d = d.conjugate()
                g = g * d
            g = g.canonical()
            return (g.real, abs(g.imag))

    ##########################

    def four_squares(self, RANDOM=True):
        """Write number as sum of four squares."""
        primes = self.factorization
        if RANDOM:
            shuffle(primes)
        quaternions = []
        for p in self.factorization:
            q = prime_as_norm(p)
            if RANDOM:
                q = q.shuffle()
            quaternions.append(q)
        q = reduce(lambda x, y : x*y, quaternions, 1)
        r, i, j, k = q.components
        return tuple(sorted([abs(r), abs(i), abs(j), abs(k)], reverse=True))

############################################################
############################################################
#       End
############################################################
############################################################
