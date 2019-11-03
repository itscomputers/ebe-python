#   tests/continued_fraction_test.py
#===========================================================
import env
from hypothesis import assume, given, strategies as st

from numth.basic import is_square
from numth.types import Quadratic, frac
from numth.continued_fraction.quadratic import *
#===========================================================

@st.composite
def root(draw, max_value=None):
    return draw(st.integers(
        min_value=2,
        max_value=max_value
    ).filter(
        lambda x: not is_square(x)
    ))

#===========================================================

@given(
    st.integers(),
    st.integers(),
    st.integers(min_value=1),
    root(),
    st.integers()
)
def test_quadratic_rational_class(real, imag, denom, root, integer):
    assume( (real, imag) != (0, 0) )
    qr = QuadraticRational(real, imag, denom, root)
    q = Quadratic(frac(real, denom), frac(imag, denom), root)
    assert qr.to_quadratic == q
    assert qr == q
    assert qr.inverse == q.inverse
    assert qr - integer == q - integer

#-----------------------------

@given(root(max_value=10**6))
def test_continued_fractions(root):
    cf = QuadraticContinuedFraction(root, store_all=True)
    cf.advance_all()
    assert cf.period is not None

    assert len(cf.quotients) == cf.period + 1
    assert len(cf.convergents) == cf.period
    assert len(cf.pell_numbers) == cf.period
    assert len(cf.table) == cf.period + 1
    
    first_beta = cf.table[0][2]
    last_beta = cf.table[-1][2]
    assert first_beta == last_beta

    first_quotient, *other_quotients, last_quotient = cf.quotients
    assert 2 * first_quotient == last_quotient
    assert other_quotients == list(reversed(other_quotients))

    last_pell_number = cf.pell_numbers[-1]
    assert last_pell_number == 1 if cf.period % 2 == 0 else -1

    last_convergent = cf.convergents[-1]
    denom_log = len(str(last_convergent[-1]))
    approx_root = frac(cf.root).sqrt(2 * denom_log)
    assert frac(*last_convergent).approx_equal(approx_root, denom_log - 1)

#-----------------------------

@given(
    root(max_value=10**6),
    st.integers(min_value=1, max_value=30)
)
def test_continued_fractions_with_max(root, max_length):
    cf = QuadraticContinuedFraction(root, store_all=True)
    cf.advance_until(max_length)
    if cf.period is None:
        assert cf.step == max_length
    else:
        assert cf.step == cf.period
        assert cf.period <= max_length

    assert len(cf.quotients) == cf.step + 1
    assert len(cf.convergents) == cf.step
    assert len(cf.pell_numbers) == cf.step
    assert len(cf.table) == cf.step + 1

