#   tests/types_gaussian_integer_test.py
#===========================================================
import pytest
from hypothesis import assume, given, strategies as st

import env
from numth.basic import gcd
from numth.types import frac, Rational, Quadratic, QuadraticInteger
from numth.types.gaussian_integer import *
#===========================================================

@st.composite
def rational(draw, nonzero=False):
    numer = draw(st.integers())
    denom = draw(st.integers(min_value=1))
    if nonzero:
        assume( numer != 0 )
    return Rational(numer, denom)

@st.composite
def gaussian_integer(draw, nonzero=False):
    real = draw(st.integers())
    imag = draw(st.integers())
    if nonzero:
        assume( (real, imag) != (0, 0) )
    return GaussianInteger(real, imag)

@st.composite
def gaussian_integer_pair(draw, nonzero=False):
    r1 = draw(st.integers())
    i1 = draw(st.integers())
    r2 = draw(st.integers())
    i2 = draw(st.integers())
    if nonzero:
        assume( (r1, i1) != (0, 0) )
        assume( (r2, i2) != (0, 0) )
    return (GaussianInteger(r1, i1), GaussianInteger(r2, i2))

@st.composite
def gaussian_integer_and_quadratic(draw, nonzero=False):
    r1 = draw(st.integers())
    i1 = draw(st.integers())
    r2 = draw(st.integers())
    i2 = draw(st.integers())
    if nonzero:
        assume( (r1, i1) != (0, 0) )
        assume( (r2, i2) != (0, 0) )
    return (GaussianInteger(r1, i1), Quadratic(r2, i2, -1))

@st.composite
def gaussian_integer_and_quadratic_integer(draw, nonzero=False):
    r1 = draw(st.integers())
    i1 = draw(st.integers())
    r2 = draw(st.integers())
    i2 = draw(st.integers())
    if nonzero:
        assume( (r1, i1) != (0, 0) )
        assume( (r2, i2) != (0, 0) )
    return (GaussianInteger(r1, i1), QuadraticInteger(r2, i2, -1))

#=============================

@given(gaussian_integer(), st.integers(), st.integers())
def test_from_components(a, real, imag):
    new = a.from_components(real, imag)
    assert type(new) is GaussianInteger
    assert new.real == real
    assert new.imag == imag

@given(gaussian_integer())
def test_to_quadratic_integer(a):
    assert type(a.to_quadratic_integer) is QuadraticInteger
    assert a.to_quadratic_integer == QuadraticInteger(a.real, a.imag, a.root)
    assert a.to_quadratic_integer == a

@given(gaussian_integer())
def test_to_quadratic(a):
    assert type(a.to_quadratic) is Quadratic
    assert a.to_quadratic == Quadratic(a.real, a.imag, a.root)
    assert a.to_quadratic == a

#=============================

@given(gaussian_integer_pair())
def test_eq(pair):
    a, b = pair
    assert a == a
    if a.components == b.components:
        assert a == b
    else:
        assert a != b

@given(gaussian_integer_and_quadratic_integer())
def test_eq_quadratic_integer(pair):
    a, b = pair
    if b.is_complex and a.components == b.components:
        assert a == b
    else:
        assert a != b

@given(gaussian_integer_and_quadratic())
def test_eq_quadratic(pair):
    a, b = pair
    if b.is_complex and a.components == b.components:
        assert a == b
    else:
        assert a != b

@given(gaussian_integer(), st.integers())
def test_eq_int(a, i):
    if a.imag == 0 and a.real == i:
        assert a == i
    else:
        assert a != i

@given(gaussian_integer(), rational())
def test_eq_Rational(a, r):
    if a.imag == 0 and a.real == r:
        assert a == r
    else:
        assert a != r

#=============================

@given(gaussian_integer())
def test_neg(a):
    assert type(-a) is GaussianInteger
    assert -a == -(a.to_quadratic_integer)
    
@given(gaussian_integer())
def test_norm_conjugate(a):
    assert type(a.conjugate) is GaussianInteger
    assert type(a.norm) is int
    assert a.conjugate == a.to_quadratic_integer.conjugate
    assert a.norm == a.to_quadratic_integer.norm

@given(gaussian_integer(nonzero=True))
def test_inverse(a):
    assert type(a.inverse) is Quadratic
    assert a.inverse == a.to_quadratic_integer.inverse

@given(gaussian_integer())
def test_round(a):
    assert type(a.round) is GaussianInteger
    assert a.round == a.to_quadratic_integer.round

@given(gaussian_integer(), st.integers(min_value=2))
def test_mod_inverse(a, i):
    if gcd(a.norm, i) > 1:
        with pytest.raises(ValueError):
            a.mod_inverse(i)
    else:
        assert type(a.mod_inverse(i)) is GaussianInteger
        assert (a * a.mod_inverse(i)) % i == 1

