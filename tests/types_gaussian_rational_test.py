#   tests/types_gaussian_rational.py
#===========================================================
import pytest
from hypothesis import assume, given, strategies as st

import env
from numth.basic import gcd
from numth.types import frac, Rational, Quadratic, QuadraticInteger
from numth.types.gaussian_rational import *
#===========================================================

@st.composite
def rational(draw, nonzero=False):
    numer = draw(st.integers())
    denom = draw(st.integers(min_value=1))
    if nonzero:
        assume( numer != 0 )
    return Rational(numer, denom)

@st.composite
def gaussian_rational(draw, nonzero=False):
    real = draw(st.integers())
    imag = draw(st.integers())
    if nonzero:
        assume( (real, imag) != (0, 0) )
    return GaussianRational(real, imag)

@st.composite
def gaussian_rational_pair(draw, nonzero=False):
    r1 = draw(st.integers())
    i1 = draw(st.integers())
    r2 = draw(st.integers())
    i2 = draw(st.integers())
    if nonzero:
        assume( (r1, i1) != (0, 0) )
        assume( (r2, i2) != (0, 0) )
    return (GaussianRational(r1, i1), GaussianRational(r2, i2))

@st.composite
def gaussian_rational_and_quadratic(draw, nonzero=False):
    r1 = draw(st.integers())
    i1 = draw(st.integers())
    r2 = draw(st.integers())
    i2 = draw(st.integers())
    if nonzero:
        assume( (r1, i1) != (0, 0) )
        assume( (r2, i2) != (0, 0) )
    return (GaussianRational(r1, i1), Quadratic(r2, i2, -1))

@st.composite
def gaussian_rational_and_quadratic_integer(draw, nonzero=False):
    r1 = draw(st.integers())
    i1 = draw(st.integers())
    r2 = draw(st.integers())
    i2 = draw(st.integers())
    if nonzero:
        assume( (r1, i1) != (0, 0) )
        assume( (r2, i2) != (0, 0) )
    return (GaussianRational(r1, i1), QuadraticInteger(r2, i2, -1))

#=============================

@given(gaussian_rational())
def test_to_quadratic(a):
    assert type(a.to_quadratic) is Quadratic
    assert a.to_quadratic == Quadratic(a.real, a.imag, a.root)
    assert a.to_quadratic == a

#=============================

@given(gaussian_rational_pair())
def test_eq(pair):
    a, b = pair
    assert a == a
    if a.components == b.components:
        assert a == b
    else:
        assert a != b

@given(gaussian_rational_and_quadratic_integer())
def test_eq_quadratic_integer(pair):
    a, b = pair
    if b.is_complex and a.components == b.components:
        assert a == b
    else:
        assert a != b

@given(gaussian_rational_and_quadratic())
def test_eq_quadratic(pair):
    a, b = pair
    if b.is_complex and a.components == b.components:
        assert a == b
    else:
        assert a != b

@given(gaussian_rational(), st.integers())
def test_eq_int(a, i):
    if a.imag == 0 and a.real == i:
        assert a == i
    else:
        assert a != i

@given(gaussian_rational(), rational())
def test_eq_Rational(a, r):
    if a.imag == 0 and a.real == r:
        assert a == r
    else:
        assert a != r

#=============================

@given(gaussian_rational())
def test_neg(a):
    assert type(-a) is GaussianRational
    assert -a == -(a.to_quadratic)

@given(gaussian_rational())
def test_norm_conjugate(a):
    assert type(a.conjugate) is GaussianRational
    assert type(a.norm) is Rational 
    assert a.conjugate == a.to_quadratic.conjugate
    assert a.norm == a.to_quadratic.norm

@given(gaussian_rational(nonzero=True))
def test_inverse(a):
    assert type(a.inverse) is GaussianRational 
    assert a.inverse == a.to_quadratic.inverse

@given(gaussian_rational())
def test_round(a):
    assert type(a.round) is GaussianRational
    assert a.round == a.to_quadratic.round

#=============================

@given(gaussian_rational())
def test_canonical(a):
    z = a.canonical
    assert z.real >= abs(z.imag)

#=============================

@given(gaussian_rational_pair())
def test_add(pair):
    a, b = pair
    assert type(a + b) is GaussianRational
    assert a + b == a.to_quadratic + b.to_quadratic

@given(gaussian_rational_and_quadratic_integer())
def test_add_QuadraticInteger(pair):
    a, b = pair
    assert type(a + b) is GaussianRational
    assert type(b + a) is GaussianRational
    assert a + b == a.to_quadratic + b
    assert b + a == b + a.to_quadratic

