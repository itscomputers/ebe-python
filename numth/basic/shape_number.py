#   numth/basic/shape_number.py
#===========================================================
from .division import div
from .sqrt import integer_sqrt, is_square
#===========================================================

def shape_number_by_index(k: int, sides: int) -> int:
    """
    Computes the `k`th shape number for number of `sides`.

    example:
        `shape_number_by_index(5, 3) => 15`
        since 15 is the 5th triangular number

    params:
        `k : int --nonnegative`,
        `sides : int --at least 3`

    returns:
        `int`
    """
    return k * (k * (sides - 2) - sides + 4) // 2

#=============================

def which_shape_number(number: int, sides: int) -> int:
    """
    Computes, if possible, shape number index for `number` with
    given number of `sides`.
    Inverse of `numth.basic.shape_number.shape_number_by_index`.

    examples:
        `which_shape_number(15, 3) => 5`,
        `which_shape_number(20, 3) => None`

    params:
        `number : int`,
        `sides : int --at least 3`

    returns:
        `k : int` or `None`
    """
    denom = 2 * (sides - 2)
    root = 8 * (sides - 2) * number + (sides - 4)**2

    if not is_square(root):
        return None

    k, r = div(sides - 4 + integer_sqrt(root), denom)
    if r != 0:
        return None
    return k

