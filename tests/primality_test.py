#   tests/primality_test.py
# ===========================================================
import env  # noqa
from hypothesis import given, strategies as st

from lib.basic.primality import is_prime__naive, primes_up_to
from lib.primality.miller_rabin import (
    miller_rabin_cutoffs,
    miller_rabin_max_cutoff,
    miller_rabin_test,
    miller_rabin_witness,
    miller_rabin_witnesses,
)
from lib.primality.miller_rabin import _generate_witnesses
from lib.primality.lucas import (
    lucas_test,
    lucas_witness_pair,
    lucas_witness_pairs,
)
from lib.primality.lucas import (
    _generate_witness_pairs,
    _good_parameters,
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
#   lucas
# ===========================================================


@given(st.integers(min_value=3), st.integers(min_value=1, max_value=50))
def test_lucas_witnesses(number, num_witnesses):
    number += 1 - number % 2
    witness_pairs = _generate_witness_pairs(number, num_witnesses)

    results = set(lucas_witness_pair(number, *pair) for pair in witness_pairs)
    combined_result = lucas_witness_pairs(number, witness_pairs)

    if ("composite", False) in results:
        assert combined_result == ("composite", False)
    elif ("probable prime", True) in results:
        assert combined_result == ("probable prime", True)
    else:
        assert combined_result == ("probable prime", False)


# -----------------------------


@given(st.integers(min_value=3, max_value=10**6))
def test_lucas_test(number):
    number += 1 - number % 2
    l_primality = lucas_test(number, 20)
    number_is_prime = is_prime__naive(number)
    if l_primality in ["strong probable prime", "probable prime"]:
        assert number_is_prime
    else:
        assert not number_is_prime


# -----------------------------


@given(st.integers(min_value=3), st.integers(min_value=1, max_value=30))
def test_generate_witness_pairs(number, num_witnesses):
    number += 1 - number % 2
    witness_pairs = _generate_witness_pairs(number, num_witnesses)
    assert num_witnesses == len(witness_pairs)
    for witness_pair in witness_pairs:
        P, Q = witness_pair
        assert _good_parameters(number, P, Q, P**2 - 4 * Q) is not False


# ===========================================================
#   miller_rabin
# ===========================================================


@given(st.integers(min_value=3), st.integers(min_value=1, max_value=50))
def test_miller_rabin_witnesses(number, num_witnesses):
    witnesses = _generate_witnesses(number, num_witnesses)
    single_results = set(miller_rabin_witness(number, witness) for witness in witnesses)
    combined_result = miller_rabin_witnesses(number, witnesses)
    if single_results == set(["probable prime"]):
        assert combined_result == "probable prime"
    else:
        assert combined_result == "composite"


# -----------------------------


@given(st.integers(min_value=2, max_value=10**6))
def test_miller_rabin_test(number):
    mr_primality = miller_rabin_test(number, 20)
    number_is_prime = is_prime__naive(number)
    if mr_primality in ["prime", "probable prime"]:
        assert number_is_prime
    else:
        assert not number_is_prime


# -----------------------------


@given(st.integers(min_value=3), st.integers(min_value=1, max_value=50))
def test_generate_witnesses(number, num_witnesses):
    witnesses = _generate_witnesses(number, num_witnesses)

    for w in witnesses:
        assert 2 <= w < number

    if number > miller_rabin_max_cutoff() and num_witnesses > number:
        assert len(witnesses) == number - 3

    elif number <= miller_rabin_max_cutoff():
        assert witnesses <= set(p for (val, p) in miller_rabin_cutoffs())

    else:
        assert len(witnesses) == num_witnesses


# ===========================================================
#   main
# ===========================================================


def test_is_prime_on_sieve():
    primes = primes_up_to(10**4)
    for p in primes:
        assert is_prime(p)

    non_primes = set(range(10**4)) - set(primes)
    for p in non_primes:
        assert not is_prime(p)


# -----------------------------


@given(st.integers(min_value=3))
def test_integration_of_miller_rabin_and_lucas(number):
    number += 1 - number % 2
    number_is_prime = is_prime(number)
    mr_primality = miller_rabin_test(number, 20)
    l_primality = lucas_test(number, 20)
    if "composite" in [mr_primality, l_primality]:
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
