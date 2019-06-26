#   test_modular.py
#===========================================================
from hypothesis import given, assume, strategies as st

from ..basic import gcd, jacobi, lcm
from ..factorization import factor
from ..primality import primes_in_range 
from ..modular import *
#===========================================================

primes = primes_in_range(1, 500)

#=============================

def test_sqrt_minus_one():
    for p in primes:
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
    for p in primes[1:]:
        if jacobi(number, p) == 1:
            sqrts = set(mod_sqrt_tonelli_shanks(number, p))
            for s in sqrts:
                assert( pow(s, 2, p) == number % p )
            assert( set(mod_sqrt_cipolla(number, p)) == sqrts )
            assert( set(mod_sqrt(number, p)) == sqrts )

#=============================

@given(st.integers(min_value=2, max_value=10**4))
def test_euler_phi(number):
    phi = len([x for x in range(1, number) if gcd(x, number) == 1])
    assert( phi == euler_phi(number) )

    
@given(st.integers(min_value=2, max_value=10**4))
def test_carmichael_lambda(number):
    factorization = factor(number)
    carmichael = carmichael_lambda_from_factorization(factorization)
    individual_euler = {k : euler_phi(k**v) for k, v in factorization.items()}
    if 2 in factorization and factorization[2] > 2:
        individual_euler[2] //= 2
    assert( carmichael == lcm(*individual_euler.values()) )

