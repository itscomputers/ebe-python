#   tests/primality_test.py
# ===========================================================
import pytest
from hypothesis import given, strategies as st

import env  # noqa
from lib.basic.primality import is_prime__naive, primes_up_to
from lib.primality.algorithms import (
    lucas_test,
    miller_rabin_test,
    LucasWitness,
    MillerRabinWitness,
    Observation,
)
from lib.primality.main import (
    is_prime,
    next_prime,
    next_primes,
    primes_in_range,
    prev_prime_gen,
    prev_prime,
    next_twin_primes,
    goldbach_partition,
)

# ===========================================================
#   observation
# ===========================================================


@pytest.mark.parametrize(
    "values, expected",
    [
        (
            ["composite", "prime", "strong_probable_prime", "probable_prime"],
            "composite",
        ),
        (
            ["prime", "composite", "strong_probable_prime", "probable_prime"],
            "composite",
        ),
        (
            ["prime", "strong_probable_prime", "composite", "probable_prime"],
            "composite",
        ),
        (
            ["prime", "strong_probable_prime", "probable_prime", "composite"],
            "composite",
        ),
        (
            ["prime", "strong_probable_prime", "probable_prime"],
            "prime",
        ),
        (
            ["strong_probable_prime", "prime", "probable_prime"],
            "prime",
        ),
        (
            ["strong_probable_prime", "probable_prime", "prime"],
            "prime",
        ),
        (
            ["strong_probable_prime", "probable_prime"],
            "strong_probable_prime",
        ),
        (
            ["probable_prime", "strong_probable_prime"],
            "strong_probable_prime",
        ),
        (
            ["probable_prime", "probable_prime"],
            "probable_prime",
        ),
    ],
)
def test_observation_compose(values, expected):
    observations = (Observation(value=value) for value in values)
    observation = Observation.compose(observations)
    assert observation.value == expected


# ===========================================================
#   lucas
# ===========================================================


@given(st.integers(min_value=3, max_value=10**6))
def test_lucas_test(number):
    number += 1 - number % 2
    observation = lucas_test(number, 20)
    number_is_prime = is_prime__naive(number)
    if observation.value in ["strong_probable_prime", "probable_prime"]:
        assert number_is_prime
    else:
        assert not number_is_prime


# -----------------------------


@given(st.integers(min_value=3), st.integers(min_value=1, max_value=30))
def test_generate_lucas_witnesses(number, witness_count):
    number += 1 - number % 2
    witnesses = list(LucasWitness.generate(number, witness_count))
    assert witness_count == len(witnesses)
    for witness in witnesses:
        try:
            witness._first_observation(number)
        except ValueError as e:
            pytest.fail(str(e))


# -----------------------------


def test_lucas_on_sieve():
    upper = 10**4
    primes = set(primes_up_to(upper))
    for number in range(2, upper):
        observation = lucas_test(number, witness_count=20)
        if number in primes:
            assert observation.value in [
                "prime",
                "probable_prime",
                "strong_probable_prime",
            ]
        else:
            assert observation.value == "composite"


# ===========================================================
#   miller_rabin
# ===========================================================


@given(st.integers(min_value=2, max_value=10**6))
def test_miller_rabin_test(number):
    observation = miller_rabin_test(number, witness_count=20)
    number_is_prime = is_prime__naive(number)
    if observation.value in ["prime", "probable_prime"]:
        assert number_is_prime
    else:
        assert not number_is_prime


# -----------------------------


@given(st.integers(min_value=3), st.integers(min_value=1, max_value=50))
def test_generate_miller_rabin_witnesses(number, witness_count):
    witnesses = list(MillerRabinWitness.generate(number, witness_count))

    for w in witnesses:
        assert 2 <= w._value < number

    if number > MillerRabinWitness.MAX_CUTOFF and witness_count > number:
        assert len(witnesses) == number - 3
        assert all(witness._assured for witness in witnesses)

    elif number <= MillerRabinWitness.MAX_CUTOFF:
        assert [witness._value for witness in witnesses] == [
            p for (val, p) in MillerRabinWitness.CUTOFFS if val < number
        ]
        assert all(witness._assured for witness in witnesses)

    else:
        assert len(witnesses) == witness_count


