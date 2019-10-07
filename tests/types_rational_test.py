#   tests/types_rational_test.py
#===========================================================
import env
import math
from fractions import Fraction
from hypothesis import given, assume, strategies as st

from numth.basic import gcd, mod_inverse
from numth.types import frac, Rational
#===========================================================

def coords(flag=None):
    if flag == 'nonzero':
        return [st.integers().filter(lambda x: x != 0),
                st.integers(min_value=1)]
    if flag == 'positive':
        return [st.integers(min_value=0), st.integers(min_value=1)]
    return [st.integers(), st.integers(min_value=1)]

#===========================================================

@given(*coords())
def test_numer_and_denom(n, d):
    r = Rational(n, d)
    assert r.numer == r.numerator == r._numerator
    assert r.denom == r.denominator == r._denominator

#-----------------------------

@given(
    st.integers(),
    st.floats().filter(lambda x: not (math.isnan(x) or math.isinf(x))),
    *coords()
)
def test_constructors(i, fl, n, d):
    assert int(Rational.from_int(i)) == int(frac(i)) == i
    assert int(Rational.from_str(str(i))) == int(frac(str(i))) == i
    assert float(Rational.from_float(fl)) == float(frac(fl)) == fl
    assert float(Rational.from_str(str(fl))) == float(frac(fl)) == fl

    r = Rational(n, d)
    f = Fraction(n, d)
    s1 = '{}/{}'.format(n, d)
    s2 = '{} / {}'.format(n, d)
    l = [n, d]
    t = (n, d)
    assert Rational.from_Rational(r) == frac(r) == r
    assert Rational.from_Fraction(f) == frac(f) == r
    assert Rational.from_str(s1) == frac(s1) == r
    assert Rational.from_str(s2) == frac(s2) == r
    assert Rational.from_list(l) == frac(l) == r
    assert Rational.from_tuple(t) == frac(t) == r

#-----------------------------

@given(st.integers(), st.integers(max_value=-1))
def test_negative_denominator(n, d):
    r = Rational(n, d)
    assert r.numer * n <= 0
    assert r.denom > 0

#=============================

def test_decimal():
    a = 12837465999
    r = Rational(a, 10000000000)
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
        assert r.decimal(digits) == decimal
    for digits, decimal in enumerate(expected):
        assert (-r).decimal(digits) == '-{}'.format(decimal)

#=============================

@given(*coords('nonzero'))
def test_inverse(n, d):
    r = Rational(n, d)
    assert r.inverse == Rational(d, n)
    assert r * r.inverse == 1

#-----------------------------

@given(*coords())
def test_round_to_nearest_int(n, d):
    r = Rational(n, d)
    i = r.round_to_nearest_int
    assert abs(r - i) <= Rational(1, 2)

#-----------------------------

@given(*coords())
def test_is_square(n, d):
    r2 = Rational(n**2, d**2)
    assert r2.is_square

#=============================

@given(*coords(), *coords(), st.integers(min_value=0, max_value=30))
def test_approx_equal(n1, d1, n2, d2, num_digits):
    r = Rational(n1, d1)
    rr = Rational(n2, d2)
    in_range = abs(r - rr) < Rational(1, 10**num_digits)
    assert r.approx_equal(rr, num_digits) == in_range

@given(*coords(), st.integers(), st.integers(min_value=0, max_value=30))
def test_approx_equal_2(n, d, integer, num_digits):
    r = Rational(n, d)
    delta = Rational(integer, 10**(num_digits + 1))
    in_range = abs(delta) < Rational(1, 10**(num_digits))
    assert r.approx_equal(r + delta, num_digits) == in_range

#=============================

@given(*coords('positive'), st.integers(min_value=10, max_value=20))
def test_sqrt(n, d, num_digits):
    r = Rational(n, d)
    s = r.sqrt(num_digits)
    lhs = 10**num_digits * abs(r - s**2)
    rhs = s + int(s) + 1

    assert lhs < rhs

#=============================

@given(*coords())
def test_pos(n, d):
    r = Rational(n, d)
    assert type(+r) is Rational
    assert r == +r

#-----------------------------

@given(*coords())
def test_neg(n, d):
    r = Rational(n, d)
    assert type(-r) is Rational
    assert -r == Rational(-n, d)
    assert r == -(-r)

#-----------------------------

@given(*coords())
def test_abs(numer, denom):
    r = Rational(numer, denom)
    assert type(abs(r)) is Rational
    if r < 0:
        assert abs(r) == -r
    else:
        assert abs(r) == r

#=============================

@given(st.integers(), *coords(), *coords())
def test_add(i, n1, d1, n2, d2):
    r1 = Rational(n1, d1)
    r2 = Rational(n2, d2)
    f1 = Fraction(n1, d1)
    f2 = Fraction(n2, d2)
    assert r1 + r2 == r2 + r1 == f1 + f2
    assert r1 + f2 == f2 + r1 == f1 + f2
    assert f1 + r2 == r2 + f1 == f1 + f2
    assert r1 + i == i + r1 == f1 + i

@given(st.integers(), *coords(), *coords())
def test_sub(i, n1, d1, n2, d2):
    r1 = Rational(n1, d1)
    r2 = Rational(n2, d2)
    f1 = Fraction(n1, d1)
    f2 = Fraction(n2, d2)
    assert r1 - r2 == -(r2 - r1) == f1 - f2
    assert r1 - f2 == -(f2 - r1) == f1 - f2
    assert f1 - r2 == -(r2 - f1) == f1 - f2
    assert r1 - i == -(i - r1) == f1 - i

@given(st.integers(), *coords(), *coords())
def test_mul(i, n1, d1, n2, d2):
    r1 = Rational(n1, d1)
    r2 = Rational(n2, d2)
    f1 = Fraction(n1, d1)
    f2 = Fraction(n2, d2)
    assert r1 * r2 == r2 * r1 == f1 * f2
    assert r1 * f2 == f2 * r1 == f1 * f2
    assert f1 * r2 == r2 * f1 == f1 * f2
    assert r1 * i == i * r1 == f1 * i

@given(
    st.integers().filter(lambda x: x != 0),
    *coords('nonzero'),
    *coords('nonzero')
)
def test_div(i, n1, d1, n2, d2):
    r1 = Rational(n1, d1)
    r2 = Rational(n2, d2)
    f1 = Fraction(n1, d1)
    f2 = Fraction(n2, d2)
    assert r1 / r2 == (r2 / r1).inverse == f1 / f2
    assert r1 / f2 == (f2 / r1).inverse == f1 / f2
    assert f1 / r2 == (r2 / f1).inverse == f1 / f2
    assert r1 / i == (i / r1).inverse == f1 / i

#=============================

@given(*coords('nonzero'), st.integers(min_value=0, max_value=15))
def test_pow(n, d, e):
    r = Rational(n, d)
    r_e = r**e
    f = Fraction(n, d)
    f_e = f**e
    s = Rational(n**e, d**e)
    assert r_e == f_e
    assert r_e == s
    assert r**(-e) == s.inverse
    assert r**Rational(e, 1) == s
    assert n**Rational(e, 1) == n**e

