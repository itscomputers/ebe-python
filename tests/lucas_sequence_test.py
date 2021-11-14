#   tests/lucas_sequence_test.py
# ===========================================================
import env
from hypothesis import given, strategies as st

from lib.types import QuadraticInteger
from lib.lucas_sequence.modular import *

# ===========================================================
#   modular
# ===========================================================


@given(
    st.integers(min_value=0, max_value=100),
    st.integers(min_value=1),
    st.integers().filter(lambda x: x != 0),
    st.integers(min_value=3),
)
def test_by_index(k, P, Q, mod):
    mod += 1 - mod % 2

    D = P ** 2 - 4 * Q
    imag = ((mod + 1) // 2) % mod
    real = (P * imag) % mod
    q = QuadraticInteger(real, imag, D)
    kth_power = pow(q, k, mod)

    U = (2 * kth_power.imag) % mod
    V = (2 * kth_power.real) % mod

    assert (U, V, pow(Q, k, mod)) == lucas_mod_by_index(k, P, Q, mod)


# -----------------------------


@given(
    st.integers(min_value=1),
    st.integers().filter(lambda x: x != 0),
    st.integers(min_value=3),
)
def test_lucas_sequence(P, Q, mod):
    mod += 1 - mod % 2
    gen = lucas_mod_gen(P, Q, mod)
    for i in range(100):
        assert lucas_mod_by_index(i, P, Q, mod) == next(gen)
