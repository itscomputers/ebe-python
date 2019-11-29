#   lib/__init__.py
#   - a number theory library in python 3

#===========================================================

from .algebraic_structures import (
    ModularRing
)

from .basic import *
from .factorization import *
from .lucas_sequence import *
from .modular import *

from .continued_fraction import (
    continued_fraction_quotients,
    continued_fraction_convergents,
    continued_fraction_pell_numbers,
    continued_fraction_table,
    continued_fraction_all
)

from .primality import (
    lucas_witness_pair,
    lucas_test,
    miller_rabin_witness,
    miller_rabin_test,
    is_prime,
    next_prime_gen,
    next_prime,
    next_primes,
    primes_in_range,
    prev_prime_gen,
    prev_prime,
    next_twin_primes_gen,
    next_twin_primes,
    goldbach_partition
)

from .rational_approximation import (
    newton_gen,
    halley_gen,
    pi,
    babylonian_gen,
    continued_fraction_convergent_gen
)

from .types import (
    polyn,
    Polynomial,
    Quadratic,
    QuadraticInteger,
    GaussianInteger,
    Quaternion,
    frac,
    Rational
)

