#   numth/basic/shape_number.py
#===========================================================

def shape_number_by_index(k, sides):
    """
    Find the kth shape number for given number of sides.

    params
    + k : int
    + sides : int
        must be > 2
    
    return
    int
    """
    return k * (k * (sides - 2) - sides + 4) // 2

#=============================

def which_shape_number(number, sides):
    """
    Determine if a number is a shape number with given number of sides.

    params
    + number : int
    + sides : int
        must be > 2

    return
    int
    """
    denom = 2 * (sides - 2)
    root = 8 * (sides - 2) * number + (sides - 4)**2
    
    if not is_square(root):
        return None
    
    q, r = div(sides - 4 + integer_sqrt(root), denom)
    if r == 0:
        return q

