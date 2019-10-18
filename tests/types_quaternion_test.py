#   tests/types_quadratic_test.py
#===========================================================
import env
import pytest
from hypothesis import assume, given, strategies as st

from numth.basic import div_with_small_remainder
from numth.types import Rational
from numth.types.quaternion import *
#===========================================================

def coords():
    return 4 * [st.integers()]

def rational(flag=None):
    if flag == 'nonzero':
        return [st.integers().filter(lambda x: x != 0),
                st.integers(min_value=1)]
    return [st.integers(), st.integers(min_value=1)]

def rational_coords(flag=None):
    return 4 * [*rational(flag)]

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

@given(*coords())
def test_from_components(r, i, j, k):
    a = Quaternion(r, i, j, k)
    assert Quaternion.from_components(r, i, j, k) == a
    assert Quaternion.from_components(r, -i, -j, -k) == a.conjugate
    assert Quaternion.from_components(-r, -i, -j, -k) == -a

#-----------------------------

@given(*coords()[:2])
def test_from_quadratic(a, b):
    quaternion = Quaternion(a, b, 0, 0)
    quadratic = Quadratic(a, b, -1)
    quadratic_integer = QuadraticInteger(a, b, -1)
    gaussian_integer = GaussianInteger(a, b)
    assert quaternion == Quaternion.from_quadratic(quadratic)
    assert quaternion == Quaternion.from_quadratic_integer(quadratic_integer)
    assert quaternion == Quaternion.from_gaussian_integer(gaussian_integer)

    assert Quaternion.from_quadratic(Quadratic(a, b, 2)) is NotImplemented
    assert Quaternion.from_quadratic(Quadratic(a, b, -2)) is NotImplemented

#-----------------------------

@given(*coords())
def test_to_quadratic(r, i, j, k):
    quaternion = Quaternion(r, i, j, k)
    quadratic = Quadratic(r, i, -1)
    gaussian_integer = GaussianInteger(r, i)
    if j == k == 0:
        assert quaternion.to_quadratic == quadratic
        assert quaternion.to_gaussian_integer == gaussian_integer
    else:
        assert quaternion.to_quadratic is NotImplemented
        assert quaternion.to_gaussian_integer is NotImplemented

#=============================

@given(*coords())
def test_eq(r, i, j, k):
    a = Quaternion(r, i, j, k)
    b = Quaternion(r, i, j, k)
    x = Quaternion(r, r, j, k)
    y = Quaternion(r, i, r, k)
    z = Quaternion(r, i, j, r)
    assert a == b
    if r != i:
        assert a != x
    if r != j:
        assert a != y
    if r != k:
        assert a != z

#-----------------------------

@given(*coords()[:2])
def test_eq_quadratic(r, i):
    a = Quaternion(r, i, 0, 0)
    b = Quadratic(r, i, -1)
    w = Quadratic(r, i, 2)
    x = Quadratic(r + 1, i, -1)
    y = Quaternion(r, i, 1, 0)
    z = Quaternion(r, i, 0, 1)
    assert a == b
    assert a != w
    assert a != x
    assert b != y
    assert b != z

#-----------------------------

@given(*coords())
def test_eq_int(r, i, j, k):
    a = Quaternion(r, i, j, k)
    b = Quaternion(r, 0, 0, 0)
    if i == j == k == 0:
        assert a == r
    else:
        assert a != r
    assert b == r

#-----------------------------

@given(*rational_coords())
def test_eq_rational(r_n, r_d, i_n, i_d, j_n, j_d, k_n, k_d):
    r = frac(r_n, r_d)
    i = frac(i_n, i_d)
    j = frac(j_n, j_d)
    k = frac(k_n, k_d)
    a = Quaternion(r, i, j, k)
    b = Quaternion(r, 0, 0, 0)
    if i == j == k == 0:
        assert a == r
    else:
        assert a != r
    assert b == r

#=============================

@given(*coords())
def test_neg(r, i, j, k):
    a = Quaternion(r, i, j, k)
    assert -a == Quaternion(-r, -i, -j, -k)
    assert a + -a == -a + a == 0
    assert -a == -1 * a

