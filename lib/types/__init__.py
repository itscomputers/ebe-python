#   lib/types/__init__.py
#   - module for new types

# ===========================================================
from .gaussian_integer import GaussianInteger
from .gaussian_rational import GaussianRational
from .polynomial import Polynomial, polyn
from .quadratic import Quadratic
from .quadratic_integer import QuadraticInteger
from .quaternion import Quaternion
from .quaternion_integer import QuaternionInteger
from .rational import Rational, frac

# ===========================================================
__all__ = [
    "frac",
    "polyn",
    "GaussianInteger",
    "GaussianRational",
    "Polynomial",
    "Quadratic",
    "QuadraticInteger",
    "Quaternion",
    "QuaternionInteger",
    "Rational",
]
