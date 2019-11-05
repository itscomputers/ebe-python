#   tests/types_polynomial_test.py
#===========================================================
import env
from hypothesis import assume, given, strategies as st

from lib.basic import is_square, lcm
from lib.types import Rational, QuadraticInteger
from lib.types.polynomial import *
from lib.types.polynomial import (
    _term_pattern,
    _term_to_exp_coeff,
    _exp_coeff_to_term,
    _args_to_polyn
)
#===========================================================

def coords(n, coeff_filter=lambda x: True, exp_min=0, exp_max=30, coeff_min=None, coeff_max=None):
    return (x for y in \
            n * [(
                st.integers(min_value=exp_min, max_value=exp_max),
                st.integers(min_value=coeff_min, max_value=coeff_max).filter(coeff_filter)
            )] for x in y)

#-----------------------------

def nonzero(num):
    return num != 0

#-----------------------------

def are_distinct(*args):
    if len(args) < 2:
        return True
    return args[0] not in args[1:] and are_distinct(*args[1:])

#-----------------------------

def make(*args):
    return Polynomial({args[i]: args[i+1] for i in range(0, len(args), 2)})

#=============================

@given(*coords(1, nonzero))
def test_term_pattern_and_term_to_exp_coeff(e, c):
    pattern = _term_pattern()

    string = '{}t^{}'.format(c, e)
    term = pattern.match(string).group(1,2,3)
    assert( term == (str(c), 't', '^{}'.format(e)) )
    assert( _term_to_exp_coeff(*term) == (e, c) )

    string = '{}*u^{}'.format(c, e)
    term = pattern.match(string).group(1,2,3)
    assert( term == (str(c), '*u', '^{}'.format(e)) )
    assert( _term_to_exp_coeff(*term) == (e, c) )

    string = '-v^{}'.format(e)
    term = pattern.match(string).group(1,2,3)
    assert( term == ('-', 'v', '^{}'.format(e)) )
    assert( _term_to_exp_coeff(*term) == (e, -1) )

    string = '+w^{}'.format(e)
    term = pattern.match(string).group(1,2,3)
    assert( term == ('+', 'w', '^{}'.format(e)) )
    assert( _term_to_exp_coeff(*term) == (e, 1) )

    string = 'x^{}'.format(e)
    term = pattern.match(string).group(1,2,3)
    assert( term == ('', 'x', '^{}'.format(e)) )
    assert( _term_to_exp_coeff(*term) == (e, 1) )

    string = '0y^{}'.format(e)
    term = pattern.match(string).group(1,2,3)
    assert( term == ('0', 'y', '^{}'.format(e)) )
    assert( _term_to_exp_coeff(*term) == (e, 0) )

    string = '0*z^{}'.format(e)
    term = pattern.match(string).group(1,2,3)
    assert( term == ('0', '*z', '^{}'.format(e)) )
    assert( _term_to_exp_coeff(*term) == (e, 0) )

    string = '{}'.format(c)
    term = pattern.match(string).group(1,2,3)
    assert( term == (str(c), None, None) )
    assert( _term_to_exp_coeff(*term) == (0, c) )

    string = '0'
    term = pattern.match(string).group(1,2,3)
    assert( term == ('0', None, None) )
    assert( _term_to_exp_coeff(*term) == (0, 0) )

#-----------------------------

@given(*coords(1, coeff_filter=lambda x: x not in [-1, 0, 1], exp_min=2))
def test_exp_coeff_to_term(e, c):
    assert( _exp_coeff_to_term(e, c) == '{}x^{}'.format(c, e) )
    assert( _exp_coeff_to_term(e, 1) == 'x^{}'.format(e) )
    assert( _exp_coeff_to_term(e, -1) == '-x^{}'.format(e) )
    assert( _exp_coeff_to_term(1, c) == '{}x'.format(c) )
    assert( _exp_coeff_to_term(1, 1) == 'x' )
    assert( _exp_coeff_to_term(1, -1) == '-x' )
    assert( _exp_coeff_to_term(0, c) == str(c) )
    assert( _exp_coeff_to_term(0, 1) == '1' )
    assert( _exp_coeff_to_term(0, -1) == '-1' )
    assert( _exp_coeff_to_term(0, 0) == '0' )

#-----------------------------

@given(*coords(1, nonzero))
def test_args_to_polyn(e, c):
    args = [0] * e + [c]
    assert( _args_to_polyn(*args).coeffs == {e: c} )

#-----------------------------

@given(*coords(2))
def test_polyn(e1, c1, e2, c2):
    assume( are_distinct(e1, e2) )
    p1 = make(e1, c1, e2, c2)
    p2 = polyn((e1, c1), (e2, c2))
    if c2 >= 0:
        p3 = polyn('{}x^{} + {}x^{}'.format(c1, e1, c2, e2))
    else:
        p3 = polyn('{}x^{} {}x^{}'.format(c1, e1, c2, e2))
    assert( p1 == p2 )
    assert( p2 == p3 )

