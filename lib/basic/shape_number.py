#   lib/basic/shape_number.py
#   - contains basic function related to shape numbers

#===========================================================
from .division import div
from .sqrt import integer_sqrt, is_square
#===========================================================
__all__ = [
    'shape_number_by_index',
    'which_shape_number',
]
#===========================================================

def shape_number_by_index(k, sides):
    """
    Computes the `k`th polygonal shape number.

    k: int --at least 0
    sides: int --at least 3
        ~>  int

    example:
        `shape_number_by_index(5, 3) ~> 15`
        since 15 is the 5th triangular number
    """

    return k * (k * (sides - 2) - sides + 4) // 2

#=============================

def which_shape_number(number, sides):
    """
    Computes, if possible, shape number index for `number` with
    given number of `sides`. Inverse of
    `lib.basic.shape_number.shape_number_by_index`.

    number: int
    sides: int --at least 3
        ~> int

    examples:
        `which_shape_number(15, 3) ~> 5`,
        `which_shape_number(20, 3) ~> None`
    """

    denom = 2 * (sides - 2)
    root = 8 * (sides - 2) * number + (sides - 4)**2

    if not is_square(root):
        return None

    q, r = div(sides - 4 + integer_sqrt(root), denom)
    if r == 0:
        return q