#=============================

@given(gaussian_integer())
def test_canonical(a):
    z = a.canonical
    assert z.real >= abs(z.imag)

@given(gaussian_integer_pair(nonzero=True))
def test_gcd(pair):
    a, b = pair
    z = a.gcd(b)
    assert a % z == b % z == 0
    assert (a // z).gcd(b // z) == 1

#=============================

@given(gaussian_integer_pair())
def test_add(pair):
    a, b = pair
    assert type(a + b) is GaussianInteger
    assert a + b == a.to_quadratic_integer + b.to_quadratic_integer

@given(gaussian_integer_and_quadratic_integer())
def test_add_QuadraticInteger(pair):
    a, b = pair
    assert type(a + b) is GaussianInteger
    assert type(b + a) is GaussianInteger
    assert a + b == a.to_quadratic_integer + b
    assert b + a == b + a.to_quadratic_integer

@given(gaussian_integer_and_quadratic())
def test_add_Quadratic(pair):
    a, b = pair
    assert type(a + b) is Quadratic 
    assert type(b + a) is Quadratic
    assert a + b == a.to_quadratic + b
    assert b + a == b + a.to_quadratic

@given(gaussian_integer(), st.integers())
def test_add_int(a, i):
    assert type(a + i) is GaussianInteger
    assert type(i + a) is GaussianInteger
    assert a + i == a.to_quadratic + i
    assert i + a == i + a.to_quadratic

@given(gaussian_integer(), rational())
def test_add_Rational(a, r):
    assert type(a + r) is Quadratic 
    assert type(r + a) is Quadratic
    assert a + r == a.to_quadratic + r
    assert r + a == r + a.to_quadratic

#=============================

@given(gaussian_integer_pair())
def test_sub(pair):
    a, b = pair
    assert type(a - b) is GaussianInteger
    assert a - b == a.to_quadratic_integer - b.to_quadratic_integer

@given(gaussian_integer_and_quadratic_integer())
def test_sub_QuadraticInteger(pair):
    a, b = pair
    assert type(a - b) is GaussianInteger
    assert type(b - a) is GaussianInteger
    assert a - b == a.to_quadratic_integer - b
    assert b - a == b - a.to_quadratic_integer

@given(gaussian_integer_and_quadratic())
def test_sub_Quadratic(pair):
    a, b = pair
    assert type(a - b) is Quadratic 
    assert type(b - a) is Quadratic
    assert a - b == a.to_quadratic - b
    assert b - a == b - a.to_quadratic

@given(gaussian_integer(), st.integers())
def test_sub_int(a, i):
    assert type(a - i) is GaussianInteger
    assert type(i - a) is GaussianInteger
    assert a - i == a.to_quadratic - i
    assert i - a == i - a.to_quadratic

@given(gaussian_integer(), rational())
def test_sub_Rational(a, r):
    assert type(a - r) is Quadratic 
    assert type(r - a) is Quadratic
    assert a - r == a.to_quadratic - r
    assert r - a == r - a.to_quadratic

#=============================

@given(gaussian_integer_pair())
def test_mul(pair):
    a, b = pair
    assert type(a * b) is GaussianInteger
    assert a * b == a.to_quadratic_integer * b.to_quadratic_integer

@given(gaussian_integer_and_quadratic_integer())
def test_mul_QuadraticInteger(pair):
    a, b = pair
    assert type(a * b) is GaussianInteger
    assert type(b * a) is GaussianInteger
    assert a * b == a.to_quadratic_integer * b
    assert b * a == b * a.to_quadratic_integer

@given(gaussian_integer_and_quadratic())
def test_mul_Quadratic(pair):
    a, b = pair
    assert type(a * b) is Quadratic 
    assert type(b * a) is Quadratic
    assert a * b == a.to_quadratic * b
    assert b * a == b * a.to_quadratic

@given(gaussian_integer(), st.integers())
def test_mul_int(a, i):
    assert type(a * i) is GaussianInteger
    assert type(i * a) is GaussianInteger
    assert a * i == a.to_quadratic * i
    assert i * a == i * a.to_quadratic

@given(gaussian_integer(), rational())
def test_mul_Rational(a, r):
    assert type(a * r) is Quadratic 
    assert type(r * a) is Quadratic
    assert a * r == a.to_quadratic * r
    assert r * a == r * a.to_quadratic

#=============================

@given(gaussian_integer_pair(nonzero=True))
def test_truediv(pair):
    a, b = pair
    assert type(a / b) is Quadratic 
    assert a / b == a.to_quadratic_integer / b.to_quadratic_integer

@given(gaussian_integer_and_quadratic_integer(nonzero=True))
def test_truediv_QuadraticInteger(pair):
    a, b = pair
    assert type(a / b) is Quadratic 
    assert type(b / a) is Quadratic
    assert a / b == a.to_quadratic_integer / b
    assert b / a == b / a.to_quadratic_integer

@given(gaussian_integer_and_quadratic(nonzero=True))
def test_truediv_Quadratic(pair):
    a, b = pair
    assert type(a / b) is Quadratic 
    assert type(b / a) is Quadratic
    assert a / b == a.to_quadratic / b
    assert b / a == b / a.to_quadratic

@given(gaussian_integer(nonzero=True), st.integers().filter(lambda x: x != 0))
def test_truediv_int(a, i):
    assert type(a / i) is Quadratic
    assert type(i / a) is Quadratic
    assert a / i == a.to_quadratic / i
    assert i / a == i / a.to_quadratic

@given(gaussian_integer(nonzero=True), rational(nonzero=True))
def test_truediv_Rational(a, r):
    assert type(a / r) is Quadratic 
    assert type(r / a) is Quadratic
    assert a / r == a.to_quadratic / r
    assert r / a == r / a.to_quadratic

#=============================

@given(gaussian_integer_pair(nonzero=True))
def test_floordiv(pair):
    a, b = pair
    assert type(a // b) is GaussianInteger
    assert a // b == a.to_quadratic_integer // b.to_quadratic_integer

@given(gaussian_integer_and_quadratic_integer(nonzero=True))
def test_floordiv_QuadraticInteger(pair):
    a, b = pair
    assert type(a // b) is GaussianInteger
    assert type(b // a) is GaussianInteger
    assert a // b == a.to_quadratic_integer // b
    assert b // a == b // a.to_quadratic_integer

@given(gaussian_integer_and_quadratic(nonzero=True))
def test_floordiv_Quadratic(pair):
    a, b = pair
    assert type(a // b) is GaussianInteger 
    assert type(b // a) is GaussianInteger
    assert a // b == a.to_quadratic // b
    assert b // a == b // a.to_quadratic

@given(gaussian_integer(nonzero=True), st.integers().filter(lambda x: x != 0))
def test_floordiv_int(a, i):
    assert type(a // i) is GaussianInteger
    assert type(i // a) is GaussianInteger
    assert a // i == a.to_quadratic // i
    assert i // a == i // a.to_quadratic

@given(gaussian_integer(nonzero=True), rational(nonzero=True))
def test_floordiv_Rational(a, r):
    assert type(a // r) is GaussianInteger
    assert type(r // a) is GaussianInteger
    assert a // r == a.to_quadratic // r
    assert r // a == r // a.to_quadratic

#=============================

@given(gaussian_integer_pair(nonzero=True))
def test_mod(pair):
    a, b = pair
    assert type(a % b) is GaussianInteger
    assert a % b == a.to_quadratic_integer % b.to_quadratic_integer

@given(gaussian_integer_and_quadratic_integer(nonzero=True))
def test_mod_QuadraticInteger(pair):
    a, b = pair
    assert type(a % b) is GaussianInteger
    assert type(b % a) is GaussianInteger
    assert a % b == a.to_quadratic_integer % b
    assert b % a == b % a.to_quadratic_integer

@given(gaussian_integer_and_quadratic(nonzero=True))
def test_mod_Quadratic(pair):
    a, b = pair
    assert type(a % b) is Quadratic 
    assert type(b % a) is Quadratic
    assert a % b == a.to_quadratic % b
    assert b % a == b % a.to_quadratic

@given(gaussian_integer(nonzero=True), st.integers().filter(lambda x: x != 0))
def test_mod_int(a, i):
    assert type(a % i) is GaussianInteger
    assert type(i % a) is GaussianInteger
    assert a % i == a.to_quadratic % i
    assert i % a == i % a.to_quadratic

@given(gaussian_integer(nonzero=True), rational(nonzero=True))
def test_mod_Rational(a, r):
    assert type(a % r) is Quadratic
    assert type(r % a) is Quadratic
    assert a % r == a.to_quadratic % r
    assert r % a == r % a.to_quadratic

#=============================

@given(
    gaussian_integer(nonzero=True),
    st.integers(min_value=2, max_value=20)
)
def test_pow(a, m):
    assert type(a**0) is GaussianInteger
    assert type(a**1) is GaussianInteger
    assert type(a**-1) is Quadratic
    assert type(a**m) is GaussianInteger
    assert type(a**-m) is Quadratic
    assert a**0 == 1
    assert a**1 == a
    assert a**-1 == a.inverse
    assert a**m == a.to_quadratic_integer**m
    assert a**-m == (a**m).inverse

#=============================

@given(gaussian_integer())
def test_rational_approx(a):
    if a.imag == 0:
        assert a.rational_approx(25) == a.real
    else:
        with pytest.raises(ValueError):
            a.rational_approx(25)
