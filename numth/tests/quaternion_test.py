#   test_quadratic.py
#===========================================================
from hypothesis import given, assume, strategies as st

from ..types import Rational
from ..types.quaternion import *
#===========================================================

def coords():
    return 4 * [st.integers()]

def rational(flag=None):
    if flag == 'nonzero':
        return [st.integers().filter(lambda x: x != 0),
                st.integers(min_value=1)]
    return [st.integers(), st.integers(min_value=1)]

#=============================

@given(*coords())
def test_norm(r, i, j, k):
    q = Quaternion(r, i, j, k)
    assert( q.norm() == r**2 + i**2 + j**2 + k**2 )
    assert( q * q.conjugate() == Quaternion(q.norm(), 0, 0, 0) )

#-----------------------------

@given(*coords())
def test_conjugate(r, i, j, k):
    q = Quaternion(r, i, j, k)
    assert( q.conjugate().components == (q.r, -q.i, -q.j, -q.k) )
    assert( q + q.conjugate() == Quaternion(2*r, 0, 0, 0) )
    assert( q - q.conjugate() == Quaternion(0, 2*i, 2*j, 2*k) )

#-----------------------------

@given(*coords())
def test_inverse(r, i, j, k):
    assume( (r, i, j, k) != (0, 0, 0, 0) )
    q = Quaternion(r, i, j, k)
    assert( q * q.inverse() == Quaternion(1, 0, 0, 0) )
    assert( q.inverse().inverse() == q )

#=============================

@given(*coords())
def test_neg(r, i, j, k):
    q = Quaternion(r, i, j, k)
    assert( (-q).components == tuple(-x for x in q.components) )
    assert( q + (-q) == -q + q == Quaternion(0, 0, 0, 0) )

#=============================

@given(*coords(), *coords())
def test_add(r1, i1, j1, k1, r2, i2, j2, k2):
    q1 = Quaternion(r1, i1, j1, k1)
    q2 = Quaternion(r2, i2, j2, k2)
    s = Quaternion(r1 + r2, i1 + i2, j1 + j2, k1 + k2)
    assert( q1 + q2 == s )
    assert( q2 + q1 == s )

#-----------------------------

@given(*coords(), *rational())
def test_add_quaternion_and_number(r, i, j, k, numer, denom):
    q = Quaternion(r, i, j, k)
    s = Quaternion(r + numer, i, j, k)
    t = Quaternion(r + Rational(numer, denom), i, j, k)
    assert( q + numer == s )
    assert( numer + q == s )
    assert( q + Rational(numer, denom) == t )
    assert( Rational(numer, denom) + q == t )

#=============================

@given(*coords(), *coords())
def test_sub(r1, i1, j1, k1, r2, i2, j2, k2):
    q1 = Quaternion(r1, i1, j1, k1)
    q2 = Quaternion(r2, i2, j2, k2)
    s = Quaternion(r1 - r2, i1 - i2, j1 - j2, k1 - k2)
    assert( q1 - q2 == s )
    assert( q2 - q1 == -s )

#-----------------------------

@given(*coords(), *rational())
def test_sub_quaternion_and_number(r, i, j, k, numer, denom):
    q = Quaternion(r, i, j, k)
    s = Quaternion(r - numer, i, j, k)
    t = Quaternion(r - Rational(numer, denom), i, j, k)
    assert( q - numer == s )
    assert( numer - q == -s )
    assert( q - Rational(numer, denom) == t )
    assert( Rational(numer, denom) - q == -t )

#=============================

@given(*coords(), *coords())
def test_mul(r1, i1, j1, k1, r2, i2, j2, k2):
    q1 = Quaternion(r1, i1, j1, k1)
    q2 = Quaternion(r2, i2, j2, k2)
    s = Quaternion(
        r1*r2 - i1*i2 - j1*j2 - k1*k2,
        r1*i2 + i1*r2 + j1*k2 - k1*j2,
        r1*j2 - i1*k2 + j1*r2 + k1*i2,
        r1*k2 + i1*j2 - j1*i2 + k1*r2
    )
    assert( q1 * q2 == s )

#-----------------------------

