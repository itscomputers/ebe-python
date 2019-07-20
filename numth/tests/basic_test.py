#   numth/tests/basic_test.py
#===========================================================
from hypothesis import given, assume, strategies as st
from random import sample

from ..factorization import factor
from ..modular import euler_phi_from_factorization
from ..basic import *
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

#=============================

@given(st.integers(min_value=0))
def test_integer_sqrt(number):
    s = integer_sqrt(number)
    assert( s**2 <= number < (s+1)**2 )

#-----------------------------

@given(st.integers())
def test_is_square(number):
    assert( is_square(number**2) )

#=============================

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
    primes = sample(prime_sieve(10**3), 4)
    moduli = [primes[0]**1, primes[1]**2, primes[2] * primes[3]]
    solution = chinese_remainder_theorem([a,b,c], moduli)
    for (r, m) in zip([a,b,c], moduli):
        assert( solution % m == r % m )

#-----------------------------

@given(st.integers(min_value=2, max_value=500))
def test_prime_to(number):
    factorization = factor(number)
    phi = euler_phi_from_factorization(factorization)
    group = prime_to(factorization)
    assert( phi == len(group) )
    for x in group:
        assert( gcd(x, number) == 1 )

#=============================

def test_prime_sieve():
    assert( len(prime_sieve(10**2)) == 25 )
    assert( len(prime_sieve(10**3)) == 168 )
    assert( len(prime_sieve(10**4)) == 1229 )
    assert( len(prime_sieve(10**5)) == 9592 )

#-----------------------------

def test_is_prime__naive():
    for p in prime_sieve(10**3):
        assert( is_prime__naive(p) )

#=============================

@given(st.integers())
def test_jacobi(a):
    for p in prime_sieve(10**3)[1:]:
        if a % p == 0:
            assert( jacobi(a, p) == 0 )
        else:
            assert( jacobi(a, p) == euler_criterion(a, p) ) 

#=============================

@given(st.floats(min_value=0))
def test_round_down(number):
    assume( str(number) not in ['-inf', 'inf', 'nan'] )
    if number <= int(number) + .5:
        assert( round_down(number) == int(number) )
    else:
        assert( round_down(number) == int(number) + 1 )
    assert( round_down(-number) == - round_down(number) )