@given(gaussian_rational_and_quadratic())
def test_add_Quadratic(pair):
    a, b = pair
    assert type(a + b) is GaussianRational
    assert type(b + a) is GaussianRational
    assert a + b == a.to_quadratic + b
    assert b + a == b + a.to_quadratic

@given(gaussian_rational(), st.integers())
def test_add_int(a, b):
    assert type(a + b) is GaussianRational
    assert type(b + a) is GaussianRational
    assert a + b == a.to_quadratic + b
    assert b + a == b + a.to_quadratic

@given(gaussian_rational(), rational())
def test_add_Rational(a, b):
    assert type(a + b) is GaussianRational
    assert type(b + a) is GaussianRational
    assert a + b == a.to_quadratic + b
    assert b + a == b + a.to_quadratic

#=============================

@given(gaussian_rational_pair())
def test_sub(pair):
    a, b = pair
    assert type(a - b) is GaussianRational
    assert a - b == a.to_quadratic - b.to_quadratic

@given(gaussian_rational_and_quadratic_integer())
def test_sub_QuadraticInteger(pair):
    a, b = pair
    assert type(a - b) is GaussianRational
    assert type(b - a) is GaussianRational
    assert a - b == a.to_quadratic - b
    assert b - a == b - a.to_quadratic

@given(gaussian_rational_and_quadratic())
def test_sub_Quadratic(pair):
    a, b = pair
    assert type(a - b) is GaussianRational
    assert type(b - a) is GaussianRational
    assert a - b == a.to_quadratic - b
    assert b - a == b - a.to_quadratic

@given(gaussian_rational(), st.integers())
def test_sub_int(a, b):
    assert type(a - b) is GaussianRational
    assert type(b - a) is GaussianRational
    assert a - b == a.to_quadratic - b
    assert b - a == b - a.to_quadratic

@given(gaussian_rational(), rational())
def test_sub_Rational(a, b):
    assert type(a - b) is GaussianRational
    assert type(b - a) is GaussianRational
    assert a - b == a.to_quadratic - b
    assert b - a == b - a.to_quadratic

#=============================

@given(gaussian_rational_pair())
def test_mul(pair):
    a, b = pair
    assert type(a * b) is GaussianRational
    assert a * b == a.to_quadratic * b.to_quadratic

@given(gaussian_rational_and_quadratic_integer())
def test_mul_QuadraticInteger(pair):
    a, b = pair
    assert type(a * b) is GaussianRational
    assert type(b * a) is GaussianRational
    assert a * b == a.to_quadratic * b
    assert b * a == b * a.to_quadratic

@given(gaussian_rational_and_quadratic())
def test_mul_Quadratic(pair):
    a, b = pair
    assert type(a * b) is GaussianRational
    assert type(b * a) is GaussianRational
    assert a * b == a.to_quadratic * b
    assert b * a == b * a.to_quadratic

@given(gaussian_rational(), st.integers())
def test_mul_int(a, b):
    assert type(a * b) is GaussianRational
    assert type(b * a) is GaussianRational
    assert a * b == a.to_quadratic * b
    assert b * a == b * a.to_quadratic

@given(gaussian_rational(), rational())
def test_mul_Rational(a, b):
    assert type(a * b) is GaussianRational
    assert type(b * a) is GaussianRational
    assert a * b == a.to_quadratic * b
    assert b * a == b * a.to_quadratic

#=============================

@given(gaussian_rational_pair(nonzero=True))
def test_truediv(pair):
    a, b = pair
    assert type(a / b) is GaussianRational
    assert a / b == a.to_quadratic / b.to_quadratic

@given(gaussian_rational_and_quadratic_integer(nonzero=True))
def test_truediv_QuadraticInteger(pair):
    a, b = pair
    assert type(a / b) is GaussianRational
    assert type(b / a) is GaussianRational
    assert a / b == a.to_quadratic / b
    assert b / a == b / a.to_quadratic

@given(gaussian_rational_and_quadratic(nonzero=True))
def test_truediv_Quadratic(pair):
    a, b = pair
    assert type(a / b) is GaussianRational
    assert type(b / a) is GaussianRational
    assert a / b == a.to_quadratic / b
    assert b / a == b / a.to_quadratic

@given(gaussian_rational(nonzero=True), st.integers().filter(lambda x: x != 0))
def test_truediv_int(a, b):
    assert type(a / b) is GaussianRational
    assert type(b / a) is GaussianRational
    assert a / b == a.to_quadratic / b
    assert b / a == b / a.to_quadratic

