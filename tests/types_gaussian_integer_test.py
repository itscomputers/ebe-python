#   tests/types_gaussian_integer_test.py
#===========================================================
import env
import itertools
import math
import pytest
from hypothesis import given, assume, strategies as st

from numth.basic import gcd, is_square
from numth.types import frac, Rational, Quadratic, QuadraticInteger
from numth.types.gaussian_integer import *
#===========================================================

def coords():
    return 2 * [st.integers()]

def double_coords():
    return [*coords(), *coords()]

def rational():
    return [st.integers(), st.integers(min_value=1)]

#=============================

@given(*coords())
def test_to_quadratic_integer(real, imag):
    a = GaussianInteger(real, imag)
    b = a.to_quadratic_integer
    assert a == b
    assert type(a) is GaussianInteger
    assert type(b) is QuadraticInteger
    assert set(map(type, b.signature)) == set([int])

#=============================

@given(*coords())
def test_to_quadratic(real, imag):
    a = GaussianInteger(real, imag)
    b = a.to_quadratic
    assert a == b
    assert type(a) is GaussianInteger
    assert type(b) is Quadratic
    assert set(map(type, b.signature)) == set([Rational])
    assert GaussianInteger.from_quadratic(b).signature == a.signature

#=============================

@given(*coords())
def test_from_complex(real, imag):
    if abs(real) < 2**53 and abs(imag) < 2**53:
        a = GaussianInteger.from_complex(complex(real, imag))
        assert type(a) is GaussianInteger
        assert a == Quadratic.from_complex(complex(real, imag))

#-----------------------------

@given(*coords())
def test_from_components(real, imag):
    a = GaussianInteger(real, imag)
    assert type(a.from_components(real, imag)) is GaussianInteger
    assert a.from_components(real, imag) == a
    assert a.from_components(real, -imag) == a.conjugate
    assert a.from_components(-real, -imag) == -a

#=============================

@given(*coords())
def test_neg(real, imag):
    a = GaussianInteger(real, imag)
    assert type(-a) is GaussianInteger
    assert -a == -(a.to_quadratic)

#-----------------------------

@given(*coords())
def test_conjugate(real, imag):
    a = GaussianInteger(real, imag)
    assert type(a.conjugate) is GaussianInteger
    assert a.conjugate == (a.to_quadratic).conjugate

#-----------------------------

@given(*coords())
def test_norm(real, imag):
    a = GaussianInteger(real, imag)
    assert type(a.norm) is int
    assert a.norm == (a.to_quadratic).norm

#-----------------------------

@given(*coords())
def test_inverse(real, imag):
    assume( real != 0 or imag != 0 )
    a = GaussianInteger(real, imag)
    if a.norm in [1, -1]:
        assert type(a.inverse) is GaussianInteger
    else:
        assert type(a.inverse) is Quadratic
    assert a.inverse == (a.to_quadratic).inverse

#-----------------------------

@given(*coords())
def test_round(real, imag):
    a = GaussianInteger(real, imag)
    assert type(a.round) is GaussianInteger
    assert a.round == a

#=============================

@given(*double_coords())
def test_add(real1, imag1, real2, imag2):
    a = GaussianInteger(real1, imag1)
    b = GaussianInteger(real2, imag2)
    z = a.to_quadratic + b.to_quadratic
    assert type(a + b) is GaussianInteger
    assert type(b + a) is GaussianInteger
    assert a + b == z
    assert b + a == z

#-----------------------------

@given(*double_coords())
def test_add_quadratic_integer(real1, imag1, real2, imag2):
    a = GaussianInteger(real1, imag1)
    b = QuadraticInteger(real2, imag2, -1)
    z = a.to_quadratic + b
    assert type(a + b) is GaussianInteger
    assert type(b + a) is GaussianInteger
    assert a + b == z
    assert b + a == z
    
#-----------------------------

@given(*double_coords())
def test_add_quadratic(real1, imag1, real2, imag2):
    a = GaussianInteger(real1, imag1)
    b = Quadratic(real2, imag2, -1)
    z = a.to_quadratic + b
    assert type(a + b) is Quadratic
    assert type(b + a) is Quadratic
    assert a + b == z
    assert b + a == z

#-----------------------------

@given(*coords(), st.integers())
def test_add_int(real, imag, integer):
    a = GaussianInteger(real, imag)
    b = integer
    z = a.to_quadratic + b
    assert type(a + b) is GaussianInteger
    assert type(b + a) is GaussianInteger
    assert a + b == z
    assert b + a == z

#-----------------------------

@given(*coords(), *rational())
def test_add_rational(real, imag, numer, denom):
    a = GaussianInteger(real, imag)
    b = frac(numer, denom)
    z = a.to_quadratic + b
    assert type(a + b) is Quadratic
    assert type(b + a) is Quadratic
    assert a + b == z
    assert b + a == z

#=============================

@given(*double_coords())
def test_sub(real1, imag1, real2, imag2):
    a = GaussianInteger(real1, imag1)
    b = GaussianInteger(real2, imag2)
    z = a.to_quadratic - b.to_quadratic 
    assert type(a - b) is GaussianInteger
    assert type(b - a) is GaussianInteger
    assert a - b == z
    assert b - a == -z