#-----------------------------

@given(*coords())
def test_norm_conjugate(r, i, j, k):
    a = Quaternion(r, i, j, k)
    assert a.conjugate == Quaternion(r, -i, -j, -k)
    assert a.norm == r**2 + i**2 + j**2 + k**2
    assert a * a.conjugate == a.norm
    assert a + a.conjugate == 2 * a.r
    assert a - a.conjugate == Quaternion(0, 2*i, 2*j, 2*k)

#-----------------------------

@given(*rational_coords())
def test_inverse(r_n, r_d, i_n, i_d, j_n, j_d, k_n, k_d):
    assume( (r_n, i_n, j_n, k_n) != (0, 0, 0, 0) )
    r = frac(r_n, r_d)
    i = frac(i_n, i_d)
    j = frac(j_n, j_d)
    k = frac(k_n, k_d)
    a = Quaternion(r, i, j, k)
    assert a * a.inverse == 1
    assert a.inverse.inverse == a

#-----------------------------

@given(*rational_coords())
def test_round(r_n, r_d, i_n, i_d, j_n, j_d, k_n, k_d):
    assume( (r_n, i_n, j_n, k_n) != (0, 0, 0, 0) )
    r = frac(r_n, r_d)
    i = frac(i_n, i_d)
    j = frac(j_n, j_d)
    k = frac(k_n, k_d)
    a = Quaternion(r, i, j, k)
    z = a.round
    diff = a - z
    for c in diff.components:
        assert 2 * abs(c) <= 1

#=============================

@given(*coords(), *coords())
def test_add(r1, i1, j1, k1, r2, i2, j2, k2):
    a = Quaternion(r1, i1, j1, k1)
    b = Quaternion(r2, i2, j2, k2)
    z = Quaternion(r1 + r2, i1 + i2, j1 + j2, k1 + k2)
    assert type(a + b) is Quaternion
    assert type(b + a) is Quaternion
    assert a + b == z
    assert b + a == z

#-----------------------------

@given(*coords(), *coords()[:2])
def test_add_quadratic(r1, i1, j1, k1, r2, i2):
    a = Quaternion(r1, i1, j1, k1)
    b = Quadratic(r2, i2, -1)
    z = Quaternion(r1 + r2, i1 + i2, j1, k1)
    assert type(a + b) is Quaternion
    assert type(b + a) is Quaternion
    assert a + b == z
    assert b + a == z

#-----------------------------

@given(*coords(), *coords()[:2])
def test_add_quadratic_integer(r1, i1, j1, k1, r2, i2):
    a = Quaternion(r1, i1, j1, k1)
    b = QuadraticInteger(r2, i2, -1)
    z = Quaternion(r1 + r2, i1 + i2, j1, k1)
    assert type(a + b) is Quaternion
    assert type(b + a) is Quaternion
    assert a + b == z
    assert b + a == z

#-----------------------------

@given(*coords(), st.integers())
def test_add_int(r, i, j, k, integer):
    a = Quaternion(r, i, j, k)
    b = integer
    z = Quaternion(r + b, i, j, k)
    assert type(a + b) is Quaternion
    assert type(b + a) is Quaternion
    assert a + b == z
    assert b + a == z

#-----------------------------

@given(*coords(), *rational())
def test_add_rational(r, i, j, k, numer, denom):
    a = Quaternion(r, i, j, k)
    b = frac(numer, denom)
    z = Quaternion(r + b, i, j, k)
    assert type(a + b) is Quaternion
    assert type(b + a) is Quaternion
    assert a + b == z
    assert b + a == z

#=============================

@given(*coords(), *coords())
def test_sub(r1, i1, j1, k1, r2, i2, j2, k2):
    a = Quaternion(r1, i1, j1, k1)
    b = Quaternion(r2, i2, j2, k2)
    z = Quaternion(r1 - r2, i1 - i2, j1 - j2, k1 - k2)
    assert type(a - b) is Quaternion
    assert type(b - a) is Quaternion
    assert a - b == z
    assert b - a == -z

#-----------------------------

