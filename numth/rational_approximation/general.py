#   numth/rational_approximation/general.py
#===========================================================
from typing import Iterator, Union

from ..types import frac, Polynomial, Rational
#===========================================================

def newton_gen(
    polynomial: Polynomial,
    initial: Union[int, float, Rational]
) -> Iterator[Rational]:
    """
    Newton's method for approximating a zero of a polynomial.

    params
    + polynomial : Polynomial
    + initial : int, float, Rational

    return
    generator -> Rational
    """
    approx = frac(initial)
    derivative = polynomial.derivative()

    while True:
        yield approx
        approx = approx - polynomial.eval(approx) / derivative.eval(approx)

#=============================

def halley_gen(
    polynomial: Polynomial,
    initial: Union[int, float, Rational]
) -> Iterator[Rational]:
    """
    Halley's method for approximating a zero of a polynomial.

    params
    + polynomial : Polynomial
    + initial : int, float, Rational

    return
    generator -> Rational
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

