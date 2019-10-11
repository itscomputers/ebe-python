#   tests/types_quadratic_test.py
#===========================================================
import env
import itertools
import math
import pytest
from hypothesis import given, assume, strategies as st

from numth.basic import gcd, is_square
from numth.types import frac, Rational, Quadratic
from numth.types.quadratic_integer import *
#===========================================================

def root_filter(x):
    return x < 0 or not is_square(x)

#-----------------------------

def pair():
    return 2 * [st.integers()]

def coords(rmin=None, rmax=None):
    if rmin is not None and rmax is not None:
        rval = st.integers(min_value=rmin, max_value=rmax)
    elif rmin is not None:
        rval = st.integers(min_value=rmin)
    elif rmax is not None:
        rval = st.integers(max_value=rmax)
    else:
        rval = st.integers()
    return [*pair(), rval.filter(root_filter)]

def double_coords():
    return [*pair(), *pair(), st.integers().filter(root_filter)]

def rational():
    return [st.integers(), st.integers(min_value=1)]

#=============================

@given(*coords())
def test_to_quadratic(real, imag, root):
    a = QuadraticInteger(real, imag, root)
    b = a.to_quadratic
    assert a == b
    assert type(a) is QuadraticInteger
    assert type(b) is Quadratic
    assert set(map(type, b.signature)) == set([Rational])
    assert QuadraticInteger.from_quadratic(b).signature == a.signature

#=============================

@given(*pair())
def test_from_complex(real, imag):
    if abs(real) < 2**53 and abs(imag) < 2**53:
        a = QuadraticInteger.from_complex(complex(real, imag))
        assert type(a) is QuadraticInteger
        assert a == Quadratic.from_complex(complex(real, imag))

#-----------------------------

@given(*coords())
def test_from_components(real, imag, root):
    a = QuadraticInteger(real, imag, root)
    assert type(a.from_components(real, imag)) is QuadraticInteger
    assert a.from_components(real, imag) == a
    assert a.from_components(real, -imag) == a.conjugate
    assert a.from_components(-real, -imag) == -a

#=============================

@given(*coords())
def test_neg(real, imag, root):
    a = QuadraticInteger(real, imag, root)
    assert type(-a) is QuadraticInteger
    assert -a == -(a.to_quadratic)

#-----------------------------

@given(*coords())
def test_conjugate(real, imag, root):
    a = QuadraticInteger(real, imag, root)
    assert type(a.conjugate) is QuadraticInteger
    assert a.conjugate == (a.to_quadratic).conjugate

#-----------------------------

@given(*coords())
def test_norm(real, imag, root):
    a = QuadraticInteger(real, imag, root)
    assert type(a.norm) is int
    assert a.norm == (a.to_quadratic).norm

#-----------------------------

@given(*coords())
def test_inverse(real, imag, root):
    assume( real != 0 or imag != 0 )
    a = QuadraticInteger(real, imag, root)
    if a.norm in [1, -1]:
        assert type(a.inverse) is QuadraticInteger
    else:
        assert type(a.inverse) is Quadratic
    assert a.inverse == (a.to_quadratic).inverse

#-----------------------------

@given(*coords())
def test_round(real, imag, root):
    a = QuadraticInteger(real, imag, root)
    assert type(a.round) is QuadraticInteger
    assert a.round == a

#=============================

@given(*double_coords())
def test_add(real1, imag1, real2, imag2, root):
    a = QuadraticInteger(real1, imag1, root)
    b = QuadraticInteger(real2, imag2, root)
    z = a.to_quadratic + b.to_quadratic
    assert type(a + b) is QuadraticInteger
    assert type(b + a) is QuadraticInteger
    assert a + b == z
    assert b + a == z

#-----------------------------

@given(*double_coords())
def test_add_quadratic(real1, imag1, real2, imag2, root):
    a = QuadraticInteger(real1, imag1, root)
    b = Quadratic(real2, imag2, root)
    z = a.to_quadratic + b
    assert type(a + b) is Quadratic
    assert type(b + a) is Quadratic
    assert a + b == z
    assert b + a == z

#-----------------------------

@given(*coords(), st.integers())
def test_add_int(real, imag, root, integer):
    a = QuadraticInteger(real, imag, root)
    b = integer
    z = a.to_quadratic + b
    assert type(a + b) is QuadraticInteger
    assert type(b + a) is QuadraticInteger
    assert a + b == z
    assert b + a == z

