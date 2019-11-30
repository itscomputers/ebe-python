#   lib/types/__init__.py
#   - module for new types

#===========================================================
from .gaussian_integer import *
from .gaussian_rational import *
from .polynomial import *
from .quadratic import *
from .quadratic_integer import *
from .quaternion import *
from .quaternion_integer import *
from .rational import *
#===========================================================
__all__ = [
    'frac',
    'polyn',
    'GaussianInteger',
    'GaussianRational',
    'Polynomial',
    'Quadratic',
    'QuadraticInteger',
    'Quaternion',
    'QuaternionInteger',
    'Rational',
]

