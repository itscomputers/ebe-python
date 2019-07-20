#   numth/basic/sqrt.py
#===========================================================
import math
#===========================================================

def integer_sqrt(number, guess=None):
    """
    Integer part of the square root of a number.

    Computes largest integer whose square is less than or equal to number.

    params
    + number : int
        nonnegative
    + guess : int
        nonnegative

    return
    int
    """
    if guess is None:
        guess = int(math.sqrt(number))

    while guess**2 > number or (guess+1)**2 <= number:
        guess = (guess + number // guess) // 2

    return guess

#=============================

def is_square(number):
    """
    If a number is a perfect square.

    params
    number : int

    return
    bool
    """
    return integer_sqrt(number)**2 == number

