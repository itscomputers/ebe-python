#   lib/basic/__init__.py
#   - module with basic number theoretic functionality

# flake8: noqa

# ===========================================================
from .division import (
    bezout,
    div,
    gcd,
    lcm,
    padic,
)
from .modular import (
    chinese_remainder_theorem,
    jacobi,
    mod_inverse,
    mod_power,
    prime_to,
)
from .primality import (
    iter_primes_up_to,
    prime_gen,
    primes_up_to,
)
from .shape_number import (
    shape_number_by_index,
    which_shape_number,
)
from .sqrt import (
    integer_sqrt,
    is_square,
)