#-----------------------------

@given(*coords(), *rational())
def test_add_rational(real, imag, root, numer, denom):
    a = QuadraticInteger(real, imag, root)
    b = frac(numer, denom)
    z = a.to_quadratic + b
    assert type(a + b) is Quadratic
    assert type(b + a) is Quadratic
    assert a + b == z
    assert b + a == z

#=============================

@given(*double_coords())
def test_sub(real1, imag1, real2, imag2, root):
    a = QuadraticInteger(real1, imag1, root)
    b = QuadraticInteger(real2, imag2, root)
    z = a.to_quadratic - b.to_quadratic
    assert type(a - b) is QuadraticInteger
    assert type(b - a) is QuadraticInteger
    assert a - b == z
    assert b - a == -z

#-----------------------------

@given(*double_coords())
def test_sub_quadratic(real1, imag1, real2, imag2, root):
    a = QuadraticInteger(real1, imag1, root)
    b = Quadratic(real2, imag2, root)
    z = a.to_quadratic - b
    assert type(a - b) is Quadratic
    assert type(b - a) is Quadratic
    assert a - b == z
    assert b - a == -z

#-----------------------------

@given(*coords(), st.integers())
def test_sub_int(real, imag, root, integer):
    a = QuadraticInteger(real, imag, root)
    b = integer
    z = a.to_quadratic - b
    assert type(a - b) is QuadraticInteger
    assert type(b - a) is QuadraticInteger
    assert a - b == z
    assert b - a == -z

#-----------------------------

@given(*coords(), *rational())
def test_sub_rational(real, imag, root, numer, denom):
    a = QuadraticInteger(real, imag, root)
    b = frac(numer, denom)
    z = a.to_quadratic - b
    assert type(a - b) is Quadratic
    assert type(b - a) is Quadratic
    assert a - b == z
    assert b - a == -z

#=============================

@given(*double_coords())
def test_mul(real1, imag1, real2, imag2, root):
    a = QuadraticInteger(real1, imag1, root)
    b = QuadraticInteger(real2, imag2, root)
    z = a.to_quadratic * b.to_quadratic
    assert type(a * b) is QuadraticInteger
    assert type(b * a) is QuadraticInteger
    assert a * b == z
    assert b * a == z

#-----------------------------

@given(*double_coords())
def test_mul_quadratic(real1, imag1, real2, imag2, root):
    a = QuadraticInteger(real1, imag1, root)
    b = Quadratic(real2, imag2, root)
    z = a.to_quadratic * b
    assert type(a * b) is Quadratic
    assert type(b * a) is Quadratic
    assert a * b == z
    assert b * a == z

#-----------------------------

@given(*coords(), st.integers())
def test_mul_int(real, imag, root, integer):
    a = QuadraticInteger(real, imag, root)
    b = integer
    z = a.to_quadratic * b
    assert type(a * b) is QuadraticInteger
    assert type(b * a) is QuadraticInteger
    assert a * b == z
    assert b * a == z

#-----------------------------

@given(*coords(), *rational())
def test_mul_rational(real, imag, root, numer, denom):
    a = QuadraticInteger(real, imag, root)
    b = frac(numer, denom)
    z = a.to_quadratic * b
    assert type(a * b) is Quadratic
    assert type(b * a) is Quadratic
    assert a * b == z
    assert b * a == z

#=============================

@given(*double_coords())
def test_div(real1, imag1, real2, imag2, root):
    assume(real1 != 0 or imag1 != 0)
    assume(real2 != 0 or imag2 != 0)
    a = QuadraticInteger(real1, imag1, root)
    b = QuadraticInteger(real2, imag2, root)
    z = a.to_quadratic / b.to_quadratic
    assert type(a / b) is Quadratic
    assert type(b / a) is Quadratic
    assert a / b == z
    assert b / a == z.inverse

#-----------------------------

@given(*double_coords())
def test_div_quadratic(real1, imag1, real2, imag2, root):
    assume(real1 != 0 or imag1 != 0)
    assume(real2 != 0 or imag2 != 0)
    a = QuadraticInteger(real1, imag1, root)
    b = Quadratic(real2, imag2, root)
    z = a.to_quadratic / b
    assert type(a / b) is Quadratic
    assert type(b / a) is Quadratic
    assert a / b == z
    assert b / a == z.inverse

