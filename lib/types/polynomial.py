#   lib/types/polynomial.py
#   - class for arithmetic of polynomials

# ===========================================================
from functools import reduce
import re

from ..basic import lcm, mod_power
from ..utils import combine_counters
from .arithmetic_type import ArithmeticType
from .rational import frac

# ===========================================================
__all__ = [
    "add_",
    "add_constant",
    "mul_",
    "mul_constant",
    "truediv_constant",
    "floordiv_constant",
    "mod_constant",
    "polyn",
    "Polynomial",
]
# ===========================================================


def polyn(*args):
    """Shortcut to create Polynomial from string or tuple of coeffs"""
    if len(args) == 1:
        if isinstance(*args, str):
            return Polynomial.from_string(*args)
        if isinstance(*args, dict):
            return Polynomial(*args)
    return Polynomial.from_coeff_list(*args)


# =============================


def add_(a, b):
    """Shortcut to add other polynomials."""
    return combine_counters(a, b)


def add_constant(a, b):
    """Shortcut to add rational numbers and integers."""
    return combine_counters(a, {0: b})


def mul_(a, b):
    """Shortcut to multiply by other polynomials."""
    return reduce(
        add_, ({e1 + e2: c1 * c2 for e2, c2 in b.items()} for e1, c1 in a.items()), dict()
    )


def mul_constant(a, b):
    """Shortcut to multiply by rational numbers and integers."""
    return dict((k, v * b) for k, v in a.items())


def truediv_constant(a, b):
    return dict((k, v * frac(b).inverse) for k, v in a.items())


