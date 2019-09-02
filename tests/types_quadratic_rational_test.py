#   tests/types_quadratic_rational_test.py
#===========================================================
import env
from hypothesis import given, assume, strategies as st
import math

from numth.basic import is_square
from numth.types import frac
from numth.types.quadratic_rational import *
#===========================================================

def root_filter(x):
    return x < 0 or not is_square(x)

def nonzero(x):
    return x != 0

def positive(x):
    return x > 0

def rational():
    return (st.integers(), st.integers().filter(positive))

def components(real_filter=None, imag_filter=None):
    if real_filter:
        real = st.integers().filter(real_filter)
    else:
        real = st.integers()

    if imag_filter:
        imag = st.integers().filter(imag_filter)
    else:
        imag = st.integers()

    return (real, imag, st.integers().filter(root_filter)) 

def coords(real_filter=None, imag_filter=None):
    return (
        *components(real_filter, imag_filter),
        st.integers().filter(root_filter)
    )

def double_coords():
    return (*(2 * components()), st.integers().filter(root_filter))

#===========================================================

@given(*coords())
def test_norm_conjugate(r, i, d, root):
    a = QuadraticRational(r, i, d, root)
    assert a * a.conjugate == QuadraticRational(a._norm, 0, a._denom**2, a.root)
    assert a + a.conjugate == QuadraticRational(2 * a._real, 0, a._denom, a.root)
    assert a - a.conjugate == QuadraticRational(0, 2 * a._imag, a._denom, a.root)

#-----------------------------

@given(*coords(nonzero, nonzero))
def test_inverse(r, i, d, root):
    a = QuadraticRational(r, i, d, root)
    assert a * a.inverse == 1
    assert (a.inverse).inverse == a

#-----------------------------

@given(*coords())
def test_neg(r, i, d, root):
    a = QuadraticRational(r, i, d, root)
    assert a + -a == -a + a == 0
    assert -(-a) == a
    assert -a == -1 * a

#-----------------------------

@given(*double_coords())
def test_add(r, i, d, R, I, D, root):
    a = QuadraticRational(r, i, d, root)
    A = QuadraticRational(R, I, D, root)
    s = a + A
    assert s.real == a.real + A.real
    assert s.imag == a.imag + A.imag
    assert s == A + a

@given(*coords(), *rational())
def test_add_number(r, i, d, root, numer, denom):
    a = QuadraticRational(r, i, d, root)
    b = frac(numer, denom)
    s = a + b
    S = a + numer
    assert s.real == a.real + b
    assert s.imag == a.imag
    assert S.real == a.real + numer
    assert S.imag == a.imag
    assert s == b + a
    assert S == numer + a

#-----------------------------

@given(*double_coords())
def test_sub(r, i, d, R, I, D, root):
    a = QuadraticRational(r, i, d, root)
    A = QuadraticRational(R, I, D, root)
    s = a - A
    assert s.real == a.real - A.real
    assert s.imag == a.imag - A.imag
    assert -s == A - a

@given(*coords(), *rational())
def test_sub_number(r, i, d, root, numer, denom):
    a = QuadraticRational(r, i, d, root)
    b = frac(numer, denom)
    s = a - b
    S = a - numer
    assert s.real == a.real - b
    assert s.imag == a.imag
    assert S.real == a.real - numer
    assert S.imag == a.imag
    assert -s == b - a
    assert -S == numer - a

#-----------------------------

@given(*double_coords())
def test_mul(r, i, d, R, I, D, root):
    a = QuadraticRational(r, i, d, root)
    A = QuadraticRational(R, I, D, root)
    s = a * A
    assert s.real == a.real * A.real + a.imag * A.imag * root
    assert s.imag == a.real * A.imag + a.imag * A.real
    assert s == A * a

@given(*coords(), *rational())
def test_mul_number(r, i, d, root, numer, denom):
    a = QuadraticRational(r, i, d, root)
    b = frac(numer, denom)
    s = a * b
    S = a * numer
    assert s.real == a.real * b
    assert s.imag == a.imag * b
    assert S.real == a.real * numer
    assert S.imag == a.imag * numer
    assert s == b * a
    assert S == numer * a

#-----------------------------

@given(*double_coords())
def test_truediv(r, i, d, R, I, D, root):
    assume( (r, i) != (0, 0) and (R, I) != (0, 0) )
    a = QuadraticRational(r, i, d, root)
    A = QuadraticRational(R, I, D, root)
    s = a / A
    assert s == a * (A.inverse)
    assert s.inverse == A / a
    assert s.inverse == (a.inverse) * A

@given(*coords(), *rational())
def test_truediv_number(r, i, d, root, numer, denom):
    assume( (r, i) != (0, 0) and numer != 0 )
    a = QuadraticRational(r, i, d, root)
    b = frac(numer, denom)
    s = a / b
    S = a / numer
    assert s.real == a.real / b
    assert s.imag == a.imag / b
    assert S.real == a.real / numer
    assert S.imag == a.imag / numer
    assert s == a * b.inverse()
    assert s.inverse == b / a
    assert s.inverse == b * a.inverse
    assert S == a * frac(1, numer)
    assert S.inverse == numer / a
    assert S.inverse == numer * a.inverse

