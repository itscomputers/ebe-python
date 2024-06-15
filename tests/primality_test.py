#   tests/primality_test.py
# ===========================================================
import pytest
from hypothesis import given, strategies as st

import env  # noqa
from lib.basic.primality import is_prime__naive, primes_up_to
from lib.primality.algorithms import (
    is_prime,
    lucas_test,
    miller_rabin_test,
    LucasWitness,
    MillerRabinWitness,
    Observation,
)
from lib.primality.goldbach import goldbach_partition
from lib.primality.prime_search import (
    next_prime,
    next_primes,
    prev_prime,
    prev_primes,
    primes_in_range,
    PrimeSearch,
    Window,
)
from lib.primality.twin_prime_search import (
    next_twin_prime,
    prev_twin_prime,
    TwinPrimeSearch,
)

# ===========================================================
# algorithms
# ===========================================================


def test_is_prime_on_sieve():
    upper = 10**4
    primes = set(primes_up_to(upper))
    for number in range(2, upper):
        assert is_prime(number) is (number in primes)


# -----------------------------


@given(st.integers(min_value=2, max_value=10**7))
def test_is_prime(number):
    assert is_prime(number) == is_prime__naive(number)


# ============================
# observation
# ============================


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


# ============================
# lucas
# ============================


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
        observation = lucas_test(number, witness_count=5)
        if number in primes:
            assert observation.value in [
                "prime",
                "probable_prime",
                "strong_probable_prime",
            ]
        else:
            assert observation.value == "composite"


# ============================
# miller_rabin
# ============================


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


# ============================
# integration
# ============================


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


# ==========================================================
# prime search
# ==========================================================


def test_prime_search():
    prime_search = PrimeSearch(1)
    primes = primes_up_to(100)
    for prime in primes:
        assert prime_search.next().value == prime

    prime_search.next()
    for prime in reversed(primes):
        assert prime_search.prev().value == prime

    assert not prime_search.prev().has_value()
    with pytest.raises(AttributeError):
        prime_search.value

    assert prime_search.next().value == 2


# -----------------------------


def test_prime_search_reverse():
    prime_search = PrimeSearch(100)
    primes = primes_up_to(100)
    for prime in reversed(primes):
        assert prime_search.prev().value == prime

    assert not prime_search.prev().has_value()
    with pytest.raises(AttributeError):
        prime_search.value

    for prime in primes:
        assert prime_search.next().value == prime


# =============================
# next prime
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
# prev prime
# =============================


@given(st.integers(min_value=-1, max_value=10**4))
def test_prev_primes_generator(number):
    prime_search = PrimeSearch(number)
    primes = []
    while prime_search.prev().has_value():
        primes.append(prime_search.value)
    assert list(reversed(primes)) == primes_in_range(1, number)


# -----------------------------


def test_prev_prime_small():
    assert prev_prime(5) == prev_prime(4) == 3
    assert prev_prime(3) == 2
    assert prev_prime(2) is None
    assert prev_prime(1) is None
    assert prev_prime(0) is None


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


# -----------------------------


@given(st.integers(min_value=6, max_value=10**2))
def test_prev_primes(number):
    primes = prev_primes(number, count=number)
    assert list(reversed(primes)) == primes_in_range(1, number)


# =============================
# window
# =============================


@pytest.mark.parametrize(
    "numbers, expected",
    [
        ([-1, 0, 1], 2),
        ([2], 3),
        ([3, 4], 5),
        ([5, 6], 7),
        ([7, 8, 9, 10], 11),
        ([11, 12], 13),
        ([13, 14, 15, 16], 17),
        ([17, 18], 19),
        ([19, 20, 21, 22], 23),
        ([23, 24, 25, 26, 27, 28], 29),
        ([29, 30], 31),
        ([31, 32, 33, 34, 35, 36], 37),
        ([37, 38, 39, 40], 41),
        ([41, 42], 43),
        ([43, 44, 45, 46], 47),
        ([47, 48], 49),
        ([49, 50, 51, 52], 53),
        ([53, 54, 55, 56, 57, 58], 59),
        ([59, 60], 61),
        ([61, 62, 63, 64, 65, 66], 67),
        ([67, 68, 69, 70], 71),
        ([71, 72], 73),
        ([73, 74, 75, 76], 77),
        ([77, 78], 79),
        ([79, 80, 81, 82], 83),
        ([83, 84, 85, 86, 87, 88], 89),
    ],
)
def test_window_next_value(numbers, expected):
    for number in numbers:
        window = Window(number, [2, 3, 5])
        try:
            assert window.next().value == expected, f"failed on: {number} ~> {expected}"
        except StopIteration:
            pytest.fail(f"failed on: {number} -> {expected}")


# ----------------------------


