#   tests/modular_test.py
# ===========================================================
import env
from hypothesis import given, strategies as st

from lib.basic import gcd, primes_up_to, jacobi
from lib.factorization import factor, divisors
from lib.modular.multiplicative_functions import *
from lib.modular.sqrt import *

# ===========================================================

PRIMES = primes_up_to(500)

# ===========================================================
#   carmichael lambda and euler phi
# ===========================================================


@given(st.integers(min_value=3, max_value=10**4))
def test_euler_phi_and_carmichael_lambda(number):
    factorization = factor(number)
    euler = euler_phi(factorization)
    carmichael = carmichael_lambda(factorization)
    assert euler == euler_phi(number)
    assert carmichael == carmichael_lambda(number)

    mult_group = [x for x in range(1, number) if gcd(x, number) == 1]
    half_carmichael_powers = map(lambda x: pow(x, carmichael // 2, number), mult_group)
    carmichael_powers = map(lambda x: pow(x, carmichael, number), mult_group)

    assert len(mult_group) == euler
    assert set(half_carmichael_powers) != set([1])
    assert set(carmichael_powers) == set([1])


# -----------------------------


@given(st.integers(min_value=3, max_value=10**4))
def test_euler_phi_with_divisors(number):
    assert sum(map(euler_phi, divisors(number))) == number


# ===========================================================
#   sqrt
# ===========================================================


def test_sqrt_minus_one():
    for p in PRIMES:
        if p % 4 == 1:
            sqrts = set(mod_sqrt_minus_one_wilson(p))
            for s in sqrts:
                assert pow(s, 2, p) == p - 1
            assert set(mod_sqrt_minus_one_legendre(p)) == sqrts
            assert set(mod_sqrt_tonelli_shanks(-1, p)) == sqrts
            assert set(mod_sqrt_cipolla(-1, p)) == sqrts
            assert set(mod_sqrt(-1, p)) == sqrts


# -----------------------------


@given(st.integers())
def test_mod_sqrt(number):
    for p in PRIMES[1:]:
        if jacobi(number, p) == 1:
            sqrts = set(mod_sqrt_tonelli_shanks(number, p))
            for s in sqrts:
                assert pow(s, 2, p) == number % p
            assert set(mod_sqrt_cipolla(number, p)) == sqrts
            assert set(mod_sqrt(number, p)) == sqrts
