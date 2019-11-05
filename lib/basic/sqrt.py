#   lib/basic/sqrt.py
#   - contains basic functions around integer square roots

#===========================================================
import math
#===========================================================
__all__ = [
    'integer_sqrt',
    'is_square',
]
#===========================================================

def integer_sqrt(number, guess=None):
    """
    Computes the integer part of the square root of `number`.

    number: int --at least 0
        ~>  int

    example:
        `integer_sqrt(30) ~> 5`
        since `5**2 == 25 <= 30 < 36 == 6**2`
    """

    if guess is None:
        guess = int(math.sqrt(number))

    while guess**2 > number or (guess+1)**2 <= number:
        guess = (guess + number // guess) // 2

    return guess

#=============================

def is_square(number):
    """
    Determines whether `number` is a perfect square.

    number: int
        ~>  bool

    examples:
        `is_square(25) ~> True`,
        `is_square(30) ~> False`,
        `is_square(-25) ~> False`
    """

    return number >= 0 and integer_sqrt(number)**2 == number

