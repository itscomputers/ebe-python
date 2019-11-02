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

@given(st.integers(), st.integers(max_value=-1))
def test_negative_denominator(n, d):
    a = Rational(n, d)
    assert a.numer * n <= 0
    assert a.denom > 0

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

#=============================

@given(rational(), rational())
def test_comparison(a, b):
    signature = a.numer * b.denom - a.denom * b.numer
    if signature == 0:
        assert a == b
        assert a >= b
        assert a <= b
    elif signature < 0:
        assert a < b
        assert a <= b
        assert b > a
        assert b >= a
    else:
        assert a > b
        assert a >= b
        assert b < a
        assert b <= a

@given(rational(), st.integers())
def test_comparison_int(a, b):
    signature = a.numer - a.denom * b
    if signature == 0:
        assert a == b
        assert a >= b
        assert a <= b
    elif signature < 0:
        assert a < b
        assert a <= b
        assert b > a
        assert b >= a
    else:
        assert a > b
        assert a >= b
        assert b < a
        assert b <= a

@given(rational(), rational())
def test_comparison_Fraction(a, b):
    signature = a.numer * b.denominator - a.denom * b.numerator
    if signature == 0:
        assert a == b
        assert a >= b
        assert a <= b
    elif signature < 0:
        assert a < b
        assert a <= b
        assert b > a
        assert b >= a
    else:
        assert a > b
        assert a >= b
        assert b < a
        assert b <= a

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

#-----------------------------

@given(rational('nonzero'))
def test_inverse(a):
    assert type(a.inverse) is Rational
    assert a.inverse == Rational(a.denom, a.numer)
    assert a * a.inverse == 1

#-----------------------------

@given(rational())
def test_round_to_nearest_int(a):
    rounded = a.round_to_nearest_int
    assert type(rounded) is int
    assert abs(a - rounded) <= Rational(1, 2)

#-----------------------------

@given(rational())
def test_round_prefer_toward_zero(a):
    rounded = a.round_prefer_toward_zero
    assert type(rounded) is int
    if abs(a - rounded) == Rational(1, 2):
        assert abs(rounded) == abs(a.round_to_nearest_int) - 1
    else:
        assert abs(a - rounded) < Rational(1, 2)

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

@given(rational(), rational())
def test_add(a, b):
    assert type(a + b) is Rational
    assert a + b == b + a
    assert a + b == a.to_fraction + b.to_fraction

@given(rational(), st.integers())
def test_add_int(a, b):
    assert type(a + b) is Rational
    assert type(b + a) is Rational
    assert a + b == b + a
    assert a + b == a.to_fraction + b
    assert b + a == b + a.to_fraction

@given(rational(), st.fractions())
def test_add_Fraction(a, b):
    assert type(a + b) is Rational
    assert type(b + a) is Rational
    assert a + b == b + a
    assert a + b == a.to_fraction + b
    assert b + a == b + a.to_fraction

#-----------------------------

@given(rational(), rational())
def test_sub(a, b):
    assert type(a - b) is Rational
    assert a - b == -(b - a) == -b + a
    assert a - b == a.to_fraction - b.to_fraction

@given(rational(), st.integers())
def test_sub_int(a, b):
    assert type(a - b) is Rational
    assert type(b - a) is Rational
    assert a - b == -(b - a) == -b + a
    assert a - b == a.to_fraction - b
    assert b - a == b - a.to_fraction

@given(rational(), st.fractions())
def test_sub_Fraction(a, b):
    assert type(a - b) is Rational
    assert type(b - a) is Rational
    assert a - b == -(b - a) == -b + a
    assert a - b == a.to_fraction - b
    assert b - a == b - a.to_fraction

#-----------------------------

@given(rational(), rational())
def test_mul(a, b):
    assert type(a * b) is Rational
    assert a * b == b * a
    assert a * b == a.to_fraction * b.to_fraction

@given(rational(), st.integers())
def test_mul_int(a, b):
    assert type(a * b) is Rational
    assert type(b * a) is Rational
    assert a * b == b * a
    assert a * b == a.to_fraction * b
    assert b * a == b * a.to_fraction

@given(rational(), st.fractions())
def test_mul_Fraction(a, b):
    assert type(a * b) is Rational
    assert type(b * a) is Rational
    assert a * b == b * a
    assert a * b == a.to_fraction * b
    assert b * a == b * a.to_fraction

#-----------------------------

@given(rational('nonzero'), rational('nonzero'))
def test_truediv(a, b):
    assert type(a / b) is Rational
    assert a / b == (b / a).inverse == 1/b * a
    assert a / b == a.to_fraction / b.to_fraction

@given(rational('nonzero'), st.integers().filter(lambda x: x != 0))
def test_truediv_int(a, b):
    assert type(a / b) is Rational
    assert type(b / a) is Rational
    assert a / b == (b / a).inverse == Rational(1, b) * a
    assert a / b == a.to_fraction / b
    assert b / a == b / a.to_fraction

@given(rational('nonzero'), st.fractions().filter(lambda x: x != 0))
def test_truediv_Fraction(a, b):
    assert type(a / b) is Rational
    assert type(b / a) is Rational
    assert a / b == (b / a).inverse == 1/b * a
    assert a / b == a.to_fraction / b
    assert b / a == b / a.to_fraction

#-----------------------------

@given(rational('nonzero'), rational('nonzero'))
def test_floordiv(a, b):
    assert type(a // b) is int
    assert a // b == a.to_fraction // b.to_fraction

@given(rational('nonzero'), st.integers().filter(lambda x: x != 0))
def test_floordiv_int(a, b):
    assert type(a // b) is int
    assert type(b // a) is int
    assert a // b == a.to_fraction // b
    assert b // a == b // a.to_fraction

@given(rational('nonzero'), st.fractions().filter(lambda x: x != 0))
def test_floordiv_Fraction(a, b):
    assert type(a // b) is int
    assert type(b // a) is int
    assert a // b == a.to_fraction // b
    assert b // a == b // a.to_fraction

#-----------------------------

@given(rational('nonzero'), rational('nonzero'))
def test_mod(a, b):
    assert type(a % b) is Rational
    assert a == (a // b) * b + (a % b)
    assert a % b == a.to_fraction % b.to_fraction

@given(rational('nonzero'), st.integers().filter(lambda x: x != 0))
def test_mod_int(a, b):
    assert type(a % b) is Rational
    assert type(b % a) is Rational
    assert a == (a // b) * b + (a % b)
    assert b == (b // a) * a + (b % a)
    assert a % b == a.to_fraction % b
    assert b % a == b % a.to_fraction

@given(rational('nonzero'), st.fractions().filter(lambda x: x != 0))
def test_mod_Fraction(a, b):
    assert type(a % b) is Rational
    assert type(b % a) is Rational
    assert a == (a // b) * b + (a % b)
    assert b == (b // a) * a + (b % a)
    assert a % b == a.to_fraction % b
    assert b % a == b % a.to_fraction

#=============================

@given(rational('nonzero'), st.integers(min_value=0, max_value=15))
def test_pow(a, m):
    mth_power = a**m
    assert type(mth_power) is Rational
    assert mth_power == a.to_fraction**m
    assert mth_power == Rational(a.numer**m, a.denom**m)
    assert a**(-m) == mth_power.inverse
    assert a**Rational(m, 1) == mth_power
    assert a.numer**Rational(m, 1) == a.numer**m

