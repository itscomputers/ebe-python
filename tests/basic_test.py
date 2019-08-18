#   tests/basic_test.py
#===========================================================
import env
from hypothesis import given, assume, strategies as st
from random import sample

from numth.factorization import factor
from numth.modular import euler_phi
from numth.basic import *
#===========================================================
#   division
#===========================================================

@given(
    st.integers(),
    st.integers().filter(lambda x: x != 0)
)
def test_div(a, b):
    q, r = div(a, b)
    assert( 0 <= r < abs(b) )
    assert( a == q * b + r )

#-----------------------------

@given(
    st.integers(),
    st.integers().filter(lambda x: x != 0)
)
def test_div_with_small_remainder(a, b):
    q, r = div_with_small_remainder(a, b)
    assert( -abs(b) / 2 < r <= abs(b) / 2 )
    assert( a == q * b + r )

#-----------------------------

@given(
    st.integers(),
    st.integers()
)
def test_gcd(a, b):
    assume( (a, b) != (0, 0) )
    d = gcd(a, b)
    assert( a % d == b % d == 0 )
    assert( gcd(a//d, b//d) == 1 )


@given(
    st.integers(min_value=1),
    st.integers(min_value=1),
    st.integers(min_value=1)
)
def test_gcd_of_many(a, b, c):
    d = gcd(a, b, c)
    assert( a % d == b % d == c % d == 0 )
    assert( gcd(a//d, b//d, c//d) == 1 )

#-----------------------------

@given(
    st.integers(),
    st.integers()
)
def test_lcm(a, b):
    assume( a != 0 and b != 0 )
    m = lcm(a, b)
    assert( m % a == m % b == 0 )
    assert( gcd(m//a, m//b) == 1 )

#-----------------------------

@given(
    st.integers(min_value=1),
    st.integers(min_value=1),
    st.integers(min_value=1)
)
def test_lcm_of_multiple(a, b, c):
    m = lcm(a, b, c)
    assert( m % a == m % b == m % c == 0 )
    assert( gcd(m//a, m//b, m//c) == 1 )

#-----------------------------

@given(
    st.integers(),
    st.integers()
)
def test_bezout(a, b):
    assume( a != 0 or b != 0 )
    x, y = bezout(a, b)
    d = gcd(a, b)
    assert( a*x + b*y == d )

#-----------------------------

@given(
    number = st.integers().filter(lambda x: x != 0),
    base = st.integers(min_value=2)
)
def test_padic(number, base):
    exp, rest = padic(number, base)
    assert( number == base**exp * rest )
    assert( rest % base != 0 )

#===========================================================
#   modular
#===========================================================

@given(st.integers())
def test_jacobi(a):
    for p in iter_primes_up_to(10**3):
        if p == 2:
            continue
        if a % p == 0:
            assert( jacobi(a, p) == 0 )
        else:
            assert( jacobi(a, p) == euler_criterion(a, p) ) 

#-----------------------------

@given(
    number = st.integers(),
    modulus = st.integers(min_value=2)
)
def test_mod_inverse(number, modulus):
    assume( gcd(number, modulus) == 1 )
    inverse = mod_inverse(number, modulus)
    assert( 0 < inverse < modulus )
    assert( (number * inverse) % modulus == 1 )

#-----------------------------

@given(
    number = st.integers(),
    exponent = st.integers(max_value=-1),
    modulus = st.integers(min_value=2)
)
def test_mod_power(number, exponent, modulus):
    assume( gcd(number, modulus) == 1 )
    value = mod_power(number, exponent, modulus)
    inverse = mod_power(number, -exponent, modulus)
    assert( mod_inverse(value, modulus) == inverse )
    assert( mod_power(number, 0, modulus) == 1 )

#-----------------------------

@given(*(3 * [st.integers()]))
def test_chinese_remainder_theorem(a, b, c):
    primes = sample(primes_up_to(10**3), 4)
    moduli = [primes[0]**1, primes[1]**2, primes[2] * primes[3]]
    solution = chinese_remainder_theorem([a,b,c], moduli)
    for (r, m) in zip([a,b,c], moduli):
        assert( solution % m == r % m )

#-----------------------------

@given(st.integers(min_value=2, max_value=500))
def test_prime_to(number):
    factorization = factor(number)
    phi = euler_phi(factorization)
    group = prime_to(factorization)
    assert( phi == len(group) )
    for x in group:
        assert( gcd(x, number) == 1 )

#===========================================================
#   primality
#===========================================================

def test_primes_up_to():
    prime_lists = (primes_up_to(10**i) for i in range(6))
    prime_counts = [0, 4, 25, 168, 1229, 9592]
    for i, prime_list in enumerate(prime_lists):
        assert len(prime_list) == prime_counts[i]
        if i < 5:
            assert prime_list == list(iter_primes_up_to(10**i))

#-----------------------------

def test_is_prime__naive():
    for p in iter_primes_up_to(10**3):
        assert( is_prime__naive(p) )

#===========================================================
#   shape_number
#===========================================================

@given(st.integers(min_value=3))
def test_shape_number(s):
    for k in range(1, 20):
        assert( which_shape_number(shape_number_by_index(k, s), s) == k )

#===========================================================
#   sqrt
#===========================================================

@given(st.integers(min_value=0))
def test_integer_sqrt(number):
    s = integer_sqrt(number)
    assert( s**2 <= number < (s+1)**2 )

#-----------------------------

@given(st.integers())
def test_is_square(number):
    assert( is_square(number**2) )