#-----------------------------

@given(*coords(), st.integers().filter(lambda x: x != 0))
def test_div_int(real, imag, root, integer):
    assume(real != 0 or imag != 0)
    a = QuadraticInteger(real, imag, root)
    b = integer
    z = a.to_quadratic / b
    assert type(a / b) is Quadratic
    assert type(b / a) is Quadratic
    assert a / b == z
    assert b / a == z.inverse

#-----------------------------

@given(*coords(), *rational())
def test_div_rational(real, imag, root, numer, denom):
    assume(real != 0 or imag != 0)
    assume(numer != 0)
    a = QuadraticInteger(real, imag, root)
    b = frac(numer, denom)
    z = a.to_quadratic / b
    assert type(a / b) is Quadratic
    assert type(b / a) is Quadratic
    assert a / b == z
    assert b / a == z.inverse

#=============================

@given(*double_coords())
def test_floor_div(real1, imag1, real2, imag2, root):
    assume(real1 != 0 or imag1 != 0)
    assume(real2 != 0 or imag2 != 0)
    a = QuadraticInteger(real1, imag1, root)
    b = QuadraticInteger(real2, imag2, root)
    z = a.to_quadratic / b.to_quadratic
    assert type(a // b) is QuadraticInteger
    assert type(b // a) is QuadraticInteger
    assert a // b == z.round
    assert b // a == z.inverse.round

#-----------------------------

@given(*double_coords())
def test_floor_div_quadratic(real1, imag1, real2, imag2, root):
    assume(real1 != 0 or imag1 != 0)
    assume(real2 != 0 or imag2 != 0)
    a = QuadraticInteger(real1, imag1, root)
    b = Quadratic(real2, imag2, root)
    z = a.to_quadratic / b
    assert type(a // b) is QuadraticInteger
    assert type(b // a) is QuadraticInteger
    assert a // b == z.round
    assert b // a == z.inverse.round

#-----------------------------

@given(*coords(), st.integers().filter(lambda x: x != 0))
def test_floor_div_int(real, imag, root, integer):
    assume(real != 0 or imag != 0)
    a = QuadraticInteger(real, imag, root)
    b = integer
    z = Quadratic(real // b, imag // b, root)
    y = (b / a.to_quadratic).round
    assert type(a // b) is QuadraticInteger
    assert type(b // a) is QuadraticInteger
    assert a // b == z
    assert b // a == y

#-----------------------------

@given(*coords(), *rational())
def test_floor_div_rational(real, imag, root, numer, denom):
    assume(real != 0 or imag != 0)
    assume(numer != 0)
    a = QuadraticInteger(real, imag, root)
    b = frac(numer, denom)
    z = Quadratic(real // b, imag // b, root)
    y = (b / a.to_quadratic).round
    assert type(a // b) is QuadraticInteger
    assert type(b // a) is QuadraticInteger
    assert a // b == z
    assert b // a == y

#=============================

@given(*double_coords())
def test_mod(real1, imag1, real2, imag2, root):
    assume( real2 != 0 or imag2 != 0 )
    a = QuadraticInteger(real1, imag1, root)
    b = QuadraticInteger(real2, imag2, root)
    z = a.to_quadratic % b.to_quadratic
    assert type(a % b) is QuadraticInteger
    assert a % b == z

#-----------------------------

@given(*double_coords())
def test_mod_quadratic(real1, imag1, real2, imag2, root):
    assume( real1 != 0 or imag1 != 0 )
    assume( real2 != 0 or imag2 != 0 )
    a = QuadraticInteger(real1, imag1, root)
    b = Quadratic(real2, imag2, root)
    z = a.to_quadratic % b
    y = b % a.to_quadratic
    assert type(a % b) is Quadratic
    assert type(b % a) is Quadratic
    assert a % b == z
    assert b % a == y

#=============================

@given(*coords(), st.integers(min_value=-20, max_value=20))
def test_pow(real, imag, root, exponent):
    assume( real != 0 or imag != 0 )
    a = QuadraticInteger(real, imag, root)
    y = a ** exponent
    z = a.to_quadratic ** exponent
    if exponent >= 0 or a.norm in [1, -1]:
        assert type(y) is QuadraticInteger
    else:
        assert type(y) is Quadratic
    assert y == z