#=============================

@given(*coords(2), *coords(1, exp_min=1))
def test_polyn_int_div(e1, c1, e2, c2, e3, c4):
    assume( are_distinct(e1, e2) )
    p1 = make(e1, c1, e2, c2)
    p2 = make(e3, 1, 0, c4)
    q, r = polyn_div(p1, p2)
    assert( r.degree < p2.degree )
    assert( p1 == q * p2 + r )

#-----------------------------

@given(*coords(2), *coords(2, nonzero))
def test_polyn_rational_div(e1, c1, e2, c2, e3, c3, e4, c4):
    assume( are_distinct(e1, e2) and are_distinct(e3, e4) )
    p1 = make(e1, c1, e2, c2)
    p2 = make(e3, c3, e4, c4)
    q, r = polyn_div(p1, p2, Rational)
    assert( r.degree < p2.degree )
    assert( p1 == q * p2 + r )

#=============================

@given(*coords(3))
def test_repr(e1, c1, e2, c2, e3, c3):
    assume( are_distinct(e1, e2, e3) )
    p1 = make(e1, c1, e2, c2, e3, c3)
    assert( polyn(repr(p1)) == p1 )

#=============================

@given(*coords(3, nonzero))
def test_degree_and_leading_coeff(e1, c1, e2, c2, e3, c3):
    assume( are_distinct(e1, e2, e3) )
    (e1, c1), (e2, c2), (e3, c3) = sorted([(e1, c1), (e2, c2), (e3, c3)])
    p1 = make(e1, c1, e2, c2, e3, c3)
    p2 = make(e1, c1, e2, c2, e3, 0)
    p3 = make(e1, c1, e2, 0, e3, 0)
    p4 = make(e1, 0, e2, 0, e3, 0)
    assert( p1.degree == e3 )
    assert( p1.leading_coeff == c3 )
    assert( p2.degree == e2 )
    assert( p2.leading_coeff == c2 )
    assert( p3.degree == e1 )
    assert( p3.leading_coeff == c1 )
    assert( p4.degree == -1 )
    assert( p4.leading_coeff == 0 )

#-----------------------------

@given(*coords(1, nonzero))
def test_full_coeffs(e, c):
    p = make(e, c)
    full_coeffs = {_e: 0 for _e in range(e)}
    full_coeffs[e] = c
    assert( p._full_coeffs() == full_coeffs )

#=============================

@given(*coords(2))
def test_neg(e1, c1, e2, c2):
    p = make(e1, c1, e2, c2)
    q = make(e1, -c1, e2, -c2)
    assert( -p == q )
    assert( p == -q )
    assert( p + -p == polyn(0) )
    assert( p * -q == -p * q == -(p * q) )
    assert( -p == polyn(-1) * p )

#-----------------------------

@given(*coords(2))
def test_canonical(e1, c1, e2, c2):
    p = make(e1, c1, e2, c2)
    assert( p.canonical().leading_coeff >= 0 )

#-----------------------------

@given(
    st.integers(min_value=0),
    st.integers(min_value=1),
    st.integers(min_value=2),
    st.integers(min_value=1),
    st.integers(min_value=1),
    st.integers(min_value=2),
    st.integers(min_value=2),
    st.integers(min_value=1),
    st.integers(min_value=2),
)
def test_to_integer_polyn(e1, n1, d1, e2, n2, d2, e3, n3, d3):
    assume( are_distinct(e1, e2, e3) )
    p = make(e1, Rational(n1, d1), e2, Rational(n2, d2), e3, Rational(n3, d3))
    q = p.to_integer_polyn()
    m = lcm(*(c.denom for c in p.coeffs.values()))
    for c in q.coeffs.values():
        assert( type(c) is int )
    assert( q / m == p )

#=============================

@given(*coords(2))
def test_add(e1, c1, e2, c2):
    p1 = make(e1, c1)
    p2 = make(e2, c2)
    if e1 == e2:
        s1 = make(e1, c1 + c2)
    else:
        s1 = make(e1, c1, e2, c2)
    if c2 >= 0:
        s2 = polyn('+'.join((repr(p1), repr(p2))))
    else:
        s2 = polyn(''.join((repr(p1), repr(p2))))
    assert( p1 + p2 == s1 )
    assert( p2 + p1 == s1 )
    assert( s2 == s1 )
    assert( p1 + polyn(0) == p1 )

#-----------------------------

@given(*coords(1), st.integers())
def test_add_polynomial_and_number(e, c, integer):
    p = make(e, c)
    assert( p + 0 == p )
    if e == 0:
        s = make(e, c + integer)
    else:
        s = make(e, c, 0, integer)
    assert( p + integer == s )
    assert( integer + p == s )

#=============================