@given(*coords(), *coords()[:2])
def test_sub_quadratic(r1, i1, j1, k1, r2, i2):
    a = Quaternion(r1, i1, j1, k1)
    b = Quadratic(r2, i2, -1)
    z = Quaternion(r1 - r2, i1 - i2, j1, k1)
    assert type(a - b) is Quaternion
    assert type(b - a) is Quaternion
    assert a - b == z
    assert b - a == -z

#-----------------------------

@given(*coords(), *coords()[:2])
def test_sub_quadratic_integer(r1, i1, j1, k1, r2, i2):
    a = Quaternion(r1, i1, j1, k1)
    b = QuadraticInteger(r2, i2, -1)
    z = Quaternion(r1 - r2, i1 - i2, j1, k1)
    assert type(a - b) is Quaternion
    assert type(b - a) is Quaternion
    assert a - b == z
    assert b - a == -z

#-----------------------------

@given(*coords(), st.integers())
def test_sub_int(r, i, j, k, integer):
    a = Quaternion(r, i, j, k)
    b = integer
    z = Quaternion(r - b, i, j, k)
    assert type(a - b) is Quaternion
    assert type(b - a) is Quaternion
    assert a - b == z
    assert b - a == -z

#-----------------------------

@given(*coords(), *rational())
def test_sub_rational(r, i, j, k, numer, denom):
    a = Quaternion(r, i, j, k)
    b = frac(numer, denom)
    z = Quaternion(r - b, i, j, k)
    assert type(a - b) is Quaternion
    assert type(b - a) is Quaternion
    assert a - b == z
    assert b - a == -z

#=============================

@given(*coords(), *coords())
def test_mul(r1, i1, j1, k1, r2, i2, j2, k2):
    a = Quaternion(r1, i1, j1, k1)
    b = Quaternion(r2, i2, j2, k2)
    z = Quaternion(
        r1*r2 - i1*i2 - j1*j2 - k1*k2,
        r1*i2 + i1*r2 + j1*k2 - k1*j2,
        r1*j2 - i1*k2 + j1*r2 + k1*i2,
        r1*k2 + i1*j2 - j1*i2 + k1*r2
    )
    assert type(a * b) is Quaternion
    assert a * b == z

#-----------------------------

@given(*coords(), *coords()[:2])
def test_mul_quadratic(r1, i1, j1, k1, r2, i2):
    a = Quaternion(r1, i1, j1, k1)
    b = Quadratic(r2, i2, -1)
    z = Quaternion(
        r1*r2 - i1*i2,
        r1*i2 + i1*r2,
        j1*r2 + k1*i2,
        -j1*i2 + k1*r2
    )
    assert type(a * b) is Quaternion
    assert a * b == z

#-----------------------------

@given(*coords(), *coords()[:2])
def test_mul_quadratic_integer(r1, i1, j1, k1, r2, i2):
    a = Quaternion(r1, i1, j1, k1)
    b = QuadraticInteger(r2, i2, -1)
    z = Quaternion(
        r1*r2 - i1*i2,
        r1*i2 + i1*r2,
        j1*r2 + k1*i2,
        -j1*i2 + k1*r2
    )
    assert type(a * b) is Quaternion
    assert type(b * a) is Quaternion
    assert a * b == z
    assert b * a == Quaternion(r2, i2, 0, 0) * a

#-----------------------------

@given(*coords(), st.integers())
def test_mul_int(r, i, j, k, integer):
    a = Quaternion(r, i, j, k)
    b = integer
    z = Quaternion(r * b, i * b, j * b, k * b)
    assert type(a * b) is Quaternion
    assert type(b * a) is Quaternion
    assert a * b == z
    assert b * a == z

#-----------------------------

@given(*coords(), *rational())
def test_mul_rational(r, i, j, k, numer, denom):
    a = Quaternion(r, i, j, k)
    b = frac(numer, denom)
    z = Quaternion(r * b, i * b, j * b, k * b)
    assert type(a * b) is Quaternion
    assert type(b * a) is Quaternion
    assert a * b == z
    assert b * a == z

#=============================