@pytest.mark.parametrize(
    "numbers, expected",
    [
        ([-1, 0, 1, 2], None),
        ([3], 2),
        ([4, 5], 3),
        ([6, 7], 5),
        ([8, 9, 10, 11], 7),
        ([12, 13], 11),
        ([14, 15, 16, 17], 13),
        ([18, 19], 17),
        ([20, 21, 22, 23], 19),
        ([24, 25, 26, 27, 28, 29], 23),
        ([30, 31], 29),
        ([32, 33, 34, 35, 36, 37], 31),
        ([38, 39, 40, 41], 37),
        ([42, 43], 41),
        ([44, 45, 46, 47], 43),
        ([48, 49], 47),
        ([50, 51, 52, 53], 49),
        ([54, 55, 56, 57, 58, 59], 53),
        ([60, 61], 59),
        ([62, 63, 64, 65, 66, 67], 61),
        ([68, 69, 70, 71], 67),
        ([72, 73], 71),
        ([74, 75, 76, 77], 73),
        ([78, 79], 77),
        ([80, 81, 82, 83], 79),
        ([84, 85, 86, 87, 88, 89], 83),
    ],
)
def test_window_prev_value(numbers, expected):
    for number in numbers:
        window = Window(number, [2, 3, 5])
        try:
            assert window.prev().value == expected, f"failed on: {number} ~> {expected}"
        except StopIteration:
            pytest.fail(f"failed on: {number} -> {expected}")


# ----------------------------


def test_window_next_values():
    window = Window(0, [2, 3, 5])
    for value in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49, 53, 59, 61]:
        assert window.next().value == value


# ----------------------------


def test_window_prev_values():
    window = Window(62, [2, 3, 5])
    for value in [
        61,
        59,
        53,
        49,
        47,
        43,
        41,
        37,
        31,
        29,
        23,
        19,
        17,
        13,
        11,
        7,
        5,
        3,
        2,
        None,
        None,
    ]:
        if value is None:
            assert window.prev().value is None
        else:
            assert window.prev().value == value


# ----------------------------


def test_window_prev_and_next_values():
    window = Window(48, [2, 3, 5])
    assert window.next().value == 49
    assert window.next().value == 53
    assert window.next().value == 59
    assert window.next().value == 61
    assert window.next().value == 67
    assert window.prev().value == 61
    assert window.prev().value == 59
    assert window.prev().value == 53
    assert window.prev().value == 49

    window = Window(6, [2, 3, 5])
    assert window.prev().value == 5
    assert window.prev().value == 3
    assert window.prev().value == 2
    assert window.prev().value is None
    assert window.prev().value is None
    assert window.next().value == 2
    assert window.next().value == 3
    assert window.next().value == 5


# ==========================================================
# twin prime search
# ==========================================================


def test_twin_prime_search():
    twin_prime_search = TwinPrimeSearch(1)
    primes = primes_up_to(100)
    twin_primes = [
        (primes[i - 1], primes[i])
        for i in range(1, len(primes))
        if primes[i] == primes[i - 1] + 2
    ]
    for twin_prime in twin_primes:
        assert twin_prime_search.next().value == twin_prime

    twin_prime_search.next()
    for twin_prime in reversed(twin_primes):
        assert twin_prime_search.prev().value == twin_prime

    assert not twin_prime_search.prev().has_value()
    with pytest.raises(AttributeError):
        twin_prime_search.value
    assert twin_prime_search.next().value == (3, 5)


# -----------------------------


def test_twin_prime_search_reversed():
    twin_prime_search = TwinPrimeSearch(100)
    primes = primes_up_to(100)
    twin_primes = [
        (primes[i - 1], primes[i])
        for i in range(1, len(primes))
        if primes[i] == primes[i - 1] + 2
    ]
    for twin_prime in reversed(twin_primes):
        assert twin_prime_search.prev().value == twin_prime

    assert not twin_prime_search.prev().has_value()
    with pytest.raises(AttributeError):
        twin_prime_search.value

    for twin_prime in twin_primes:
        assert twin_prime_search.next().value == twin_prime


# -----------------------------


@given(st.integers(min_value=-1, max_value=10**10))
def test_next_twin_prime(number):
    p, q = next_twin_prime(number)
    assert is_prime(p)
    assert is_prime(q)
    assert q == p + 2
    for i in range(number + 1 - number % 2, p, 2):
        assert not is_prime(i) or not is_prime(i + 2)


# -----------------------------


@pytest.mark.parametrize(
    "numbers, twin_prime",
    [
        (range(1, 5), (3, 5)),
        (range(5, 7), (5, 7)),
        (range(7, 13), (11, 13)),
        (range(13, 19), (17, 19)),
        (range(19, 31), (29, 31)),
        (range(31, 43), (41, 43)),
        (range(43, 61), (59, 61)),
        (range(61, 73), (71, 73)),
        (range(73, 103), (101, 103)),
    ],
)
def test_next_twin_prime_small(numbers, twin_prime):
    for number in numbers:
        assert (
            next_twin_prime(number) == twin_prime
        ), f"failed on #{number} ~> #{twin_prime}"


# -----------------------------


@pytest.mark.parametrize(
    "numbers, twin_prime",
    [
        (range(1, 4), None),
        (range(4, 6), (3, 5)),
        (range(6, 12), (5, 7)),
        (range(12, 18), (11, 13)),
        (range(18, 30), (17, 19)),
        (range(30, 42), (29, 31)),
        (range(42, 60), (41, 43)),
        (range(60, 72), (59, 61)),
        (range(72, 102), (71, 73)),
    ],
)
def test_prev_twin_prime_small(numbers, twin_prime):
    for number in numbers:
        assert (
            prev_twin_prime(number) == twin_prime
        ), f"failed on {number} ~> {twin_prime}"


# ==========================================================
# goldbach conjecture
# ==========================================================


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
        assert 2 <= len(partition) <= 3


# -----------------------------


def test_goldbach_conjecture_small():
    assert goldbach_partition(4) == (2, 2)
    assert goldbach_partition(5) == (3, 2)
