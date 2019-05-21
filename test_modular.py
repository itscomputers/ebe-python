#   test_modular.py
#===========================================================
from hypothesis import given, assume, strategies as st

from numth.basic import jacobi
from numth.modular import *
#===========================================================

def primes():
    return [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41,
            43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

#=============================

def test_sqrt_minus_one():
    for p in primes():
        if p % 4 == 1:
            sqrts = set(mod_sqrt_minus_one_wilson(p))
            for s in sqrts:
                assert( pow(s, 2, p) == p - 1 )
            assert( set(mod_sqrt_minus_one_legendre(p)) == sqrts )
            assert( set(mod_sqrt_tonelli_shanks(-1, p)) == sqrts )
            assert( set(mod_sqrt_cipolla(-1, p)) == sqrts )
            assert( set(mod_sqrt(-1, p)) == sqrts )

#=============================

@given(st.integers())
def test_mod_sqrt(number):
    for p in primes()[1:]:
        if jacobi(number, p) == 1:
            sqrts = set(mod_sqrt_tonelli_shanks(number, p))
            for s in sqrts:
                assert( pow(s, 2, p) == number % p )
            assert( set(mod_sqrt_cipolla(number, p)) == sqrts )
            assert( set(mod_sqrt(number, p)) == sqrts )

