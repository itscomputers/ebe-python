#   numth/basic/sqrt.py
#===========================================================
import math
#===========================================================

def integer_sqrt(number, guess=None):
    """
    Computes the integer part of the square root of `number`.

    example:
        `integer_sqrt(30) => 5`
        since `5**2 == 25 <= 30 < 36 == 6**2`

    params:
        `number : int --positive`

    returns:
        `int`
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

    examples:
        `is_square(25) => True`,
        `is_square(30) => False`,
        `is_square(-25) => False`

    params:
        `number : int`

    returns:
        `bool`
    """
    return number >= 0 and integer_sqrt(number)**2 == number