@given(*coords(), *coords())
def test_div(r1, i1, j1, k1, r2, i2, j2, k2):
    assume( (r1, i1, j1, k1) != (0, 0, 0, 0) )
    assume( (r2, i2, j2, k2) != (0, 0, 0, 0) )
    a = Quaternion(r1, i1, j1, k1)
    b = Quaternion(r2, i2, j2, k2)
    b_norm = b.norm
    z = Quaternion(
        frac(r1*r2 + i1*i2 + j1*j2 + k1*k2) / b_norm,
        frac(-r1*i2 + i1*r2 - j1*k2 + k1*j2) / b_norm,
        frac(-r1*j2 + i1*k2 + j1*r2 - k1*i2) / b_norm,
        frac(-r1*k2 - i1*j2 + j1*i2 + k1*r2) / b_norm
    )
    assert type(a / b) is Quaternion
    assert type(b / a) is Quaternion
    assert a / b == z
    assert b / a == z.inverse

#-----------------------------

@given(*coords(), *coords()[:2])
def test_div_quadratic(r1, i1, j1, k1, r2, i2):
    assume( (r1, i1, j1, k1) != (0, 0, 0, 0) )
    assume( (r2, i2) != (0, 0) )
    a = Quaternion(r1, i1, j1, k1)
    b = Quadratic(r2, i2, -1)
    b_norm = b.norm
    z = Quaternion(
        frac(r1*r2 + i1*i2) / b_norm,
        frac(-r1*i2 + i1*r2) / b_norm,
        frac(j1*r2 - k1*i2) / b_norm,
        frac(j1*i2 + k1*r2) / b_norm
    )
    assert type(a / b) is Quaternion
    assert type(b / a) is Quaternion
    assert a / b == z
    assert b / a == z.inverse

#-----------------------------

@given(*coords(), *coords()[:2])
def test_div_quadratic_integer(r1, i1, j1, k1, r2, i2):
    assume( (r1, i1, j1, k1) != (0, 0, 0, 0) )
    assume( (r2, i2) != (0, 0) )
    a = Quaternion(r1, i1, j1, k1)
    b = QuadraticInteger(r2, i2, -1)
    b_norm = b.norm
    z = Quaternion(
        frac(r1*r2 + i1*i2) / b_norm,
        frac(-r1*i2 + i1*r2) / b_norm,
        frac(j1*r2 - k1*i2) / b_norm,
        frac(j1*i2 + k1*r2) / b_norm
    )
    assert type(a / b) is Quaternion
    assert type(b / a) is Quaternion
    assert a / b == z
    assert b / a == z.inverse

#-----------------------------

@given(*coords(), st.integers().filter(lambda x: x != 0))
def test_div_int(r, i, j, k, integer):
    assume( (r, i, j, k) != (0, 0, 0, 0) )
    a = Quaternion(r, i, j, k)
    b = integer
    z = Quaternion(frac(r, b), frac(i, b), frac(j, b), frac(k, b))
    assert type(a / b) is Quaternion
    assert type(b / a) is Quaternion
    assert a / b == z
    assert b / a == z.inverse

#-----------------------------

@given(*coords(), *rational('nonzero'))
def test_div_rational(r, i, j, k, numer, denom):
    assume( (r, i, j, k) != (0, 0, 0, 0) )
    a = Quaternion(r, i, j, k)
    b = frac(numer, denom)
    z = Quaternion(r / b, i / b, j / b, k / b)
    assert type(a / b) is Quaternion
    assert type(b / a) is Quaternion
    assert a / b == z
    assert b / a == z.inverse

#=============================

@given(*coords(), *coords())
def test_floordiv_and_mod(r1, i1, j1, k1, r2, i2, j2, k2):
    assume( (r1, i1, j1, k1) != (0, 0, 0, 0) )
    assume( (r2, i2, j2, k2) != (0, 0, 0, 0) )
    a = Quaternion(r1, i1, j1, k1)
    b = Quaternion(r2, i2, j2, k2)
    fd = a // b
    m = a % b
    assert type(fd) is Quaternion
    assert type(m) is Quaternion
    assert set(map(lambda x: x.denom, (fd).components)) == set([1])
    for c in ((a / b) - fd).components:
        assert 2 * abs(c) <= 1
    assert m.norm <= b.norm
    assert a == fd * b + m

