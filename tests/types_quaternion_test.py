#   tests/types_quaternion_test.py
#===========================================================
import pytest
from hypothesis import assume, given, strategies as st

import env
from numth.basic import div_with_small_remainder
from numth.types import Rational
from numth.types.quaternion import *
#===========================================================

@st.composite
def rational(draw, nonzero=False):
    numer = draw(st.integers())
    denom = draw(st.integers(min_value=1))
    if nonzero:
        assume( numer != 0 )
    return Rational(numer, denom)

@st.composite
def quaternion(draw, nonzero=False):
    r = draw(st.integers())
    i = draw(st.integers())
    j = draw(st.integers())
    k = draw(st.integers())
    if nonzero:
        assume( (r, i, j, k) != (0, 0, 0, 0) )
    return Quaternion(r, i, j, k)

@st.composite
def quaternion_rational(draw, nonzero=False):
    r_n = draw(st.integers())
    r_d = draw(st.integers(min_value=1))
    i_n = draw(st.integers())
    i_d = draw(st.integers(min_value=1))
    j_n = draw(st.integers())
    j_d = draw(st.integers(min_value=1))
    k_n = draw(st.integers())
    k_d = draw(st.integers(min_value=1))
    if nonzero:
        assume( (r_n, i_n, j_n, k_n) != (0, 0, 0, 0) )
    r = Rational(r_n, r_d)
    i = Rational(i_n, i_d)
    j = Rational(j_n, j_d)
    k = Rational(k_n, k_d)
    return Quaternion(r, i, j, k)

@st.composite
def gaussian_rational(draw, nonzero=False):
    real = draw(st.integers())
    imag = draw(st.integers())
    if nonzero:
        assume( (real, imag) != (0, 0) )
    return GaussianRational(real, imag)

@st.composite
def gaussian_integer(draw, nonzero=False):
    real = draw(st.integers())
    imag = draw(st.integers())
    if nonzero:
        assume( (real, imag) != (0, 0) )
    return GaussianInteger(real, imag)

#=============================

