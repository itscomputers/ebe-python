#   test_quadratic.py
#===========================================================
from hypothesis import given, assume, strategies as st
import math

from numth.basic import div, is_square
from numth.quadratic import * 
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

def rational():
    return [st.integers(), st.integers(min_value=1)]

def rational_coords():
    return [*rational(), *rational(), st.integers().filter(root_filter)]

def double_coords():
    return [*pair(), *pair(), st.integers().filter(root_filter)]

#=============================

@given(*coords())
def test_norm_conjugate(real, imag, root):
    a = Quadratic(real, imag, root)
    assert( a * a.conjugate() == Quadratic(a.norm(), 0, a.root) )
    assert( a + a.conjugate() == Quadratic(2*a.real, 0, a.root) )
    assert( a - a.conjugate() == Quadratic(0, 2*a.imag, a.root) )

#-----------------------------

@given(
    *coords(),
    st.integers(min_value=2)
)
def test_mod_inverse(real, imag, root, modulus):
    q = Quadratic(real, imag, root)
    assume( gcd(q.norm(), modulus) == 1 )
    q_inverse = q.mod_inverse(modulus)
    assert( (q_inverse * q) % modulus == Quadratic(1, 0, root) )
    assert( q_inverse == q.inverse(modulus) )

#-----------------------------

@given(*coords())
def test_inverse(real, imag, root):
    assume( real != 0 and imag != 0 )
    a = Quadratic(real, imag, root)
    assert( a * a.inverse() == Quadratic(1, 0, root) )
    assert( a.inverse().inverse() == a )

#=============================

@given(*coords(rmin=2, rmax=2**80))
def test_to_rational_approx(real, imag, root):
    num_digits = len(str(imag)) + 20
    r = Quadratic(real, imag, root).to_rational_approx(num_digits)
    assert( ((r - real)**2).approx_equal(imag**2 * root, 10) )

#-----------------------------

@given(*coords())
def test_neg(real, imag, root):
    a = Quadratic(real, imag, root)
    assert( a + -a == -a + a == Quadratic(0, 0, root) )
    assert( -a == -1 * a )

#-----------------------------

@given(*coords(rmin=2))
def test_int(real, imag, root):
    n = int(Quadratic(real, imag, root))
    if imag >= 0:
        assert( (n - real)**2 <= imag**2 * root < (n - real + 1)**2 )
    else:
        assert( (n - real)**2 >= imag**2 * root > (n - real + 1)**2 )
    
#-----------------------------

@given(*rational_coords())
def test_floor(real_numer, real_denom, imag_numer, imag_denom, root):
    real = Rational(real_numer, real_denom)
    imag = Rational(imag_numer, imag_denom)
    a = Quadratic(real, imag, root).floor()
    assert( a.real <= real < a.real + 1 )
    assert( a.imag <= imag < a.imag + 1 )

#-----------------------------

@given(*rational_coords())
def test_round(real_numer, real_denom, imag_numer, imag_denom, root):
    real = Rational(real_numer, real_denom)
    imag = Rational(imag_numer, imag_denom)
    a = Quadratic(real, imag, root).round()
    assert( a.real == round_down(real) )
    assert( a.imag == round_down(imag) )
    
#-----------------------------

@given(*coords(rmin=2))
def test_float(real, imag, root):
    f1 = float(Quadratic(real, imag, root))
    f2 = real + imag * math.sqrt(root)
    assert( str(f1)[:10] == str(f2)[:10] )

#=============================

@given(*double_coords())
def test_add(real1, imag1, real2, imag2, root):
    q1 = Quadratic(real1, imag1, root)
    q2 = Quadratic(real2, imag2, root)
    s = Quadratic(real1 + real2, imag1 + imag2, root)
    assert( q1 + q2 == s )
    assert( q2 + q1 == s )

#-----------------------------

@given(*coords(), *rational())
def test_add_quadratic_and_number(real, imag, root, numer, denom):
    q = Quadratic(real, imag, root)
    r = Quadratic(real + numer, imag, root)
    s = Quadratic(real + Rational(numer, denom), imag, root)
    assert( q + numer == r )
    assert( numer + q == r )
    assert( q + Rational(numer, denom) == s )
    assert( Rational(numer, denom) + q == s )

#=============================

@given(*double_coords())
def test_sub(real1, imag1, real2, imag2, root):
    q1 = Quadratic(real1, imag1, root)
    q2 = Quadratic(real2, imag2, root)
    s = Quadratic(real1 - real2, imag1 - imag2, root)
    assert( q1 - q2 == s )
    assert( q2 - q1 == -s )

#-----------------------------

@given(*coords(), *rational())
def test_sub_quadratic_and_number(real, imag, root, numer, denom):
    q = Quadratic(real, imag, root)
    r = Quadratic(real - numer, imag, root)
    s = Quadratic(real - Rational(numer, denom), imag, root)
    assert( q - numer == r )
    assert( numer - q == -r )
    assert( q - Rational(numer, denom) == s )
    assert( Rational(numer, denom) - q == -s )

#=============================

@given(*double_coords())
def test_mul(real1, imag1, real2, imag2, root):
    q1 = Quadratic(real1, imag1, root)
    q2 = Quadratic(real2, imag2, root)
    real = real1 * real2 + imag1 * imag2 * root
    imag = real1 * imag2 + imag1 * real2
    s = Quadratic(real, imag, root)
    assert( q1 * q2 == s )
    assert( q2 * q1 == s )

#-----------------------------

