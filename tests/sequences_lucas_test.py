#   tests/sequences_lucas_test.py
# ===========================================================
import env  # noqa
from hypothesis import given, strategies as st

from lib.types import QuadraticInteger, Quadratic, frac
from lib.sequences import LucasSequence

# ===========================================================
#   lucas sequence
# ===========================================================


@given(
    st.integers(min_value=0, max_value=100),
    st.integers(min_value=1),
    st.integers().filter(lambda x: x != 0),
)
def test_by_index(k, p, q):
    d = p**2 - 4 * q
    quadratic = Quadratic(frac(p, 2), frac(1, 2), d)
    kth_power = quadratic**k

    u = 2 * kth_power.imag
    v = 2 * kth_power.real

    seq = LucasSequence.at_index(k, p=p, q=q)
    assert seq.value.u == u
    assert seq.value.v == v
    assert seq.value.q == q**k


# -----------------------------


@given(
    st.integers(min_value=0, max_value=100),
    st.integers(min_value=1),
    st.integers().filter(lambda x: x != 0),
    st.integers(min_value=3),
)
def test_by_index_mod(k, p, q, mod):
    mod += 1 - mod % 2

    d = p**2 - 4 * q
    imag = (mod + 1) // 2
    real = (p * imag) % mod
    quadratic = QuadraticInteger(real, imag, d)
    kth_power = pow(quadratic, k, mod)

    u = (2 * kth_power.imag) % mod
    v = (2 * kth_power.real) % mod

    seq = LucasSequence.at_index(k, p=p, q=q, modulus=mod)
    assert seq.value.u == u
    assert seq.value.v == v
    assert seq.value.q == pow(q, k, mod)


# =============================


@given(
    st.integers(min_value=1),
    st.integers().filter(lambda x: x != 0),
)
def test_lucas_sequence(p, q):
    seq = LucasSequence(p=p, q=q)
    for k in range(100):
        value = LucasSequence.at_index(k, p=p, q=q).value
        assert seq.value == value
        next(seq)


# -----------------------------


@given(
    st.integers(min_value=1),
    st.integers().filter(lambda x: x != 0),
    st.integers(min_value=3),
)
def test_lucas_sequence_mod(p, q, mod):
    seq = LucasSequence(p=p, q=q, modulus=mod)
    for k in range(100):
        value = LucasSequence.at_index(k, p=p, q=q, modulus=mod).value
        assert seq.value == value
        next(seq)