@given(
    st.integers(min_value=2),
    st.integers(min_value=2),
    st.integers(min_value=2),
    st.integers(min_value=2)
)
def test_display(r, i, j, k):
    assert repr(Quaternion(0, 0, 0, 0)) == '0'
    assert repr(Quaternion(0, 0, 0, 1)) == 'k'
    assert repr(Quaternion(0, 0, 1, 0)) == 'j'
    assert repr(Quaternion(0, 1, 0, 0)) == 'i'
    assert repr(Quaternion(1, 0, 0, 0)) == '1'
    assert repr(Quaternion(0, 0, 0, -1)) == '-k'
    assert repr(Quaternion(0, 0, -1, 0)) == '-j'
    assert repr(Quaternion(0, -1, 0, 0)) == '-i'
    assert repr(Quaternion(-1, 0, 0, 0)) == '-1'

    assert repr(Quaternion(0, 0, 0, k)) == '{} k'.format(k)
    assert repr(Quaternion(0, 0, j, 0)) == '{} j'.format(j)
    assert repr(Quaternion(0, i, 0, 0)) == '{} i'.format(i)
    assert repr(Quaternion(r, 0, 0, 0)) == '{}'.format(r)
    assert repr(Quaternion(0, 0, 0, -k)) == '-{} k'.format(k)
    assert repr(Quaternion(0, 0, -j, 0)) == '-{} j'.format(j)
    assert repr(Quaternion(0, -i, 0, 0)) == '-{} i'.format(i)
    assert repr(Quaternion(-r, 0, 0, 0)) == '-{}'.format(r)

    assert repr(Quaternion(r, 0, 0, 1)) == '{} + k'.format(r)
    assert repr(Quaternion(r, 0, 1, 0)) == '{} + j'.format(r)
    assert repr(Quaternion(r, 1, 0, 0)) == '{} + i'.format(r)
    assert repr(Quaternion(r, 0, 0, -1)) == '{} - k'.format(r)
    assert repr(Quaternion(r, 0, -1, 0)) == '{} - j'.format(r)
    assert repr(Quaternion(r, -1, 0, 0)) == '{} - i'.format(r)

    assert repr(Quaternion(r, 0, 0, k)) == '{} + {} k'.format(r, k)
    assert repr(Quaternion(r, 0, j, 0)) == '{} + {} j'.format(r, j)
    assert repr(Quaternion(r, i, 0, 0)) == '{} + {} i'.format(r, i)
    assert repr(Quaternion(r, 0, 0, -k)) == '{} - {} k'.format(r, k)
    assert repr(Quaternion(r, 0, -j, 0)) == '{} - {} j'.format(r, j)
    assert repr(Quaternion(r, -i, 0, 0)) == '{} - {} i'.format(r, i)

    assert repr(Quaternion(r, i, j, k)) == '{} + {} i + {} j + {} k'.format(r, i, j, k)

    assert repr(Quaternion(r, i, j, -k)) == '{} + {} i + {} j - {} k'.format(r, i, j, k)
    assert repr(Quaternion(r, i, -j, k)) == '{} + {} i - {} j + {} k'.format(r, i, j, k)
    assert repr(Quaternion(r, -i, j, k)) == '{} - {} i + {} j + {} k'.format(r, i, j, k)
    assert repr(Quaternion(-r, i, j, k)) == '-{} + {} i + {} j + {} k'.format(r, i, j, k)

    assert repr(Quaternion(r, i, -j, -k)) == '{} + {} i - {} j - {} k'.format(r, i, j, k)
    assert repr(Quaternion(r, -i, j, -k)) == '{} - {} i + {} j - {} k'.format(r, i, j, k)
    assert repr(Quaternion(-r, i, j, -k)) == '-{} + {} i + {} j - {} k'.format(r, i, j, k)
    assert repr(Quaternion(r, -i, -j, k)) == '{} - {} i - {} j + {} k'.format(r, i, j, k)
    assert repr(Quaternion(-r, i, -j, k)) == '-{} + {} i - {} j + {} k'.format(r, i, j, k)
    assert repr(Quaternion(-r, -i, j, k)) == '-{} - {} i + {} j + {} k'.format(r, i, j, k)

    assert repr(Quaternion(r, -i, -j, -k)) == '{} - {} i - {} j - {} k'.format(r, i, j, k)
    assert repr(Quaternion(-r, i, -j, -k)) == '-{} + {} i - {} j - {} k'.format(r, i, j, k)
    assert repr(Quaternion(-r, -i, j, -k)) == '-{} - {} i + {} j - {} k'.format(r, i, j, k)
    assert repr(Quaternion(-r, -i, -j, k)) == '-{} - {} i - {} j + {} k'.format(r, i, j, k)

    assert repr(Quaternion(-r, -i, -j, -k)) == '-{} - {} i - {} j - {} k'.format(r, i, j, k)

#=============================

@given(gaussian_rational())
def test_from_gaussian_rational(a):
    result = Quaternion.from_gaussian_rational(a)
    assert type(result) is Quaternion
    assert result.r == a.real
    assert result.i == a.imag
    assert result.j == result.k == 0

@given(gaussian_integer())
def test_from_gaussian_integer(a):
    result = Quaternion.from_gaussian_integer(a)
    assert type(result) is Quaternion
    assert result.r == a.real
    assert result.i == a.imag
    assert result.j == result.k == 0

#=============================

@given(quaternion(), quaternion())
def test_eq(a, b):
    assert a == a
    if a.components == b.components:
        assert a == b
    else:
        assert a != b

@given(quaternion(), st.integers())
def test_eq_int(a, i):
    if a.is_real and a.r == i:
        assert a == i
    else:
        assert a != i

@given(quaternion(), rational())
def test_eq_Rational(a, r):
    if a.is_real and a.r == r:
        assert a == r
    else:
        assert a != r

#=============================

@given(quaternion())
def test_neg(a):
    assert type(-a) is Quaternion
    assert -a == Quaternion(-a.r, -a.i, -a.j, -a.k)
    assert a + -a == -a + a == 0
    assert -a == -1 * a == a * -1

