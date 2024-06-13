#   tests/modular_test.py
# ===========================================================
import env  # noqa
from hypothesis import given, strategies as st

from lib.basic import primes_up_to, jacobi
from lib.modular.sqrt import (
    mod_sqrt,
    mod_sqrt_minus_one_wilson,
    mod_sqrt_minus_one_legendre,
    mod_sqrt_tonelli_shanks,
    mod_sqrt_cipolla,
)

# ===========================================================

PRIMES = primes_up_to(500)


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
