#   lib/types/rational.py
#   - class for arithmetic of rational numbers

# ===========================================================
from fractions import Fraction
import math
import numbers

from ..config import default
from ..basic import gcd, integer_sqrt, is_square

# ===========================================================
__all__ = [
    "frac",
    "Rational",
]
# ===========================================================


def frac(*inputs):
    """Shortcut to create Rational"""
    if len(inputs) == 1:
        first = inputs[0]

        if not isinstance(first, (numbers.Real, str, list, tuple)):
            raise TypeError("incompatible type for rational number")

        type_name = type(first).__name__
        function_name = "Rational.from_{}".format(type_name)
        return eval(function_name)(first)

    return Rational(*inputs)


# ===========================================================


class Rational(Fraction):

    """
    Class that represents `numer / denom` as a rational number.

    This class inherits much of its functionality from `fractions.Fraction`.
    However, it implements some opinionated differences and some additional
    functionality.  For instance, Fraction allows operations with floats,
    but Rational does not, since floats cannot be trusted in general to be
    accurate.  A Rational can be built from a float, in which case operations
    may then occur, but this enforces intentional float to Rational conversion.

    + numer: int
    + denom: int
    + _normalize: bool --whether to check if `numer, denom` are in lowest terms
    """

    def __new__(cls, numer, denom, _normalize=True):
        self = super(Rational, cls).__new__(cls)

        if denom == 0:
            raise ZeroDivisionError("Rational(_, 0)")

        if _normalize:
            d = math.gcd(numer, denom)
            if denom < 0:
                d = -d
            numer = numer // d
            denom = denom // d

        self._numerator = numer
        self._denominator = denom
        return self

    # -------------------------

    @property
    def numer(self):
        return self._numerator

    @property
    def denom(self):
        return self._denominator

    @property
    def to_fraction(self):
        """Cast to Fraction."""
        return Fraction(self.numer, self.denom, _normalize=False)

    @classmethod
    def from_int(self, integer):
        """Build from int."""
        return Rational(integer, 1, _normalize=False)

    @classmethod
    def from_Rational(self, rational):
        """Build from Rational."""
        return rational

    @classmethod
    def from_Fraction(self, fraction):
        """Build from Fraction."""
        return Rational(fraction._numerator, fraction._denominator, _normalize=False)

    @classmethod
    def from_float(self, fl):
        """Build from float."""
        return Rational.from_str(str(fl))

    @classmethod
    def from_str(self, string):
        """Build from str."""
        return Rational.from_Fraction(Fraction(string.replace(" ", "")))

    @classmethod
    def from_list(self, li):
        """Build from List[int]."""
        return Rational(*li)

    @classmethod
    def from_tuple(self, tu):
        """Build from Tuple[int]."""
        return Rational(*tu)

    # -------------------------

    def __repr__(self):
        if self._denominator == 1:
            return "{}".format(self._numerator)
        return "{}/{}".format(self._numerator, self._denominator)

    @property
    def display(self):
        """Pretty-print rational number."""
        minus = self.sign == -1
        numer = str(abs(self._numerator))
        denom = str(self._denominator)
        length = max(len(numer), len(denom))
        numer_offset = (length - len(numer) + 1) // 2
        denom_offset = (length - len(denom) + 1) // 2
        numer = " " * (minus + numer_offset + 1) + numer
        denom = " " * (minus + denom_offset + 1) + denom
        line = "-" * minus + " " + "\u2500" * length
        return "{}\n{}\n{}".format(numer, line, denom)

    def decimal(self, num_digits=None):
        """
        Express rational number as a string in decimal form.

        + num_digits: int
        ~> str
        """
        if num_digits == 0:
            return str(self.round_to_nearest_int)

        sign = "-" if self._numerator < 0 else ""

        num_digits = num_digits or default("decimal_digits")

        quotient, remainder = divmod(abs(self._numerator), self._denominator)
        if num_digits == 0:
            return str(quotient)
        shifted_rem = Rational(remainder * 10 ** num_digits, self._denominator)
        digits = str(shifted_rem.round_to_nearest_int)
        num_zeros = num_digits - len(digits)

        return "{}{}.{}{}".format(sign, quotient, "0" * num_zeros, digits)

    # =========================

    @property
    def reciprocal(self):
        """
        Compute reciprocal rational number.

        ~> Rational
        """
        if self._numerator < 0:
            return Rational(-self._denominator, -self._numerator, _normalize=False)
        return Rational(self._denominator, self._numerator, _normalize=False)

    @property
    def inverse(self):
        """
        Compute multiplicative inverse.

        ~> Rational
        """
        return self.reciprocal

    @property
    def round_to_nearest_int(self):
        """
        Compute nearest integer, rounding up if halfway between.

        ~> int
        """
        return math.floor(self + Rational(1, 2))

    @property
    def round_prefer_toward_zero(self):
        """
        Compute nearest integer, rounding toward zero if halfway between.

        ~> int
        """
        return int(self) if self.denom == 2 else self.round_to_nearest_int

    @property
    def is_square(self):
        """
        Determine if is a square number.

        ~> bool
        """
        return is_square(self._numerator) and is_square(self._denominator)

    # =========================

    def approx_equal(self, other, num_digits=None):
        """
        Determine if approximately equal to `other`,
        ie, if ``abs(self - other) < 10**(-num_digits)``.

        + other: Union[int, float, string, Rational]
        + num_digits: int
        ~> bool
        """
        if num_digits == 0:
            return abs(self - other) < 1

        num_digits = num_digits or default("decimal_digits")

        other_ = frac(other)
        ad = self._numerator * other_._denominator
        bc = self._denominator * other_._numerator
        bd = self._denominator * other_._denominator

        return 10 ** num_digits * abs(ad - bc) < abs(bd)

    # =========================

    def sqrt(self, num_digits=None):
        """
        Compute square root or approximation of square root.

        + num_digits: int
        ~> Rational
        """
        if self < 0:
            raise ValueError("Cannot take square root of negative number")

        numer_integer_sqrt = integer_sqrt(self._numerator)
        denom_integer_sqrt = integer_sqrt(self._denominator)
        guess = Rational(numer_integer_sqrt, denom_integer_sqrt)

        if (
            numer_integer_sqrt ** 2 == self._numerator
            and denom_integer_sqrt ** 2 == self._denominator
        ):
            return guess

        num_digits = num_digits or default("sqrt_digits")

        if self._numerator > self._denominator:
            other_guess = self / guess

            while not guess.approx_equal(other_guess, num_digits):
                guess = (guess + other_guess) / 2
                other_guess = self / guess

            return guess

        else:
            return self.inverse.inverse_sqrt()

    # -------------------------

    def inverse_sqrt(self, num_digits=None):
        """
        Compute square root of reciprocal (or approximation).

        + num_digits: int
        ~> Rational
        """
        if self._numerator <= self._denominator:
            raise ValueError("Inverse square root only if greater than 1")

        guess = self.sqrt(2).inverse
        other_guess = guess * (2 - self * guess ** 2)

        while not guess.approx_equal(other_guess, num_digits):
            guess = (guess + other_guess) / 2
            other_guess = guess * (2 - self * guess ** 2)

        return guess

    # =========================

    def __pos__(self):
        return self

    def __neg__(self):
        return Rational(-self._numerator, self._denominator, _normalize=False)

    def __abs__(self):
        return Rational(abs(self._numerator), self._denominator, _normalize=False)

    # =========================

    def __add__(self, other):
        if type(other) is int:
            return Rational(
                self._numerator + other * self._denominator, self._denominator
            )
        if isinstance(other, numbers.Rational):
            return Rational(
                self._numerator * other._denominator
                + self._denominator * other._numerator,
                self._denominator * other._denominator,
            )
        return NotImplemented

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if type(other) is int:
            return Rational(self._numerator * other, self._denominator)
        if isinstance(other, numbers.Rational):
            return Rational(
                self._numerator * other._numerator, self._denominator * other._denominator
            )
        return NotImplemented

    def __truediv__(self, other):
        if type(other) is int:
            return Rational(self._numerator, self._denominator * other)
        if isinstance(other, numbers.Rational):
            return Rational(
                self._numerator * other._denominator, self._denominator * other._numerator
            )
        return NotImplemented

    def __floordiv__(self, other):
        if isinstance(other, (int, Rational)):
            return math.floor(self / other)
        return NotImplemented

    def __mod__(self, other):
        if isinstance(other, (int, Fraction, Rational)):
            return self - (self // other) * other
        return NotImplemented

    def __pow__(self, other):
        if isinstance(other, numbers.Rational) and other.denominator == 1:
            if other == 0:
                return Rational(1, 1)
            elif other < 0:
                return (self ** (-other)).inverse
            return Rational(
                self._numerator ** other, self._denominator ** other, _normalize=False
            )
        return NotImplemented

    # -------------------------

    def __radd__(self, other):
        return self + other

    def __rsub__(self, other):
        return -self + other

    def __rmul__(self, other):
        return self * other

    def __rtruediv__(self, other):
        return self.inverse * other

    def __rmod__(self, other):
        if isinstance(other, int):
            return self.from_int(other) % self
        elif isinstance(other, Fraction):
            return self.from_Fraction(other) % self
        return NotImplemented

    def __rpow__(self, other):
        if self.denom == 1:
            return other ** self.numer
        return NotImplemented
