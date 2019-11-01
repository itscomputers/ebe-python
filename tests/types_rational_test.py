#   tests/types_rational_test.py
#===========================================================
import env
import math
from fractions import Fraction
from hypothesis import given, strategies as st

from numth.types.rational import *
#===========================================================

@st.composite
def rational(draw, flag=None):
    if flag == 'nonzero':
        numer = draw(st.integers().filter(lambda x: x != 0))
    elif flag == 'positive':
        numer = draw(st.integers(min_value=0))
    else:
        numer = draw(st.integers())
    denom = draw(st.integers(min_value=1))
    return Rational(numer, denom)

#===========================================================

@given(rational())
def test_numer_and_denom(a):
    assert a.numer == a.numerator == a._numerator
    assert a.denom == a.denominator == a._denominator

#-----------------------------

@given(
    st.integers(),
    st.floats().filter(lambda x: not (math.isnan(x) or math.isinf(x))),
    rational()
)
def test_constructors(i, fl, a):
    assert int(Rational.from_int(i)) == int(frac(i)) == i
    assert int(Rational.from_str(str(i))) == int(frac(str(i))) == i
    assert float(Rational.from_float(fl)) == float(frac(fl)) == fl
    assert float(Rational.from_str(str(fl))) == float(frac(fl)) == fl

    f = Fraction(a.numer, a.denom)
    s1 = '{}/{}'.format(a.numer, a.denom)
    s2 = '{} / {}'.format(a.numer, a.denom)
    l = [a.numer, a.denom]
    t = (a.numer, a.denom)
    assert Rational.from_Rational(a) == frac(a) == a
    assert Rational.from_Fraction(f) == frac(f) == a
    assert Rational.from_str(s1) == frac(s1) == a
    assert Rational.from_str(s2) == frac(s2) == a
    assert Rational.from_list(l) == frac(l) == a
    assert Rational.from_tuple(t) == frac(t) == a

#-----------------------------

@given(st.integers(), st.integers(max_value=-1))
def test_negative_denominator(n, d):
    a = Rational(n, d)
    assert a.numer * n <= 0
    assert a.denom > 0

#=============================

def test_decimal():
    i = 12837465999
    a = Rational(i, 10000000000)
    expected = [
        '1',
        '1.3',
        '1.28',
        '1.284',
        '1.2837',
        '1.28375',
        '1.283747',
        '1.2837466',
        '1.28374660',
        '1.283746600',
        '1.2837465999',
        '1.28374659990'
    ]
    for digits, decimal in enumerate(expected):
        assert a.decimal(digits) == decimal
    for digits, decimal in enumerate(expected):
        assert (-a).decimal(digits) == '-{}'.format(decimal)

#=============================

@given(rational('nonzero'))
def test_inverse(a):
    assert type(a.inverse) is Rational
    assert a.inverse == Rational(a.denom, a.numer)
    assert a * a.inverse == 1

#-----------------------------

@given(rational())
def test_round_to_nearest_int(a):
    assert type(a.round_to_nearest_int) is int
    assert abs(a - a.round_to_nearest_int) <= Rational(1, 2)

#-----------------------------

@given(rational())
def test_is_square(a):
    assert (a**2).is_square

#=============================

@given(rational(), rational(), st.integers(min_value=0, max_value=30))
def test_approx_equal(a, b, num_digits):
    in_range = abs(a - b) < Rational(1, 10**num_digits)
    assert a.approx_equal(b, num_digits) == in_range

@given(rational(), st.integers(), st.integers(min_value=0, max_value=30))
def test_approx_equal_2(a, integer, num_digits):
    delta = Rational(integer, 10**(num_digits + 1))
    in_range = abs(delta) < Rational(1, 10**(num_digits))
    assert a.approx_equal(a + delta, num_digits) == in_range

#=============================

@given(rational('positive'), st.integers(min_value=10, max_value=20))
def test_sqrt(a, num_digits):
    s = a.sqrt(num_digits)
    assert type(s) is Rational
    lhs = 10**num_digits * abs(a - s**2)
    rhs = s + int(s) + 1

    assert lhs < rhs

#=============================

@given(rational())
def test_pos(a):
    assert type(+a) is Rational
    assert a == +a

#-----------------------------

@given(rational())
def test_neg(a):
    assert type(-a) is Rational
    assert (-a).numer == -(a.numer)
    assert (-a).denom == a.denom
    assert a == -(-a)

#-----------------------------

@given(rational())
def test_abs(a):
    assert type(abs(a)) is Rational
    if a < 0:
        assert abs(a) == -a
    else:
        assert abs(a) == a

#=============================

@given(st.integers(), rational(), rational())
def test_add(i, a, b):
    fa = Fraction(a.numer, a.denom)
    fb = Fraction(b.numer, b.denom)
    assert type(a + b) is Rational
    assert a + b == b + a == fa + fb
    assert type(a + fb) is Rational
    assert type(fb + a) is Rational
    assert a + fb == fb + a == fa + fb
    assert type(a + i) is Rational
    assert type(i + a) is Rational
    assert a + i == i + a == fa + i

@given(st.integers(), rational(), rational())
def test_sub(i, a, b):
    fa = Fraction(a.numer, a.denom)
    fb = Fraction(b.numer, b.denom)
    assert type(a - b) is Rational
    assert a - b == -(b - a) == -b + a == fa - fb
    assert type(a - fb) is Rational
    assert type(fb - a) is Rational
    assert a - fb == -(fb - a) == -fb + a == fa - fb
    assert type(a - i) is Rational
    assert type(i - a) is Rational
    assert a - i == -(i - a) == -i + a == fa - i

@given(st.integers(), rational(), rational())
def test_mul(i, a, b):
    fa = Fraction(a.numer, a.denom)
    fb = Fraction(b.numer, b.denom)
    assert type(a * b) is Rational
    assert a * b == b * a == fa * fb
    assert type(a * fb) is Rational
    assert type(fb * a) is Rational
    assert a * fb == fb * a == fa * fb
    assert type(a * i) is Rational
    assert type(i * a) is Rational
    assert a * i == i * a == fa * i

@given(
    st.integers().filter(lambda x: x != 0),
    rational('nonzero'),
    rational('nonzero')
)
def test_div(i, a, b):
    fa = Fraction(a.numer, a.denom)
    fb = Fraction(b.numer, b.denom)
    assert type(a / b) is Rational
    assert a / b == (b / a).inverse== 1/b * a == fa / fb
    assert type(a / fb) is Rational
    assert type(fb / a) is Rational
    assert a / fb == (fb / a).inverse == 1/fb * a == fa / fb
    assert type(a / i) is Rational
    assert type(i / a) is Rational
    assert a / i == (i / a).inverse == Rational(1, i) * a == fa / i

#=============================

@given(rational('nonzero'), st.integers(min_value=0, max_value=15))
def test_pow(a, e):
    a_e = a**e
    f = Fraction(a.numer, a.denom)
    f_e = f**e
    s = Rational(a.numer**e, a.denom**e)
    assert type(a_e) is Rational
    assert a_e == f_e
    assert a_e == s
    assert a**(-e) == s.inverse
    assert a**Rational(e, 1) == s
    assert a.numer**Rational(e, 1) == a.numer**e