#-----------------------------

@given(*coords(), *coords()[:2])
def test_floordiv_and_mod_quadratic(r1, i1, j1, k1, r2, i2):
    assume( (r1, i1, j1, k1) != (0, 0, 0, 0) )
    assume( (r2, i2) != (0, 0) )
    a = Quaternion(r1, i1, j1, k1)
    b = Quadratic(r2, i2, -1)
    fds = a // b, b // a
    ms = a % b, b % a
    for fd in fds:
        assert type(fd) is Quaternion
    for m in ms:
        assert type(m) is Quaternion
    assert fds == (a // Quaternion(r2, i2, 0, 0), Quaternion(r2, i2, 0, 0) // a)
    assert ms == (a % Quaternion(r2, i2, 0, 0), Quaternion(r2, i2, 0, 0) % a)
    assert a == fds[0] * b + ms[0]
    assert b == fds[1] * a + ms[1]

#-----------------------------

@given(*coords(), *coords()[:2])
def test_floordiv_and_mod_quadratic_integer(r1, i1, j1, k1, r2, i2):
    assume( (r1, i1, j1, k1) != (0, 0, 0, 0) )
    assume( (r2, i2) != (0, 0) )
    a = Quaternion(r1, i1, j1, k1)
    b = QuadraticInteger(r2, i2, -1)
    fds = a // b, b // a
    ms = a % b, b % a
    for fd in fds:
        assert type(fd) is Quaternion
    for m in ms:
        assert type(m) is Quaternion
    assert fds == (a // Quaternion(r2, i2, 0, 0), Quaternion(r2, i2, 0, 0) // a)
    assert ms == (a % Quaternion(r2, i2, 0, 0), Quaternion(r2, i2, 0, 0) % a)
    assert a == fds[0] * b + ms[0]
    assert b == fds[1] * a + ms[1]

#-----------------------------

@given(*coords(), st.integers().filter(lambda x: x != 0))
def test_floordiv_and_mod_integer(r, i, j, k, integer):
    assume( (r, i, j, k) != (0, 0, 0, 0) )
    a = Quaternion(r, i, j, k)
    b = integer
    assert type(a // b) is Quaternion
    assert type(b // a) is Quaternion
    assert type(a % b) is Quaternion
    assert type(b % a) is Quaternion
    assert a // b == a // Quaternion(b, 0, 0, 0)
    assert b // a == Quaternion(b, 0, 0, 0) // a
    assert a % b == a % Quaternion(b, 0, 0, 0)
    assert b % a == Quaternion(b, 0, 0, 0) % a
    assert a == (a // b) * b + (a % b)

#-----------------------------

@given(*coords(), *rational('nonzero'))
def test_floordiv_and_mod_rational(r, i, j, k, numer, denom):
    assume( (r, i, j, k) != (0, 0, 0, 0) )
    a = Quaternion(r, i, j, k)
    b = frac(numer, denom)
    assert type(a // b) is Quaternion
    assert type(b // a) is Quaternion
    assert type(a % b) is Quaternion
    assert type(b % a) is Quaternion
    assert a // b == a // Quaternion(b, 0, 0, 0)
    assert b // a == Quaternion(b, 0, 0, 0) // a
    assert a % b == a % Quaternion(b, 0, 0, 0)
    assert b % a == Quaternion(b, 0, 0, 0) % a
    assert a == (a // b) * b + (a % b)

#=============================

@given(
    *coords(),
    st.integers(min_value=-20, max_value=20),
    st.integers(min_value=-10, max_value=10)
)
def test_pow(r, i, j, k, m, n):
    q = Quaternion(r, i, j, k)
    assume( q.components != (0, 0, 0, 0) )
    assert( q**2 == q * q )
    assert( q**(-2) == (q * q).inverse )
    mth_power = q**m
    nth_power = q**n
    sum_power = q**(m + n)
    assert( mth_power * nth_power == sum_power )
    assert( sum_power / nth_power == mth_power )