@given(quaternion())
def test_norm_conjugate(a):
    conj = a.conjugate
    norm = a.norm
    assert type(conj) is Quaternion
    assert type(norm) is Rational
    assert conj == Quaternion(a.r, -a.i, -a.j, -a.k)
    assert norm == a.r**2 + a.i**2 + a.j**2 + a.k**2
    assert a * conj == norm
    assert a + conj == 2 * a.r
    assert a - conj == Quaternion(0, 2*a.i, 2*a.j, 2*a.k)

@given(quaternion_rational(nonzero=True))
def test_inverse(a):
    inv = a.inverse
    assert type(inv) is Quaternion
    assert a * inv == 1
    assert inv.inverse == a

@given(quaternion_rational())
def test_round(a):
    r = a.round
    assert type(r) is Quaternion
    assert set(map(lambda x: x.denom, r.components)) == set([1])

    for cmpt in (a - r).components:
        assert 2 * abs(cmpt) <= 1

#=============================

@given(quaternion(), quaternion())
def test_add(a, b):
    result = a + b
    reverse = b + a
    assert type(result) is Quaternion
    assert result == reverse
    assert result == Quaternion(a.r + b.r, a.i + b.i, a.j + b.j, a.k + b.k)

@given(quaternion(), st.integers())
def test_add_int(a, b):
    result = a + b
    reverse = b + a
    assert type(result) is Quaternion
    assert type(reverse) is Quaternion
    assert result == reverse
    assert result == Quaternion(a.r + b, a.i, a.j, a.k)

@given(quaternion(), rational())
def test_add_Rational(a, b):
    result = a + b
    reverse = b + a
    assert type(result) is Quaternion
    assert type(reverse) is Quaternion
    assert result == reverse
    assert result == Quaternion(a.r + b, a.i, a.j, a.k)

#=============================

@given(quaternion(), quaternion())
def test_sub(a, b):
    result = a - b
    reverse = b - a
    assert type(result) is Quaternion
    assert result == -reverse == -b + a
    assert result == Quaternion(a.r - b.r, a.i - b.i, a.j - b.j, a.k - b.k)
    assert result + b == a

@given(quaternion(), st.integers())
def test_sub_int(a, b):
    result = a - b
    reverse = b - a
    assert type(result) is Quaternion
    assert type(reverse) is Quaternion
    assert result == -reverse == -b + a
    assert result == Quaternion(a.r - b, a.i, a.j, a.k)

@given(quaternion(), rational())
def test_sub_Rational(a, b):
    result = a - b
    reverse = b - a
    assert type(result) is Quaternion
    assert type(reverse) is Quaternion
    assert result == -reverse == -b + a
    assert result == Quaternion(a.r - b, a.i, a.j, a.k)

#=============================

@given(quaternion(), quaternion())
def test_mul(a, b):
    result = a * b
    assert type(result) is Quaternion
    assert result == Quaternion(
        a.r*b.r - a.i*b.i - a.j*b.j - a.k*b.k,
        a.r*b.i + a.i*b.r + a.j*b.k - a.k*b.j,
        a.r*b.j - a.i*b.k + a.j*b.r + a.k*b.i,
        a.r*b.k + a.i*b.j - a.j*b.i + a.k*b.r
    )

@given(quaternion(), st.integers())
def test_mul_int(a, b):
    result = a * b
    reverse = b * a
    assert type(result) is Quaternion
    assert type(reverse) is Quaternion
    assert result == reverse
    assert result == Quaternion(a.r * b, a.i * b, a.j * b, a.k * b)

@given(quaternion(), rational())
def test_mul_Rational(a, b):
    result = a * b
    reverse = b * a
    assert type(result) is Quaternion
    assert type(reverse) is Quaternion
    assert result == reverse
    assert result == Quaternion(a.r * b, a.i * b, a.j * b, a.k * b)

#=============================

