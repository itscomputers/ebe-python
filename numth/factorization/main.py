#   numth/factorization.py
#===========================================================
from collections import Counter 
from functools import reduce
from random import randint

from ..basic import integer_sqrt, padic
from ..primality import is_prime, next_prime, primes_in_range
from .algorithms import pollard_rho_gen, pollard_p_minus_one_gen
#===========================================================

def _default(key):
    return {
        'rho_seeds' : [2, 3, 4, 6, 7, 8, 9, randint(10, 10**5)],
        'minus_seeds' : [2],
        'prime_base' : primes_in_range(1, 1000)
    }[key]

#=============================

def find_divisor(number, rho_seeds=None, minus_seeds=None):
    """
    Find a divisor of a number.

    params
    + number : int
        composite number
    + rho_seeds : list
    + minus_seeds : list

    return
    set
        set of first divisors found using all given seeds
    """
    divisor_search = _divisor_search_generators(number, rho_seeds, minus_seeds)

    divisor_found = False
    while not divisor_found:
        divisor_search, divisor_found = \
            _advance_to_next(number, divisor_search, divisor_found)

    return {value['divisor'] for value in divisor_search.values() \
            if value['divisor'] != 1}

#=============================

def factor_trivial(number, prime_base=None):
    """
    Factor out the trivial primes.

    params
    + number : int
    + prime_base : list

    return
    + remaining : int
        number leftover after division by trivial primes
    + prime_divisors : dict
        prime divisors of number from prime base with multiplicity
    """
    prime_base = prime_base or _default('prime_base')
    remaining = number
    factorization = dict()
    for prime in prime_base:
        if remaining % prime == 0:
            exp, remaining = padic(remaining, prime)
            factorization = _combine_counters(factorization, {prime : exp})

    return remaining, factorization

#-----------------------------

def factor_nontrivial(
    number,
    rho_seeds=None,
    minus_seeds=None
):
    """
    Factor out the nontrivial primes.

    params
    + number : int
    + rho_seeds : list
    + minus_seeds : list

    return
    dict
        nontrivial prime divisors with multiplicity
    """
    if number == 1:
        return dict()

    if is_prime(number):
        return {number : 1}

    sqrt_number = integer_sqrt(number)
    if sqrt_number**2 == number:
        return _apply_multiplicity(factor_nontrivial(sqrt_number), 2)

    remaining = number
    factorization = dict()

    divisors = find_divisor(remaining, rho_seeds, minus_seeds)
    for d in divisors:
        exp, remaining = padic(remaining, d)
        factorization = _combine_counters(
            factorization,
            factor_nontrivial(d),
            exp
        )

    return _combine_counters(factorization, factor_nontrivial(remaining))

#-----------------------------

def factor(number, prime_base=None, rho_seeds=None, minus_seeds=None):
    """
    Factor number into its prime divisors with multiplicity.

    For example, ``{2 : 4, 3 : 1, 5 : 2}`` means ``2**4 * 3**1 * 5**2 == 1200``

    params
    + number : int
        number to factor
    + prime_base : list
        list of primes to factor by trial division
    + rho_seeds : list
        list of seeds to use in Pollard's rho algorithm
    + minus_seeds : list
        list of seeds to use in Pollard's p-1 algorithm

    return
    dict
        prime divisors of number with multiplicity
    """
    remaining, trivial_divisors = factor_trivial(number, prime_base)
    nontrivial_divisors = factor_nontrivial(remaining, rho_seeds, minus_seeds)

    return {**trivial_divisors, **nontrivial_divisors}

#=============================

def divisors_from_factorization(factorization):
    """
    Compute the divisors of a number using its factorization.

    params
    + factorization : dict
        prime divisors with multiplicity

    return
    list
    """
    divs = set([1])
    for p in Counter(factorization).elements():
        divs = divs | set(p * d for d in divs)
    return sorted(divs)

#-----------------------------

def divisors(number):
    """
    Compute the divisors of a number.

    params
    + number : int

    return
    list
    """
    return divisors_from_factorization(factor(number))

#=============================

def square_part(factorization):
    """
    Square part of a factorization.

    Computes factorization of largest square number that divides the number.

    params
    + factorization : dict
        prime divisors with multiplicity

    return
    dict
    """
    return {k : v - v % 2 for k, v in factorization.items() if v > 1}

#-----------------------------

def square_free_part(factorization):
    """
    Square free part of a factorization.

    Computes the factorization of a number divided by its square part.

    params
    + factorization : dict
        prime divisors with multiplicity

    return
    dict
    """
    return {k : 1 for k, v in factorization.items() if v % 2 == 1}

#=============================

def number_from_factorization(factorization):
    """
    Compute number from its factorization.
    
    params
    + factorization : dict
        prime divisors with multiplicty

    return
    int
        product of prime divisors
    """
    return reduce(lambda x, y: x * y, Counter(factorization).elements(), 1)

#===========================================================

def _divisor_search_generators(number, rho_seeds, minus_seeds):
    """
    Build generators to search for a divisor.

    params
    + number : int
    + rho_seeds : list
    + minus_seeds : list

    return
    dict
        * key is a tuple of the seed and the type of seed
        * value is a dict with key 'generator' and value the generator
    """
    divisor_search = dict()
    for seed in (rho_seeds or _default('rho_seeds')):
        divisor_search[(seed, 'rho')] = {
            'generator' : pollard_rho_gen(number, seed, lambda x: x**2 + 1)
        }
    for seed in (minus_seeds or _default('minus_seeds')):
        divisor_search[(seed, 'p-1')] = {
            'generator' : pollard_p_minus_one_gen(number, seed)
        }
    return divisor_search

#-----------------------------

def _advance_to_next(number, divisor_search, divisor_found):
    """
    Advance the divisor search to the next step.

    Transforms data as follows:
    ``
    { (seed, 'rho') : { 'generator' : gen, 'divisor' : d } }
        ->  { (seed, 'rho') : { 'generator' : gen, 'divisor' : next(gen) } }
    ``

    params
    + number : int
    + divisor_search : dict
    + divisor_found : bool

    return
    + divisor_search : dict
    + divisor_found : bool
    """
    for key in divisor_search:
        divisor = next(divisor_search[key]['generator'])
        if divisor == number:
            divisor_search[key]['generator'] = _trivial_generator()
        else:
            if divisor > 1:
                divisor_found = True
            divisor_search[key]['divisor'] = divisor
    return divisor_search, divisor_found

#=============================

def _combine_counters(counter_1, counter_2, m_2=1):
    """
    Combine two dictionaries with integer values to sum across keys.

    params
    + counter_1 : dict
    + counter_2 : dict
    + m_2 : int
        multiplicity to be applied to counter_2

    return
    dict
    """
    new_counter = _apply_multiplicity(counter_2, m_2)
    for k, v in counter_1.items():
        if k in new_counter:
            new_counter[k] += v
        else:
            new_counter[k] = v
    return new_counter

#-----------------------------

def _apply_multiplicity(counter, multiplicity):
    return {k : multiplicity * v for k, v in counter.items()}

#-----------------------------

def _trivial_generator():
    while True:
        yield 1