@given(*coords(), *rational())
def test_mul_quaternion_and_number(r, i, j, k, numer, denom):
    q = Quaternion(r, i, j, k)
    s = Quaternion(r * numer, i * numer, j * numer, k * numer)
    t = Quaternion(
        r * Rational(numer, denom),
        i * Rational(numer, denom),
        j * Rational(numer, denom),
        k * Rational(numer, denom)
    )
    assert( q * numer == s )
    assert( numer * q == s )
    assert( q * Rational(numer, denom) == t )
    assert( Rational(numer, denom) * q == t )

#=============================

@given(*coords(), *coords())
def test_div(r1, i1, j1, k1, r2, i2, j2, k2):
    q1 = Quaternion(r1, i1, j1, k1)
    q2 = Quaternion(r2, i2, j2, k2)
    assume( q1.components != (0, 0, 0, 0) )
    assume( q2.components != (0, 0, 0, 0) )
    q2_norm = q2.norm()
    s = Quaternion(
        Rational(r1*r2 + i1*i2 + j1*j2 + k1*k2, q2_norm),
        Rational(-r1*i2 + i1*r2 - j1*k2 + k1*j2, q2_norm),
        Rational(-r1*j2 + i1*k2 + j1*r2 - k1*i2, q2_norm),
        Rational(-r1*k2 - i1*j2 + j1*i2 + k1*r2, q2_norm)
    )
    assert( q1 / q2 == s )
    assert( q2 / q1 == s.inverse() )

#-----------------------------

@given(*coords(), *rational('nonzero'))
def test_div_quaternion_and_number(r, i, j, k, numer, denom):
    q = Quaternion(r, i, j, k)
    assume( q.components != (0, 0, 0, 0) )
    s = Quaternion(
        Rational(r, numer),
        Rational(i, numer),
        Rational(j, numer),
        Rational(k, numer)
    )
    t = Quaternion(
        r / Rational(numer, denom),
        i / Rational(numer, denom),
        j / Rational(numer, denom),
        k / Rational(numer, denom)
    )
    assert( q / numer == s )
    assert( numer / q == s.inverse() )
    assert( q / Rational(numer, denom) == t )
    assert( Rational(numer, denom) / q == t.inverse() )

#=============================

@given(*coords(), *coords())
def test_floordiv(r1, i1, j1, k1, r2, i2, j2, k2):
    q1 = Quaternion(r1, i1, j1, k1)
    q2 = Quaternion(r2, i2, j2, k2)
    assume( q2.components != (0, 0, 0, 0) )
    q2_norm = q2.norm()
    s = Quaternion(
        (r1*r2 + i1*i2 + j1*j2 + k1*k2) // q2_norm,
        (-r1*i2 + i1*r2 - j1*k2 + k1*j2) // q2_norm,
        (-r1*j2 + i1*k2 + j1*r2 - k1*i2) // q2_norm,
        (-r1*k2 - i1*j2 + j1*i2 + k1*r2) // q2_norm
    )
    assert( q1 // q2 == s )

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
    assert( q**(-2) == (q * q).inverse() )
    mth_power = q**m
    nth_power = q**n
    sum_power = q**(m + n)
    assert( mth_power * nth_power == sum_power )
    assert( sum_power / nth_power == mth_power )

#=============================

@given(*coords(), *coords())
def test_mod(r1, i1, j1, k1, r2, i2, j2, k2):
    q1 = Quaternion(r1, i1, j1, k1)
    q2 = Quaternion(r2, i2, j2, k2)
    assume( q2.components != (0, 0, 0, 0) )
    assert( q1 == (q1 // q2) * q2 + (q1 % q2) )

#-----------------------------

@given(*coords(), st.integers(min_value=1))
def test_mod_quaternion_and_integer(r, i, j, k, integer):
    q = Quaternion(r, i, j, k)
    assume( q.components != (0, 0, 0, 0) )
    mod_components = map(
        lambda x: x - integer * (2*x > integer),
        map(
            lambda x: x % integer, 
            q.components
        )
    )
    r = Quaternion(*mod_components)
    assert( q % integer == r )
    assert( integer % q == Quaternion(integer, 0, 0, 0) % q )