#-----------------------------

@given(*double_coords())
def test_sub_quadratic_integer(real1, imag1, real2, imag2):
    a = GaussianInteger(real1, imag1)
    b = QuadraticInteger(real2, imag2, -1)
    z = a.to_quadratic - b
    assert type(a - b) is GaussianInteger
    assert type(b - a) is GaussianInteger
    assert a - b == z
    assert b - a == -z
    
#-----------------------------

@given(*double_coords())
def test_sub_quadratic(real1, imag1, real2, imag2):
    a = GaussianInteger(real1, imag1)
    b = Quadratic(real2, imag2, -1)
    z = a.to_quadratic - b 
    assert type(a - b) is Quadratic
    assert type(b - a) is Quadratic
    assert a - b == z
    assert b - a == -z

#-----------------------------

@given(*coords(), st.integers())
def test_sub_int(real, imag, integer):
    a = GaussianInteger(real, imag)
    b = integer
    z = a.to_quadratic - b
    assert type(a - b) is GaussianInteger
    assert type(b - a) is GaussianInteger
    assert a - b == z
    assert b - a == -z

#-----------------------------

@given(*coords(), *rational())
def test_sub_rational(real, imag, numer, denom):
    a = GaussianInteger(real, imag)
    b = frac(numer, denom)
    z = a.to_quadratic - b
    assert type(a - b) is Quadratic
    assert type(b - a) is Quadratic
    assert a - b == z
    assert b - a == -z

#=============================

@given(*double_coords())
def test_mul(real1, imag1, real2, imag2):
    a = GaussianInteger(real1, imag1)
    b = GaussianInteger(real2, imag2)
    z = a.to_quadratic * b.to_quadratic
    assert type(a * b) is GaussianInteger
    assert type(b * a) is GaussianInteger
    assert a * b == z
    assert b * a == z

#-----------------------------

@given(*double_coords())
def test_mul_quadratic_integer(real1, imag1, real2, imag2):
    a = GaussianInteger(real1, imag1)
    b = QuadraticInteger(real2, imag2, -1)
    z = a.to_quadratic * b
    assert type(a * b) is GaussianInteger
    assert type(b * a) is GaussianInteger
    assert a * b == z
    assert b * a == z
    
#-----------------------------

@given(*double_coords())
def test_mul_quadratic(real1, imag1, real2, imag2):
    a = GaussianInteger(real1, imag1)
    b = Quadratic(real2, imag2, -1)
    z = a.to_quadratic * b
    assert type(a * b) is Quadratic
    assert type(b * a) is Quadratic
    assert a * b == z
    assert b * a == z

#-----------------------------

@given(*coords(), st.integers())
def test_mul_int(real, imag, integer):
    a = GaussianInteger(real, imag)
    b = integer
    z = a.to_quadratic * b
    assert type(a * b) is GaussianInteger
    assert type(b * a) is GaussianInteger
    assert a * b == z
    assert b * a == z

#-----------------------------

@given(*coords(), *rational())
def test_mul_rational(real, imag, numer, denom):
    a = GaussianInteger(real, imag)
    b = frac(numer, denom)
    z = a.to_quadratic * b
    assert type(a * b) is Quadratic
    assert type(b * a) is Quadratic
    assert a * b == z
    assert b * a == z

#=============================

@given(*double_coords())
def test_div(real1, imag1, real2, imag2):
    assume(real1 != 0 or imag1 != 0)
    assume(real2 != 0 or imag2 != 0)
    a = GaussianInteger(real1, imag1)
    b = GaussianInteger(real2, imag2)
    z = a.to_quadratic / b.to_quadratic 
    assert type(a / b) is Quadratic
    assert type(b / a) is Quadratic
    assert a / b == z
    assert b / a == z.inverse

#-----------------------------

@given(*double_coords())
def test_div_quadratic_integer(real1, imag1, real2, imag2):
    assume(real1 != 0 or imag1 != 0)
    assume(real2 != 0 or imag2 != 0)
    a = GaussianInteger(real1, imag1)
    b = QuadraticInteger(real2, imag2, -1)
    z = a.to_quadratic / b
    assert type(a / b) is Quadratic 
    assert type(b / a) is Quadratic
    assert a / b == z
    assert b / a == z.inverse
    
#-----------------------------

@given(*double_coords())
def test_div_quadratic(real1, imag1, real2, imag2):
    assume(real1 != 0 or imag1 != 0)
    assume(real2 != 0 or imag2 != 0)
    a = GaussianInteger(real1, imag1)
    b = Quadratic(real2, imag2, -1)
    z = a.to_quadratic / b 
    assert type(a / b) is Quadratic
    assert type(b / a) is Quadratic
    assert a / b == z
    assert b / a == z.inverse

#-----------------------------