def floordiv_constant(a, b):
    return dict((k, v // b) for k, v in a.items())


def mod_constant(a, b):
    return dict((k, v % b) for k, v in a.items())


# =============================


class Polynomial(ArithmeticType):
    """Polynomial class with polynomial arithmetic"""

    def __init__(self, coeffs=dict()):
        self.coeffs = {
            e: frac(c)
            for (e, c) in coeffs.items()
            if type(e) is int and e >= 0 and c != 0
        }
        self.degree = self._degree()
        self.leading_coeff = self._leading_coeff()
        self.monic = self.leading_coeff == 1

    def __repr__(self):
        if self.coeffs == dict():
            return "0"
        representation = " + ".join(
            _exp_coeff_to_term(e, c) for (e, c) in sorted(self.coeffs.items())
        )

        return representation.replace(" + -", " - ")

    # =========================

    @classmethod
    def from_string(self, string):
        return Polynomial(_string_to_dict(string))

    @classmethod
    def from_coeff_list(self, *coeff_list):
        return Polynomial({e: c for e, c in enumerate(coeff_list)})

    # =========================

    def _degree(self):
        if self.coeffs == dict():
            return -1
        return max(self.coeffs.keys())

    def _leading_coeff(self):
        if self.coeffs == dict():
            return 0
        return self.coeffs[self.degree]

    # =========================

    def _eq_Polynomial(self, other):
        return self.coeffs == other.coeffs

    def _eq_int(self, other):
        if other == 0:
            return self.coeffs == dict()
        return self.coeffs == {0: other}

    def _eq_Rational(self, other):
        if other == 0:
            return self.coeffs == dict()
        return self.coeffs == {0: other}

    def _lt_Polynomial(self, other):
        return self.degree < other.degree

    def _gt_Polynomial(self, other):
        return self.degree > other.degree

    # =========================

    def __neg__(self):
        return Polynomial({e: -c for (e, c) in self.coeffs.items()})

    def canonical(self):
        if self.leading_coeff < 0:
            return -self
        return self

    def clear_denominators(self):
        m = lcm(*(c.denom for c in self.coeffs.values()))
        coeffs = {e: int(c * m) for (e, c) in self.coeffs.items()}

        return Polynomial(coeffs).canonical()

    # =========================

    def eval(self, value):
        return sum(map(lambda x: x[1] * value ** x[0], self.coeffs.items()))

    def mod_eval(self, value, modulus):
        return (
            sum(
                map(
                    lambda x: (x[1] * mod_power(value, x[0], modulus)),
                    self.coeffs.items(),
                )
            )
            % modulus
        )

    # =========================

    def derivative(self, order=None):
        if order == 0:
            return self
        if self.degree == 0:
            return Polynomial()

        deriv = Polynomial({e - 1: e * c for (e, c) in self.coeffs.items()})

        if order is None or order == 1:
            return deriv

        return deriv.derivative(order - 1)

    def integral(self, constant=0):
        return (
            Polynomial(dict((e + 1, c / frac(e + 1)) for (e, c) in self.coeffs.items()))
            + constant
        )

    # =========================

    def _add_int(self, other):
        return self.__class__(add_constant(self.coeffs, other))

    def _add_Rational(self, other):
        return Polynomial(add_constant(self.coeffs, other))

    def _add_Polynomial(self, other):
        return Polynomial(add_(self.coeffs, other.coeffs))

    # =========================

    def _mul_int(self, other):
        return self.__class__(mul_constant(self.coeffs, other))

    def _mul_Rational(self, other):
        return Polynomial(mul_constant(self.coeffs, other))

    def _mul_Polynomial(self, other):
        return Polynomial(mul_(self.coeffs, other.coeffs))

    def __rmul__(self, other):
        return self * other

    # =========================

    def div_with_remainder(self, other):
        quotient_dict = dict()
        remainder = self
        while other.degree <= remainder.degree:
            exp = remainder.degree - other.degree
            coeff = remainder.leading_coeff / other.leading_coeff
            quotient_dict = add_(quotient_dict, {exp: coeff})
            remainder = remainder - other * Polynomial({exp: coeff})
        return Polynomial(quotient_dict), remainder

    # =========================

    def _truediv_int(self, other):
        return Polynomial(truediv_constant(self.coeffs, other))

    def _truediv_Rational(self, other):
        return Polynomial(truediv_constant(self.coeffs, other))

    # =========================

    def _floordiv_int(self, other):
        return self.__class__(floordiv_constant(self.coeffs, other))

    def _floordiv_Rational(self, other):
        return self.__class__(floordiv_constant(self.coeffs, other))

    def _floordiv_Polynomial(self, other):
        return self.div_with_remainder(other)[0]

    def _rfloordiv_int(self, other):
        return Polynomial({0: other}) // self

    def _rfloordiv_Rational(self, other):
        return Polynomial({0: other}) // self

    # =========================

    def _mod_int(self, other):
        return self.__class__(mod_constant(self.coeffs, other))

    def _mod_Rational(self, other):
        return self.__class__(mod_constant(self.coeffs, other))

    def _mod_Polynomial(self, other):
        return self.div_with_remainder(other)[1]

    # =========================

    def _inv_pow_int(self, other):
        if self.degree == 0:
            return self.coeffs[0].inverse
        return NotImplemented

    def _zero_pow_int(self, other):
        return self.__class__({0: 1})


# ===========================================================


def _split_string_into_terms(string):
    return string.replace("-", "+-").replace(" ", "").split("+")


def _term_pattern():
    """Pattern for polynomial string term."""
    return re.compile(r"^([\-])?(\d+\/\d+|\d+)?\*?([A-Za-z]*)?\^?(\d+)?")


def _term_to_dict(term, pattern=_term_pattern()):
    sign, coeff, var, exp = pattern.findall(term)[0]
    coeff = frac("{}{}".format(sign, 1 if coeff == "" else coeff))
    if var == "":
        return {0: coeff}
    if exp == "":
        return {1: coeff}
    return {int(exp): coeff}


def _string_to_dict(string):
    pattern = _term_pattern()
    return reduce(
        add_,
        map(
            lambda term: _term_to_dict(term, pattern),
            filter(lambda term: term != "", _split_string_into_terms(string)),
        ),
        dict(),
    )


# -----------------------------


def _exp_coeff_to_term(exponent, coeff):
    """Convert exponent and coeff to string term."""
    if exponent == 0:
        return "{}".format(coeff)

    if abs(coeff) == 1:
        _coeff = format(coeff).replace("1", "")
    else:
        _coeff = "{}".format(coeff)

    if exponent == 1:
        return "{} x".format(_coeff)

    return "{} x^{}".format(_coeff, exponent)
