#   numth/basic/division.py
#===========================================================

def div(dividend, divisor):
    """
    Division with remainder.
    
    Computes quotient and remainder such that
        * ``0 <= remainder < abs(divisor)``
        * ``number == quotient * divisor + remainder``

    params
    + dividend : int
    + divisor : int
        nonzero

    return
    (quotient, remainder) : (int, int)
    """
    if divisor == 0:
        raise ValueError('Attempted division by zero')

    quotient = dividend // divisor
    remainder = dividend % divisor
    if divisor < 0 and remainder != 0:
        quotient += 1
        remainder -= divisor

    return quotient, remainder

#-----------------------------

def div_with_small_remainder(dividend, divisor):
    """
    Division with (smaller) remainder, similar to ``div``.

    Computes quotient and remainder such that
        * ``-abs(divisor) / 2 < remainder <= abs(divisor) / 2``
        * ``number == quotient * divisor + remainder``

    params
    + dividend : int
    + divisor : int
        nonzero

    return
    (quotient, remainder) : (int, int)
    """
    quotient, remainder = div(dividend, divisor)
    
    if 2 * remainder > abs(divisor):
        remainder -= abs(divisor)
        quotient = (dividend - remainder) // divisor

    return quotient, remainder 

#=============================

def euclidean_algorithm(a, b, division_func=div):
    """
    Euclidean algorithm.
    
    Prints ``a = q * b + r`` using division with remainder until r is zero.

    params
    + a : int
    + b : int
    + division_func : function
        either ``div`` or ``div_with_small_remainder``

    return
    None
    """
    q, r = division_func(a, b)
    print('{} = {} * {} + {}'.format(a, q, b, r))
    if r != 0:
        euclidean_algorithm(b, r, division_func)

#=============================

def gcd(*numbers):
    """
    Greatest common divisor.

    Computes largest positive integer dividing all numbers.

    params
    + numbers : list(int)
        at least one of the numbers is nonzero

    return
    int
    """
    if len(numbers) == 1:
        return gcd(*numbers, 0)

    if len(numbers) > 2:
        return gcd(numbers[0], gcd(*numbers[1:]))

    if numbers == (0, 0):
        raise ValueError('gcd(0, 0) is undefined')

    a, b = numbers
    while b != 0:
        a, b = b, a % b

    return abs(a)

#=============================

def lcm(*numbers):
    """
    Least common multiple.

    Computes smallest positive integer divisible by all numbers.

    params
    + numbers : list(int)
        all numbers are nonzero

    return
    int
    """
    if len(numbers) == 1:
        return abs(numbers[0])

    if len(numbers) > 2:
        return lcm(numbers[0], lcm(*numbers[1:]))

    a, b = numbers
    if a * b == 0:
        raise ValueError('lcm(_, 0) is undefined')

    return abs(a // gcd(a, b) * b)

#=============================

def bezout(a, b):
    """
    Solution to Bezout's Lemma.
    
    Finds an integer solution (x, y) to ``a*x + b*y = gcd(a, b)``.
    
    params
    + a : int
    + b : int
        at least one of a or b is nonzero

    return
    (x, y) : (int, int)
    """
    if (a, b) == (0, 0):
        raise ValueError('gcd(0, 0) is undefined')

    if b == 0:
        return a // abs(a), 0

    x, y = _bezout_helper(a, b)

    if a*x + b*y > 0:
        sign = 1
    else:
        sign = -1

    return sign*x, sign*y

# - - - - - - - - - - - - - - 

def _bezout_helper(a, b):
    def advance(u, v, q):
        return v, u - q*v

    q, r = div(a, b)
    X = (0, 1)
    Y = (1, -q)

    while r != 0:
        a, b = b, r
        q, r = div(a, b)
        X, Y = advance(*X, q), advance(*Y, q)

    return X[0], Y[0]

#=============================

def padic(number, base):
    """
    p-adic representation.

    Computes exp and rest such that ``number == (base ** exp) * rest``.

    params
    + number : int
        nonzero
    + base : int
        base > 1

    return
    (exp, rest) : (int, int)
    """
    if number == 0:
        raise ValueError('number must be nonzero')

    if base < 2:
        raise ValueError('base must be at least 2')

    exp = 0
    rest = number
    while rest % base == 0:
        rest //= base
        exp += 1

    return exp, rest

