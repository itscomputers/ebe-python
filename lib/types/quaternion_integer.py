#   lib/types/quaternion_integer.py
#   - class for arithmetic of integer quaternions
# ===========================================================
from ..basic import mod_inverse
from .quaternion import (
    add_,
    floordiv_,
    mul_,
    Quaternion,
)

# ===========================================================
__all__ = [
    "QuaternionInteger",
]
# ===========================================================


class QuaternionInteger(Quaternion):
    """
    Class that represents `a + bi + cj + dk`,
    where coefficients are integers.

    The class implements arithmetic operations with members of itself,
    general quaternions, integers, and rational numbers.

    Much of the functionality is inherited from `lib.types.Quaternion`
    and operations with general quaternions or rational numbers will
    elevate it to that type.
    """

    def __init__(self, *components):
        self.components = tuple(map(int, components))

    # =========================

    @property
    def to_quaternion(self):
        """Cast to Quaternion."""
        return Quaternion(*self.components)

    @classmethod
    def from_gaussian_integer(self, gaussian_integer):
        """Build from GaussianInteger."""
        return QuaternionInteger(*gaussian_integer.components, 0, 0)

    # =========================

    def _eq_QuaternionInteger(self, other):
        return self.components == other.components

    # =========================

    @property
    def round(self):
        return self

    def mod_inverse(self, modulus):
        return (self.conjugate * mod_inverse(self.norm, modulus)) % modulus

    # =========================

    def _add_QuaternionInteger(self, other):
        return QuaternionInteger(*add_(self, other))

    # =========================

    def _mul_QuaternionInteger(self, other):
        return QuaternionInteger(*mul_(self, other))

    def _rmul_Quaternion(self, other):
        return Quaternion(*mul_(other, self))

    # =========================

    def _truediv_QuaternionInteger(self, other):
        return self * other.inverse

    def _rtruediv_Quaternion(self, other):
        return other * self.inverse

    # =========================

    def _floordiv_QuaternionInteger(self, other):
        return QuaternionInteger(*floordiv_(self, other))

    def _rfloordiv_Quaternion(self, other):
        return Quaternion(*floordiv_(other, self))

    # =========================

    def _inv_pow_mod_int(self, other, modulus):
        return self.__pow__(-other, modulus).mod_inverse(modulus)
