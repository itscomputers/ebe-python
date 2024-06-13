#   tests/factorization_test.py
# ===========================================================
from collections import Counter
from functools import reduce

import pytest
from hypothesis import given, strategies as st

import env  # noqa
from lib.basic import gcd, is_square, padic
from lib.primality import is_prime, next_prime
from lib.types import GaussianInteger, QuaternionInteger
from lib.utils import combine_counters
from lib.factorization import (
    Algorithm,
    DivisorSearch,
    Factorization,
    find_divisors,
    get_gaussian_divisor,
    get_quaternion_divisor,
)

# ===========================================================


@st.composite
def prime_(draw, min_value, max_value):
    return next_prime(draw(st.integers(min_value=min_value, max_value=max_value)))


@st.composite
def composite(draw, num_factors, min_value, max_value):
    return reduce(
        lambda x, h: x * draw(prime_(min_value, max_value)),
        range(num_factors),
        1,
    )


# ===========================================================
#   algorithms
# ===========================================================


@given(st.integers(min_value=2, max_value=10**12))
def test_pollard_rho(number):
    strategy = Algorithm.build("rho", seed=2, func=lambda x: x**2 + 1)
    if not is_prime(number):
        divisor = strategy.find_divisor(number)
        assert divisor > 1 and number % divisor == 0


# -----------------------------


@given(st.integers(min_value=2, max_value=10**10))
def test_pollard_p_minus_one(number):
    strategy = Algorithm.build("p-1", seed=2)
    if not is_prime(number):
        divisor = strategy.find_divisor(number)
        assert divisor > 1 and number % divisor == 0


# -----------------------------


@given(st.integers(min_value=2, max_value=10**8))
def test_williams_p_plus_one(number):
    strategy = Algorithm.build("p+1", seed=GaussianInteger(1, 2))
    if not is_prime(number):
        divisor = strategy.find_divisor(number)
        assert divisor > 1 and number % divisor == 0


# ===========================================================
#   divisor_search
# ===========================================================


@given(composite(4, 10**2, 10**4))
def test_find_divisors(number):
    divisors = find_divisors(number)
    assert len(divisors) > 0
    for divisor in divisors:
        assert 1 < divisor < number
        assert number % divisor == 0


# -----------------------------


@given(composite(4, 10**2, 10**4))
def test_divisor_search(number):
    algorithms = [
        Algorithm.build("rho", seed=2),
        Algorithm.build("rho", seed=3),
        Algorithm.build("rho", seed=5),
        Algorithm.build("rho", seed=6),
        Algorithm.build("p-1", seed=2),
        Algorithm.build("p-1", seed=3),
        Algorithm.build("p+1", seed=GaussianInteger(1, 2)),
        Algorithm.build("p+1", seed=GaussianInteger(1, 3)),
    ]
    divisor_search = DivisorSearch(number, algorithms).search()
    for divisor in divisor_search.divisors:
        assert 1 <= divisor <= number
        assert number % divisor == 0

    assert any(1 < divisor < number for divisor in divisor_search.divisors)


# ===========================================================
#   factorization
# ===========================================================


@given(composite(4, 1, 10**2))
def test_factor_only_prime_base(number):
    factorization = Factorization(number)
    for prime, exp in factorization:
        assert padic(number, prime)[0] == exp
        assert is_prime(prime)
    assert Factorization.from_dict(dict(factorization)).number == number


# -----------------------------


@given(composite(4, 10**3, 10**5))
def test_factor_no_prime_base(number):
    factorization = Factorization(number)
    for prime, exp in factorization:
        assert padic(number, prime)[0] == exp
        assert is_prime(prime)
    assert Factorization.from_dict(dict(factorization)).number == number


# -----------------------------


@given(st.integers(min_value=2, max_value=10**15))
def test_factor(number):
    factorization = Factorization(number)
    for prime, _ in factorization:
        assert is_prime(prime)
    assert Factorization.from_dict(dict(factorization)).number == number


# -----------------------------


@given(st.integers(min_value=2, max_value=10**12))
def test_square_and_square_free(number):
    factorization = Factorization(number)
    square = factorization.square_part
    square_free = factorization.square_free_part
    if dict(square):
        assert set(map(lambda v: v % 2, dict(square).values())) == {0}
    if dict(square_free):
        assert set(dict(square_free).values()) == {1}
    assert combine_counters(dict(square), dict(square_free)) == dict(factorization)
    assert is_square(square.number)
    assert square.number * square_free.number == number


# -----------------------------


