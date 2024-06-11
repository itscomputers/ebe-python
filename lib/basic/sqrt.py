#   lib/basic/sqrt.py
#   - module for basic functions around integer square roots

# ===========================================================
import math

# ===========================================================


def integer_sqrt(number: int, guess: int = None) -> int:
    """
    Compute the integer part of the square root of `number`.

    example: `integer_sqrt(30) ~> 5`
        since `5**2 == 25 <= 30 < 36 == 6**2`
    """
    if guess is None:
        guess = int(math.sqrt(number))

    while guess**2 > number or (guess + 1) ** 2 <= number:
        guess = (guess + number // guess) // 2

    return guess


# =============================


def is_square(number: int) -> bool:
    """
    Determine whether `number` is a perfect square.

    examples: `is_square(25) ~> True`
              `is_square(30) ~> False`
              `is_square(-25) ~> False`
    """
    return number >= 0 and integer_sqrt(number) ** 2 == number