@given(*coords(), st.integers().filter(lambda x: x != 0))
def test_div_int(real, imag, integer):
    assume(real != 0 or imag != 0)
    a = GaussianInteger(real, imag)
    b = integer
    z = a.to_quadratic / b 
    assert type(a / b) is Quadratic
    assert type(b / a) is Quadratic
    assert a / b == z
    assert b / a == z.inverse

#-----------------------------

@given(*coords(), *rational())
def test_div_rational(real, imag, numer, denom):
    assume(real != 0 or imag != 0)
    assume(numer != 0)
    a = GaussianInteger(real, imag)
    b = frac(numer, denom)
    z = a.to_quadratic / b 
    assert type(a / b) is Quadratic
    assert type(b / a) is Quadratic
    assert a / b == z
    assert b / a == z.inverse

#=============================

@given(*double_coords())
def test_floor_div(real1, imag1, real2, imag2):
    assume(real1 != 0 or imag1 != 0)
    assume(real2 != 0 or imag2 != 0)
    a = GaussianInteger(real1, imag1)
    b = GaussianInteger(real2, imag2)
    z = a.to_quadratic / b.to_quadratic
    assert type(a // b) is GaussianInteger
    assert type(b // a) is GaussianInteger
    assert a // b == z.round
    assert b // a == z.inverse.round

#-----------------------------

@given(*double_coords())
def test_floor_div_quadratic_integer(real1, imag1, real2, imag2):
    assume(real1 != 0 or imag1 != 0)
    assume(real2 != 0 or imag2 != 0)
    a = GaussianInteger(real1, imag1)
    b = QuadraticInteger(real2, imag2, -1)
    z = a.to_quadratic / b
    assert type(a // b) is GaussianInteger
    assert type(b // a) is GaussianInteger
    assert a // b == z.round
    assert b // a == z.inverse.round

#-----------------------------

@given(*double_coords())
def test_floor_div_quadratic(real1, imag1, real2, imag2):
    assume(real1 != 0 or imag1 != 0)
    assume(real2 != 0 or imag2 != 0)
    a = GaussianInteger(real1, imag1)
    b = Quadratic(real2, imag2, -1)
    z = a.to_quadratic / b
    assert type(a // b) is GaussianInteger
    assert type(b // a) is GaussianInteger
    assert a // b == z.round
    assert b // a == z.inverse.round

#-----------------------------

@given(*coords(), st.integers().filter(lambda x: x != 0))
def test_floor_div_int(real, imag, integer):
    assume(real != 0 or imag != 0)
    a = GaussianInteger(real, imag)
    b = integer
    z = Quadratic(real // b, imag // b, -1)
    y = (b / a.to_quadratic).round
    assert type(a // b) is GaussianInteger
    assert type(b // a) is GaussianInteger
    assert a // b == z
    assert b // a == y

#-----------------------------

@given(*coords(), *rational())
def test_floor_div_rational(real, imag, numer, denom):
    assume(real != 0 or imag != 0)
    assume(numer != 0)
    a = GaussianInteger(real, imag)
    b = frac(numer, denom)
    z = Quadratic(real // b, imag // b, -1)
    y = (b / a.to_quadratic).round
    assert type(a // b) is GaussianInteger
    assert type(b // a) is GaussianInteger
    assert a // b == z
    assert b // a == y

#=============================

@given(*double_coords())
def test_mod(real1, imag1, real2, imag2):
    assume( real2 != 0 or imag2 != 0 )
    a = GaussianInteger(real1, imag1)
    b = GaussianInteger(real2, imag2)
    z = a.to_quadratic % b.to_quadratic
    assert type(a % b) is GaussianInteger
    assert a % b == z
    
#-----------------------------

@given(*double_coords())
def test_mod_quadratic(real1, imag1, real2, imag2):
    assume( real1 != 0 or imag1 != 0 )
    assume( real2 != 0 or imag2 != 0 )
    a = GaussianInteger(real1, imag1)
    b = Quadratic(real2, imag2, -1)
    z = a.to_quadratic % b 
    y = b % a.to_quadratic
    assert type(a % b) is Quadratic
    assert type(b % a) is Quadratic
    assert a % b == z
    assert b % a == y

#=============================

@given(*coords(), st.integers(min_value=-20, max_value=20))
def test_pow(real, imag, exponent):
    assume( real != 0 or imag != 0 )
    a = GaussianInteger(real, imag)
    y = a ** exponent
    z = a.to_quadratic ** exponent
    if exponent >= 0 or a.norm in [1, -1]:
        assert type(y) is GaussianInteger
    else:
        assert type(y) is Quadratic
    assert y == z

#=============================

@given(*coords())
def test_canonical(real, imag):
    a = GaussianInteger(real, imag)
    z = a.canonical
    assert z.real >= abs(z.imag)

#=============================

@given(*double_coords())
def test_gcd(real1, imag1, real2, imag2):
    assume( real1 != 0 or imag1 != 0)
    assume( real2 != 0 or imag2 != 0)
    a = GaussianInteger(real1, imag1)
    b = GaussianInteger(real2, imag2)
    z = a.gcd(b)
    assert a % z == b % z == GaussianInteger(0, 0)
    assert (a // z).gcd(b // z) == GaussianInteger(1, 0)