@given(gaussian_rational(nonzero=True), rational(nonzero=True))
def test_truediv_Rational(a, b):
    assert type(a / b) is GaussianRational
    assert type(b / a) is GaussianRational
    assert a / b == a.to_quadratic / b
    assert b / a == b / a.to_quadratic

#=============================

@given(gaussian_rational_pair(nonzero=True))
def test_floordiv(pair):
    a, b = pair
    assert type(a // b) is GaussianRational
    assert a // b == a.to_quadratic // b.to_quadratic

@given(gaussian_rational_and_quadratic_integer(nonzero=True))
def test_floordiv_QuadraticInteger(pair):
    a, b = pair
    assert type(a // b) is GaussianRational
    assert type(b // a) is GaussianRational
    assert a // b == a.to_quadratic // b
    assert b // a == b // a.to_quadratic

@given(gaussian_rational_and_quadratic(nonzero=True))
def test_floordiv_Quadratic(pair):
    a, b = pair
    assert type(a // b) is GaussianRational
    assert type(b // a) is GaussianRational
    assert a // b == a.to_quadratic // b
    assert b // a == b // a.to_quadratic

@given(gaussian_rational(nonzero=True), st.integers().filter(lambda x: x != 0))
def test_floordiv_int(a, b):
    assert type(a // b) is GaussianRational
    assert type(b // a) is GaussianRational
    assert a // b == a.to_quadratic // b
    assert b // a == b // a.to_quadratic

@given(gaussian_rational(nonzero=True), rational(nonzero=True))
def test_floordiv_Rational(a, b):
    assert type(a // b) is GaussianRational
    assert type(b // a) is GaussianRational
    assert a // b == a.to_quadratic // b
    assert b // a == b // a.to_quadratic

#=============================

@given(gaussian_rational_pair(nonzero=True))
def test_mod(pair):
    a, b = pair
    assert type(a % b) is GaussianRational
    assert a % b == a.to_quadratic % b.to_quadratic

@given(gaussian_rational_and_quadratic_integer(nonzero=True))
def test_mod_QuadraticInteger(pair):
    a, b = pair
    assert type(a % b) is GaussianRational
    assert type(b % a) is GaussianRational
    assert a % b == a.to_quadratic % b
    assert b % a == b % a.to_quadratic

@given(gaussian_rational_and_quadratic(nonzero=True))
def test_mod_Quadratic(pair):
    a, b = pair
    assert type(a % b) is GaussianRational
    assert type(b % a) is GaussianRational
    assert a % b == a.to_quadratic % b
    assert b % a == b % a.to_quadratic

@given(gaussian_rational(nonzero=True), st.integers().filter(lambda x: x != 0))
def test_mod_int(a, b):
    assert type(a % b) is GaussianRational
    assert type(b % a) is GaussianRational
    assert a % b == a.to_quadratic % b
    assert b % a == b % a.to_quadratic

@given(gaussian_rational(nonzero=True), rational(nonzero=True))
def test_mod_Rational(a, b):
    assert type(a % b) is GaussianRational
    assert type(b % a) is GaussianRational
    assert a % b == a.to_quadratic % b
    assert b % a == b % a.to_quadratic

#=============================

@given(
    gaussian_rational(nonzero=True),
    st.integers(min_value=2, max_value=20)
)
def test_pow(a, m):
    mth_power = a**m
    mth_inverse = a**-m
    assert type(a**0) is GaussianRational
    assert type(a**1) is GaussianRational
    assert type(a**-1) is GaussianRational
    assert type(mth_power) is GaussianRational
    assert type(mth_inverse) is GaussianRational
    assert a**0 == 1
    assert a**1 == a
    assert a**-1 == a.inverse
    assert mth_power == a.to_quadratic**m
    assert mth_inverse == mth_power.inverse

@given(
    gaussian_rational(nonzero=True),
    st.integers(min_value=2, max_value=20),
    st.integers(min_value=2)
)
def test_pow_mod(a, exp, mod):
    power = a**exp
    mod_power = pow(a, exp, mod)
    assert type(power) is GaussianRational
    assert type(mod_power) is GaussianRational

#=============================

@given(gaussian_rational())
def test_rational_approx(a):
    if a.imag == 0:
        assert a.rational_approx(25) == a.real
    else:
        with pytest.raises(ValueError):
            a.rational_approx(25)
