#   lib/rational_approximation/__init__.py
#   - module for rational approximation

# ===========================================================
from .general import (
    halley_gen,
    newton_gen,
)
from .pi import pi
from .sqrt import (
    babylonian_gen,
    bakhshali_gen,
    continued_fraction_convergent_gen,
    goldschmidt_gen,
    halley_sqrt_gen,
    ladder_arithmetic_gen,
    linear_fractional_transformation_gen,
)

# ===========================================================
__all__ = [
    # general
    "halley_gen",
    "newton_gen",
    # pi
    "pi",
    # sqrt
    "babylonian_gen",
    "bakhshali_gen",
    "continued_fraction_convergent_gen",
    "goldschmidt_gen",
    "halley_sqrt_gen",
    "ladder_arithmetic_gen",
    "linear_fractional_transformation_gen",
]