# -----------------------------


def test_miller_rabin_on_sieve():
    upper = 10**4
    primes = set(primes_up_to(upper))
    for number in range(2, upper):
        observation = miller_rabin_test(number, witness_count=20)
        if number in primes:
            assert observation.value == "prime"
        else:
            assert observation.value == "composite"


# ===========================================================
#   main
# ===========================================================


def test_is_prime_on_sieve():
    upper = 10**4
    primes = set(primes_up_to(upper))
    for number in range(2, upper):
        assert is_prime(number) is (number in primes)


# -----------------------------


@given(st.integers(min_value=3))
def test_integration_of_miller_rabin_and_lucas(number):
    number += 1 - number % 2
    number_is_prime = is_prime(number)
    if any(
        test(number, witness_count=20).value == "composite"
        for test in (miller_rabin_test, lucas_test)
    ):
        assert not number_is_prime
    else:
        assert number_is_prime


# -----------------------------


@given(st.integers(min_value=2, max_value=10**7))
def test_is_prime(number):
    assert is_prime(number) == is_prime__naive(number)


# =============================


@given(st.integers(min_value=-1))
def test_next_prime(number):
    p = next_prime(number)
    assert is_prime(p)
    for x in range(number + 1, p):
        assert not is_prime(x)


# -----------------------------


@given(st.integers(min_value=-1, max_value=10**5), st.integers(min_value=1, max_value=30))
def test_next_primes(number, number_of_primes):
    primes = next_primes(number, number_of_primes)
    assert len(set(primes)) == number_of_primes
    for i in range(len(primes) - 1):
        assert is_prime(primes[i])
        for x in range(primes[i] + 1, primes[i + 1]):
            assert not is_prime(x)


# -----------------------------


@given(
    st.integers(min_value=-1, max_value=10**4),
    st.integers(min_value=1, max_value=10**4),
)
def test_primes_in_range(lower_bound, difference):
    upper_bound = lower_bound + difference
    primes = primes_in_range(lower_bound, upper_bound)
    if primes != []:
        assert primes[0] >= lower_bound
        assert primes[-1] < upper_bound
    for p in primes:
        assert is_prime(p)


# =============================


@given(st.integers(min_value=-1, max_value=10**4))
def test_prev_primes_gen(number):
    g = prev_prime_gen(number)
    primes = []
    while True:
        try:
            primes = primes + [next(g)]
        except StopIteration:
            break
    assert list(reversed(primes)) == primes_in_range(1, number)


# -----------------------------


def test_prev_prime_small():
    assert prev_prime(5) == prev_prime(4) == 3
    assert prev_prime(3) == 2
    assert prev_prime(2) == prev_prime(1) == prev_prime(0) is None


# -----------------------------


@given(st.integers(max_value=-1))
def test_prev_prime_neg(number):
    assert prev_prime(number) is None


# -----------------------------


@given(st.integers(min_value=6, max_value=10**4))
def test_prev_prime(number):
    p = prev_prime(number)
    assert is_prime(p)
    for x in range(p + 1, number):
        assert not is_prime(x)


# =============================


@given(st.integers(min_value=-1, max_value=10**10))
def test_next_twin_primes(number):
    p, q = next_twin_primes(number)
    assert is_prime(p)
    assert is_prime(q)
    assert q == p + 2
    for i in range(number + 1 - number % 2, p, 2):
        assert not is_prime(i) or not is_prime(i + 2)


# =============================


@given(st.integers(min_value=6, max_value=10**10))
def test_goldbach_conjecture(number):
    partition = goldbach_partition(number)
    assert list(partition) == sorted(partition, reverse=True)
    for p in partition:
        assert is_prime(p)
    assert sum(partition) == number
    if number % 2 == 0:
        assert len(partition) == 2
    else:
        assert len(partition) == 3


# -----------------------------


def test_goldbach_conjecture_small():
    assert goldbach_partition(4) == (2, 2)
    assert goldbach_partition(5) == (3, 2)
