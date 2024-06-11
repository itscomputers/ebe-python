#   lib/factorization/__init__.py
#   - module for prime factorization and its applications

# ===========================================================
from .algorithms import (
    pollard_rho,
    pollard_p_minus_one,
    williams_p_plus_one,
)
from .main import (
    divisors,
    factor,
    find_divisor,
    number_from_factorization,
)
from .two_squares import (
    gaussian_divisor,
    two_squares,
)
from .four_squares import (
    quaternion_divisor,
    four_squares,
)

# ===========================================================
__all__ = [
    # algorithms
    "pollard_rho",
    "pollard_p_minus_one",
    "williams_p_plus_one",
    # main
    "divisors",
    "factor",
    "find_divisor",
    "number_from_factorization",
    # two_squares
    "gaussian_divisor",
    "two_squares",
    # four_squares
    "quaternion_divisor",
    "four_squares",
]