@given(*coords(2))
def test_sub(e1, c1, e2, c2):
    p1 = make(e1, c1)
    p2 = make(e2, c2)
    if e1 == e2:
        s1 = make(e1, c1 - c2)
    else:
        s1 = make(e1, c1, e2, -c2)
    if c2 >= 0:
        s2 = polyn('-'.join((repr(p1), repr(p2))))
    else:
        s2 = polyn('+'.join((repr(p1), repr(p2).lstrip('-'))))
    assert( p1 - p2 == s1 )
    assert( p2 - p1 == -s1 )
    assert( s2 == s1 )
    assert( p1 - polyn(0) == p1 )

#-----------------------------

@given(*coords(1), st.integers())
def test_sub_polynomial_and_number(e, c, integer):
    p = make(e, c)
    assert( p - 0 == p )
    if e == 0:
        s = make(e, c - integer)
    else:
        s = make(e, c, 0, -integer)
    assert( p - integer == s )
    assert( integer - p == -s )

#=============================

@given(*coords(2))
def test_mul(e1, c1, e2, c2):
    p1 = make(e1, c1)
    p2 = make(e2, c2)
    s = make(e1+e2, c1*c2)
    assert( p1 * p2 == s )
    assert( p2 * p1 == s )
    assert( p1 * polyn(1) == p1 )
    assert( p1 * polyn(0) == polyn(0) )

#-----------------------------

@given(*coords(1), st.integers())
def test_mul_polynomial_and_number(e, c, integer):
    p = make(e, c)
    assert( p * 1 == p )
    assert( p * -1 == -p )
    assert( p * 0 == polyn(0) )
    s = make(e, c * integer)
    assert( p * integer == s )
    assert( integer * p == s )

#-----------------------------

@given(*coords(4))
def test_distributive_law(e1, c1, e2, c2, e3, c3, e4, c4):
    p1 = make(e1, c1)
    p2 = make(e2, c2)
    p3 = make(e3, c3)
    p4 = make(e4, c4)
    assert( (p1 + p2) * (p3 + p4) == p1*p3 + p1*p4 + p2*p3 + p2*p4 )

#=============================

@given(*coords(4, nonzero))
def test_div(e1, c1, e2, c2, e3, c3, e4, c4):
    assume( are_distinct(e1, e2) and are_distinct(e3, e4) )
    p1 = make(e1, c1, e2, c2)
    p2 = make(e3, c3, e4, c4)
    s = p1 * p2
    assert( s // p1 == p2 )
    assert( s // p2 == p1 )
    assert( p1 // p1 == polyn(1) )
    assert( p1 // polyn(1) == p1 / 1 == p1 )
    assert( p1 // polyn(-1) == p1 / -1 == -p1 )

#=============================

@given(
    *coords(2, nonzero),
    st.integers(min_value=0, max_value=20),
    st.integers(min_value=0, max_value=10)
)
def test_pow(e1, c1, e2, c2, m, n):
    assume( are_distinct(e1, e2) )
    p = make(e1, c1, e2, c2)
    mth_power = p**m
    nth_power = p**n
    sum_power = p**(m+n)
    assert( mth_power * nth_power == sum_power )
    assert( sum_power // nth_power == mth_power )

#=============================

@given(*coords(3, coeff_min=1))
def test_mod(e1, c1, e2, c2, e3, c3):
    assume( are_distinct(e1, e2) )
    p1 = make(e1, c1, e2, c2)
    p2 = make(e3, c3)
    assert( (p1 * p2) % p1 == polyn(0) )
    assert( (p1 * p2) % p2 == polyn(0) )

#=============================

@given(*coords(2), st.integers(min_value=2))
def test_div_mod_polynomial_by_int(e1, c1, e2, c2, integer):
    assume( are_distinct(e1, e2) )
    p = make(e1, c1, e2, c2)
    assert( p == (p // integer) * integer + (p % integer) )

#=============================

@given(*coords(2), st.integers())
def test_eval(e1, c1, e2, c2, val):
    assume( are_distinct(e1, e2) )
    p = make(e1, c1, e2, c2)
    output = c1 * val**e1 + c2 * val**e2
    assert( p.eval(val) == output )

#-----------------------------

@given(*coords(2), st.integers(), st.integers(min_value=2))
def test_mod_eval(e1, c1, e2, c2, val, mod):
    p = make(e1, c1, e2, c2)
    assume( p.mod_eval(val, mod) == p.eval(val) % mod )

#=============================

@given(
    *(4 * [st.integers()]),
    st.integers().filter(lambda x: x < 0 or not is_square(x))
)
def test_quadratic_integers(a1, b1, a2, b2, d):
    g1 = QuadraticInteger(a1, b1, d)
    g2 = QuadraticInteger(a2, b2, d)
    p1 = Polynomial({0: a1, 1: b1})
    p2 = Polynomial({0: a2, 1: b2})
    m = Polynomial({0: -d, 2: 1})
    g = g1 * g2
    p = Polynomial({0: g.real, 1: g.imag})
    assert( (p1 * p2) % m == p )