@given(st.integers(min_value=2, max_value=10**12))
def test_divisors(number):
    divisors = Factorization(number).divisors
    for idx in range(len(divisors) // 2):
        assert divisors[idx] * divisors[-idx - 1] == number


# -----------------------------


@given(st.integers(min_value=2, max_value=10**12))
def test_factors(number):
    factorization = Factorization(number)
    factors = factorization.factors
    assert dict(Counter(factors)) == dict(factorization)
    remaining = number
    for prime in factors:
        assert is_prime(prime)
        remaining = remaining // prime
    assert remaining == 1


# -----------------------------


@given(st.integers(min_value=2, max_value=10**12))
def test_primes(number):
    primes = Factorization(number).primes
    remaining = number
    for prime in primes:
        assert is_prime(prime)
        exp, remaining = padic(remaining, prime)
    assert remaining == 1


# -----------------------------


def test_from_dict_of_primes():
    f_dict = {5: 4, 11: 2, 541: 3}
    number = 5**4 * 11**2 * 541**3
    factorization = Factorization.from_dict(f_dict)
    assert factorization.number == number
    assert dict(factorization) == f_dict


# -----------------------------


def test_from_dict_of_mixed():
    f_dict = {5: 4, 15: 2, 541: 3}
    number = 5**4 * 15**2 * 541**3
    factorization = Factorization.from_dict(f_dict)
    assert factorization.number == number
    assert dict(factorization) == {3: 2, 5: 6, 541: 3}


# -----------------------------


def test_from_list_of_prime_factors():
    factors = [5, 5, 5, 5, 11, 11, 541, 541, 541]
    number = 5**4 * 11**2 * 541**3
    factorization = Factorization.from_list(factors)
    assert factorization.number == number
    assert factorization.factors == factors


# -----------------------------


def test_from_list_of_mixed_factors():
    factors = [5, 5, 5, 5, 15, 15, 541, 541, 541]
    number = 5**4 * 15**2 * 541**3
    factorization = Factorization.from_list(factors)
    assert factorization.number == number
    assert dict(factorization) == {3: 2, 5: 6, 541: 3}
    assert factorization.factors == [3, 3, 5, 5, 5, 5, 5, 5, 541, 541, 541]


# -----------------------------


@given(prime_(min_value=5, max_value=10**10))
def test_get_gaussian_divisor(prime):
    if prime % 4 == 1:
        g = get_gaussian_divisor(prime)
        assert g.norm == prime
        assert GaussianInteger(prime, 0) % g == GaussianInteger(0, 0)
    else:
        with pytest.raises(ValueError):
            get_gaussian_divisor(prime)


# -----------------------------


@given(st.integers(min_value=2, max_value=10**4))
def test_two_squares(number):
    factorization = Factorization(number)
    squares = factorization.two_squares
    if factorization.is_sum_of_two_squares():
        assert sorted(squares, reverse=True) == list(squares)
        assert sum(map(lambda x: x**2, squares)) == number
    else:
        assert squares is None


# -----------------------------


@given(prime_(min_value=5, max_value=10**10))
def test_get_quaternion_divisor(prime):
    q = get_quaternion_divisor(prime)
    assert q.norm == prime
    assert QuaternionInteger(prime, 0, 0, 0) % q == QuaternionInteger(0, 0, 0, 0)


# -----------------------------


@given(st.integers(min_value=2, max_value=10**4))
def test_four_squares(number):
    factorization = Factorization(number)
    squares = factorization.four_squares
    assert sorted(squares, reverse=True) == list(squares)
    assert sum(map(lambda x: x**2, squares)) == number


# -----------------------------


@given(st.integers(min_value=2, max_value=10**4))
def test_euler_phi(number):
    factorization = Factorization(number)
    euler_phi = factorization.euler_phi
    prime_to_count = sum(
        1
        for x in range(1, number)
        if not any(x % prime == 0 for prime in factorization.primes)
    )
    assert prime_to_count == euler_phi


# -----------------------------


@given(st.integers(min_value=2, max_value=10**4))
def test_carmichael_lambda(number):
    def _carmichael_property(exp) -> bool:
        return all(
            pow(x, exp, number) == 1 for x in range(1, number) if gcd(x, number) == 1
        )

    factorization = Factorization(number)
    carmichael_lambda = factorization.carmichael_lambda

    assert factorization.euler_phi % carmichael_lambda == 0

    assert _carmichael_property(carmichael_lambda)

    for divisor in Factorization(carmichael_lambda).divisors:
        if divisor < carmichael_lambda:
            assert not _carmichael_property(divisor)