@given(*coords(), *rational())
def test_mul_quadratic_and_number(real, imag, root, numer, denom):
    q = Quadratic(real, imag, root)
    r = Quadratic(real * numer, imag * numer, root)
    s = Quadratic(
        real * Rational(numer, denom),
        imag * Rational(numer, denom),
        root
    )
    assert( q * numer == r )
    assert( numer * q == r )
    assert( q * Rational(numer, denom) == s )
    assert( Rational(numer, denom) * q == s )

#=============================

@given(*double_coords())
def test_div(real1, imag1, real2, imag2, root):
    assume( real1 != 0 or imag1 != 0 )
    assume( real2 != 0 or imag2 != 0 )
    q1 = Quadratic(real1, imag1, root)
    q2 = Quadratic(real2, imag2, root)
    q2_norm = q2.norm()
    real = Rational(real1 * real2 - imag1 * imag2 * root, q2_norm)
    imag = Rational(-real1 * imag2 + imag1 * real2, q2_norm)
    s = Quadratic(real, imag, root)
    assert( q1 / q2 == s )
    assert( q2 / q1 == s.inverse() )

#-----------------------------

@given(*coords(), *rational())
def test_div_quadratic_and_number(real, imag, root, numer, denom):
    assume( (real != 0 or imag != 0) and numer != 0 )
    q = Quadratic(real, imag, root)
    r = Quadratic(Rational(real, numer), Rational(imag, numer), root)
    s = Quadratic(
        real / Rational(numer, denom),
        imag / Rational(numer, denom),
        root
    )
    assert( q / numer == r )
    assert( numer / q == r.inverse() )
    assert( q / Rational(numer, denom) == s )
    assert( Rational(numer, denom) / q == s.inverse() )

#=============================

@given(*double_coords())
def test_floordiv(real1, imag1, real2, imag2, root):
    assume( real2 != 0 or imag2 != 0 )
    q1 = Quadratic(real1, imag1, root)
    q2 = Quadratic(real2, imag2, root)
    q2_norm = q2.norm()
    real = round_down(Rational(real1 * real2 - imag1 * imag2 * root, q2_norm))
    imag = round_down(Rational(-real1 * imag2 + imag1 * real2, q2_norm))
    s = Quadratic(real, imag, root)
    assert( q1 // q2 == s )

#-----------------------------

@given(*coords(), st.integers().filter(lambda x: x != 0))
def test_floordiv_quadratic_and_integer(real, imag, root, integer):
    assume( real != 0 or imag != 0 )
    q = Quadratic(real, imag, root)
    r = Quadratic(real // integer, imag // integer, root)
    assert( q // integer == r )
    assert( integer // q == Quadratic(integer, 0, root) // q )

#=============================

@given(
    *coords(), 
    st.integers(min_value=-20, max_value=20),
    st.integers(min_value=-10, max_value=10)
)
def test_pow(real, imag, root, m, n):
    assume( real != 0 or imag != 0 )
    q = Quadratic(real, imag, root)
    assert( q**2 == q * q )
    assert( q**(-2) == (q * q).inverse() )
    mth_power = q**m
    nth_power = q**n
    sum_power = q**(m + n)
    assert( mth_power * nth_power == sum_power )
    assert( sum_power / mth_power == nth_power )

#-----------------------------

@given(
    *coords(),
    st.integers(min_value=0, max_value=20),
    st.integers(min_value=2)
)
def test_mod_power(real, imag, root, exponent, modulus):
    q = Quadratic(real, imag, root)
    assume( gcd(q.norm(), modulus) == 1 )
    mod_power = pow(q, exponent, modulus)
    mod_inverse_power = pow(q, -exponent, modulus)
    power = pow(q, exponent)
    assert( power % modulus == mod_power )
    assert( mod_inverse_power.inverse(modulus) == mod_power )

#=============================

@given(*double_coords())
def test_mod(real1, imag1, real2, imag2, root):
    assume( real2 != 0 or imag2 != 0 )
    q1 = Quadratic(real1, imag1, root)
    q2 = Quadratic(real2, imag2, root)
    assert( q1 == (q1 // q2) * q2 + (q1 % q2) )

#-----------------------------

@given(*pair(), *pair())
def test_mod_gaussian(real1, imag1, real2, imag2):
    assume( real1 != 0 or imag1 != 0 )
    assume( real2 != 0 or imag2 != 0 )
    q1 = Quadratic(real1, imag1, -1)
    q2 = Quadratic(real2, imag2, -1)
    assert( 2 * (q1 % q2).norm() <= q2.norm() )

#-----------------------------

@given(*coords(), st.integers(min_value=1))
def test_mod_quadratic_and_integer(real, imag, root, integer):
    assume( real != 0 or imag != 0 )
    q = Quadratic(real, imag, root)
    r = Quadratic(real % integer, imag % integer, root)
    assert( q % integer == r )
    assert( integer % q == Quadratic(integer, 0, root) % q )
    assert( q == (q // integer) * integer + (q % integer) )

#=============================


#-----------------------------

@given(*pair())
def test_canonical(real, imag):
    canon = Quadratic(real, imag, -1).canonical()
    assert( canon.real >= abs(canon.imag) )

#-----------------------------

@given(*pair(), *pair())
def test_gcd(real1, imag1, real2, imag2):
    assume( (real1, imag1, real2, imag2) != (0, 0, 0, 0) )
    q1 = Quadratic(real1, imag1, -1)
    q2 = Quadratic(real2, imag2, -1)
    d = q1.gcd(q2)
    dd = q2.gcd(q1)
    assert( d == dd )
    assert( (q1 % d).components == (0, 0) )
    assert( (q2 % d).components == (0, 0) )
    assert( (q1 // d).gcd(q2 // d).components == (1, 0) )
    assert( (q2 // d).gcd(q1 // d).components == (1, 0) )

