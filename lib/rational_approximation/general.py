#   lib/rational_approximation/general.py
#   - module for general rational approximation functions

# ===========================================================
from ..types import frac

# ===========================================================
__all__ = [
    "newton_gen",
    "halley_gen",
]
# ===========================================================


def newton_gen(polynomial, initial):
    """
    Newton's method for approximating a zero of `polynomial`.

    + polynomial: Polynomial
    + initial: Union[int, float, Rational]
    ~> Iterator[Rational]
    """
    approx = frac(initial)
    derivative = polynomial.derivative()

    while True:
        yield approx
        approx = approx - polynomial.eval(approx) / derivative.eval(approx)


# =============================


def halley_gen(polynomial, initial):
    """
    Halley's method for approximating a zero of `polynomial`.

    + polynomial: Polynomial
    + initial: Union[int, float, Rational]
    ~> Iterator[Rational]
    """
    approx = frac(initial)
    derivative = polynomial.derivative()
    second_derivative = derivative.derivative()

    while True:
        yield approx
        p = polynomial.eval(approx)
        dp = derivative.eval(approx)
        d2p = second_derivative.eval(approx)
        p_div_dp = p / dp
        approx = approx - p_div_dp / (1 - p_div_dp * d2p / dp / 2)