@given(quaternion(), quaternion(nonzero=True))
def test_truediv(a, b):
    result = a / b
    b_norm = b.norm
    assert type(result) is Quaternion
    assert result == Quaternion(
        (a.r*b.r + a.i*b.i + a.j*b.j + a.k*b.k) / b_norm,
        (-a.r*b.i + a.i*b.r - a.j*b.k + a.k*b.j) / b_norm,
        (-a.r*b.j + a.i*b.k + a.j*b.r - a.k*b.i) / b_norm,
        (-a.r*b.k - a.i*b.j + a.j*b.i + a.k*b.r) / b_norm
    )
    assert result == a * b.inverse
    assert result * b == a

@given(quaternion(nonzero=True), st.integers().filter(lambda x: x != 0))
def test_truediv_int(a, b):
    result = a / b
    reverse = b / a
    assert type(result) is Quaternion
    assert type(reverse) is Quaternion
    assert result == Quaternion(a.r / b, a.i / b, a.j / b, a.k / b)
    assert result * b == a
    assert reverse == b * a.inverse
    assert reverse * a == b

@given(quaternion(nonzero=True), rational(nonzero=True))
def test_truediv_Rational(a, b):
    result = a / b
    reverse = b / a
    assert type(result) is Quaternion
    assert type(reverse) is Quaternion
    assert result == Quaternion(a.r / b, a.i / b, a.j / b, a.k / b)
    assert result * b == a
    assert reverse == b * a.inverse
    assert reverse * a == b

#=============================

@given(quaternion(), quaternion(nonzero=True))
def test_floordiv(a, b):
    result = a // b
    assert type(result) is Quaternion
    assert set(map(lambda x: x.denom, result.components)) == set([1])

@given(quaternion(nonzero=True), st.integers().filter(lambda x: x != 0))
def test_floordiv_int(a, b):
    result = a // b
    reverse = b // a
    assert type(result) is Quaternion
    assert type(reverse) is Quaternion
    assert result == a // Quaternion(b, 0, 0, 0)
    assert reverse == Quaternion(b, 0, 0, 0) // a

@given(quaternion(nonzero=True), rational(nonzero=True))
def test_floordiv_Rational(a, b):
    result = a // b
    reverse = b // a
    assert type(result) is Quaternion
    assert type(reverse) is Quaternion
    assert result == a // Quaternion(b, 0, 0, 0)
    assert reverse == Quaternion(b, 0, 0, 0) // a

#=============================

@given(quaternion(), quaternion(nonzero=True))
def test_mod(a, b):
    result = a % b
    assert type(result) is Quaternion
    assert (result).norm <= b.norm
    assert a == (a // b) * b + result

@given(quaternion(nonzero=True), st.integers().filter(lambda x: x != 0))
def test_mod_int(a, b):
    result = a % b
    reverse = b % a
    assert type(result) is Quaternion
    assert type(reverse) is Quaternion
    assert result == a % Quaternion(b, 0, 0, 0)
    assert reverse == Quaternion(b, 0, 0, 0) % a
    assert result.norm <= b**2
    assert a == (a // b) * b + result
    assert b == (b // a) * a + reverse

@given(quaternion(nonzero=True), rational(nonzero=True))
def test_mod_Rational(a, b):
    result = a % b
    reverse = b % a
    assert type(result) is Quaternion
    assert type(reverse) is Quaternion
    assert result == a % Quaternion(b, 0, 0, 0)
    assert reverse == Quaternion(b, 0, 0, 0) % a
    assert result.norm <= b**2
    assert a == (a // b) * b + result
    assert b == (b // a) * a + reverse

#=============================

@given(
    quaternion(nonzero=True),
    st.integers(min_value=-20, max_value=20),
    st.integers(min_value=-10, max_value=10)
)
def test_pow(a, m, n):
    mth_power = a**m
    nth_power = a**n
    sum_power = a**(m + n)
    assert type(a**0) is Quaternion
    assert type(a**1) is Quaternion
    assert type(a**-1) is Quaternion
    assert type(mth_power) is Quaternion
    assert a**0 == 1
    assert a**1 == a
    assert a**-1 == a.inverse
    assert a**2 == a * a
    assert a**-2 == (a * a).inverse
    assert mth_power * nth_power == sum_power
    assert sum_power / mth_power == nth_power
    assert a**-m == mth_power.inverse

