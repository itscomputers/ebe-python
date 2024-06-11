#   lib/factorization/main.py
#   - module for main factorization functionality

# ===========================================================
from collections import Counter
from functools import reduce

from ..config import default
from ..basic import integer_sqrt, iter_primes_up_to, padic
from ..primality import is_prime
from ..utils import combine_counters
from .algorithms import pollard_rho_gen, pollard_p_minus_one_gen

# ===========================================================
__all__ = [
    "find_divisor",
    "factor_trivial",
    "factor_nontrivial",
    "factor",
    "divisors",
    "square_and_square_free",
    "number_from_factorization",
]
# ===========================================================


def find_divisor(number, rho_seeds=None, minus_seeds=None):
    """
    Find divisor of `number`.

    example: `find_divisor(143) ~> Set([13])`
             `find_divisor(143, [5, 7], [2]) ~> Set([11])`

    + number: int --composite
    + rho_seeds: List[int]
    + minus_seeds: List[int]
    ~> Set[int] --first divisors found from given seeds
    """
    divisor_search = _divisor_search_generators(number, rho_seeds, minus_seeds)

    divisor_found = False
    while not divisor_found:
        for value in divisor_search.values():
            divisor = next(value["generator"])
            if divisor == number:
                value["generator"] = _trivial_generator()
            else:
                if divisor > 1:
                    divisor_found = True
                value["divisor"] = divisor

    return set(
        filter(lambda x: x != 1, map(lambda x: x["divisor"], divisor_search.values()))
    )


# =============================


def factor_trivial(number, prime_base=None):
    """
    Factor out `prime_base` primes from `number` using trial division.

    example: `factor_trivial(1200, [2, 3, 7]) ~> (25, {2: 4, 3: 1})`
        since `1200 == 25 * 2**4 * 3`

    + number: int
    + prime_base: List[int]
    ~> (remaining, factorization): Tuple[int, Dict[int, int]]
    """
    prime_base = prime_base or iter_primes_up_to(default("prime_base_max"))
    remaining = number
    factorization = dict()

    for prime in prime_base:
        exp, remaining = padic(remaining, prime)
        if exp > 0:
            factorization[prime] = exp

    return remaining, factorization


# -----------------------------


def factor_nontrivial(number, rho_seeds=None, minus_seeds=None):
    """
    Factor `number` into primes using `lib.factorization.find_factor`.

    example: `factor_nontrivial(1200) ~> {2: 4, 3: 1, 5: 2}`
        since `1200 == 2**4 * 3 * 5**2

    + number: int
    + rho_seeds: List[int]
    + minus_seeds: List[int]
    ~> Dict[int, int]
    """
    if number == 1:
        return dict()

    if is_prime(number):
        return {number: 1}

    sqrt_number = integer_sqrt(number)
    if sqrt_number**2 == number:
        return combine_counters(dict(), factor_nontrivial(sqrt_number), 1, 2)

    remaining = number
    factorization = dict()

    divisors = find_divisor(remaining, rho_seeds, minus_seeds)
    for divisor in divisors:
        exp, remaining = padic(remaining, divisor)
        factorization = combine_counters(
            factorization, factor_nontrivial(divisor), 1, exp
        )

    return combine_counters(factorization, factor_nontrivial(remaining))


# -----------------------------


def factor(number, prime_base=None, rho_seeds=None, minus_seeds=None):
    """
    Factor `number` into primes.

    example: `factor(1200) ~> {2: 4, 3: 1, 5: 2}`
        since `1200 == 2**4 * 3 * 5**2`

    + number: int
    + prime_base: List[int] --primes to factor using trial division
    + rho_seeds: List[int] --seeds for Pollard's rho algorithm
    + minus_seeds: List[int] --seeds for Pollard's p-1 algorithm
    ~> Dict[int, int]
    """
    remaining, trivial_divisors = factor_trivial(number, prime_base)
    nontrivial_divisors = factor_nontrivial(remaining, rho_seeds, minus_seeds)

    return {**trivial_divisors, **nontrivial_divisors}


# =============================


def divisors_from_factorization(factorization):
    """
    Compute the divisors of corresponding `number`.

    example: `divisors_from_factorization({2: 1, 3: 2}) ~> [1, 2, 3, 6, 9, 18]`

    + factorization: Dict[int, int]
    ~> List[int]
    """
    divs = set([1])
    for p in Counter(factorization).elements():
        divs = divs | set(p * d for d in divs)
    return sorted(divs)


# -----------------------------


def divisors(number_or_factorization):
    """
    Compute the divisors of `number`.

    example: `divisors(18) ~> [1, 2, 3, 6, 9, 18]`
             `divisors({2: 1, 3: 2}) ~> [1, 2, 3, 6, 9, 18]`

    + number_or_factorization: Union[int, Dict[int, int]]
    ~> List[int]
    """
    if isinstance(number_or_factorization, int):
        factorization = factor(number_or_factorization)
    else:
        factorization = number_or_factorization

    return divisors_from_factorization(factorization)


# =============================


def square_part(factorization):
    """
    Compute square part of `factorization`.

    example: `square_part({2: 5, 3: 1, 5: 2}) ~> {2: 4, 5: 2}`

    + factorization: Dict[int, int]
    ~> Dict[int, int]
    """
    return {k: v - v % 2 for k, v in factorization.items() if v > 1}


# -----------------------------


def square_free_part(factorization):
    """
    Compute square-free part of `factorization`.

    example: `square_free_part({2: 5, 3: 1, 5: 2}) ~> {2: 1, 3: 1}`

    + factorization: Dict[int, int]
    ~> Dict[int, int]
    """
    return {k: 1 for k, v in factorization.items() if v % 2 == 1}


# -----------------------------


def square_and_square_free(factorization):
    """
    Split factorization into its square and square-free parts.

    + factorization: Dict[int, int]
    ~> Tuple[Dict[int, int], Dict[int, int]
    """
    return square_part(factorization), square_free_part(factorization)


# =============================


def number_from_factorization(factorization):
    """
    Compute number from its `factorization`.

    example: `number_from_factorization({2: 5, 3: 1, 5: 2}) ~> 2400`

    + factorization: Dict[int, int]
    ~> int
    """
    return reduce(lambda x, y: x * y, Counter(factorization).elements(), 1)


# ===========================================================


def _divisor_search_generators(number, rho_seeds, minus_seeds):
    """
    Build generators to search for a divisor.

    + number: int
    + rho_seeds: List[int]
    + minus_seeds: List[int]
    ~> Dict[Tuple[int, str], Dict[str, Iterator[int]]]
    """
    divisor_search = dict()
    for seed in rho_seeds or default("rho_seeds"):
        divisor_search[(seed, "rho")] = {
            "generator": pollard_rho_gen(number, seed, lambda x: x**2 + 1)
        }
    for seed in minus_seeds or default("minus_seeds"):
        divisor_search[(seed, "p-1")] = {
            "generator": pollard_p_minus_one_gen(number, seed)
        }
    return divisor_search


def _trivial_generator():
    while True:
        yield 1
