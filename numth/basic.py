#   numth/basic.py
#===========================================================
import math
#===========================================================

def round_down(number):
    if number < 0:
        return - round_down(-number)
    if 2 * (number - int(number)) > 1:
        return int(number) + 1
    return int(number)

#-----------------------------

def div(number, divisor):
    """
    Division with remainder.
        (number: int, divisor: int) -> (quotient: int, remainder: int)

    Notes:  divisor nonzero
            0 <= remainder < abs(divisor)
            number = quotient * divisor + remainder
    """
    if divisor == 0:
        raise ValueError('Attempted division by zero')

    quotient = number // divisor
    remainder = number % divisor
    if divisor < 0 and remainder != 0:
        quotient += 1
        remainder -= divisor

    return quotient, remainder

#-----------------------------

def div_with_small_remainder(number, divisor):
    """
    Division with (smaller) remainder, similar to `div`.
        (number: int, divisor: int) -> (quotient: int, remainder: int)

    Note:   divisor nonzero
            -abs(divisor) / 2 < remainder <= abs(divisor) / 2
    """
    quotient, remainder = div(number, divisor)
    
    if 2 * remainder > abs(divisor):
        remainder -= abs(divisor)
        quotient = (number - remainder) // divisor

    return quotient, remainder 

#-----------------------------

def euclidean_algorithm(a, b, division=div):
    """
    Euclidean algorithm.
        (a: int, b: int, division: func) -> NoneType
        
    Note:   b nonzero
            prints a = q * b + r, using division with remainder until r == 0
    """
    q, r = division(a, b)
    print('{} = {} * {} + {}'.format(a, q, b, r))
    if r != 0:
        euclidean_algorithm(b, r, division)

#-----------------------------

def gcd(*numbers):
    """
    Greatest common divisor.
        numbers: array(int) -> int

    Note:   at least one nonzero number
            return_val is the largest positive integer dividing all numbers
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

#-----------------------------

def lcm(*numbers):
    """
    Least common multiple.
        (a: int, b: int) -> int

    Notes:  a or b nonzero
            return_val is the smallest positive integer divisible by both
    """
    if len(numbers) == 1:
        return abs(numbers[0])

    if len(numbers) > 2:
        return lcm(numbers[0], lcm(*numbers[1:]))

    a, b = numbers
    if a * b == 0:
        raise ValueError('lcm(_, 0) is undefined')

    return abs( a // gcd(a, b) * b)


#-----------------------------

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

# - - - - - - - - - - - - - - 

def bezout(a, b):
    """
    Bezout's Lemma: integer solution (x, y) to a*x + b*y = gcd(a, b)
        (a: int, b: int) -> (x: int, y: int)

    Notes:  a or b nonzero
            a*x + b*y == gcd(a, b)
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

#-----------------------------

def padic(number, base):
    """
    p-adic representation.
        (number: int, base: int) -> (exp: int, rest: int)

    Notes:  number nonzero
            base > 1
            num == (base ** exp) * rest
            rest % base != 0
    """
    if number == 0:
        raise ValueError('number must be nonzero')

    if base < 2:
        raise ValueError('base must be at least 2')

    exp = 0
    while number % base == 0:
        number //= base
        exp += 1

    return exp, number

#=============================

def integer_sqrt(number, guess=None):
    """
    Integer part of the square root of a number.
        (number: int, guess: int) -> int
    
    Note:   return_val**2 <= num < (return_val + 1)**2
    """
    if guess is None:
        guess = int(math.sqrt(number))

    while guess**2 > number or (guess+1)**2 <= number:
        guess = (guess + number // guess) // 2

    return guess

#-----------------------------

def is_square(number):
    """
    If a number is a perfect square.
        number: int -> bool
    """
    return integer_sqrt(number)**2 == number

#-----------------------------

def mod_inverse(number, modulus):
    """
    The inverse of under modular multiplication.
        (number: int, modulus: int) -> int

    Notes:  modulus > 1
            (number * return_val) % modulus == 1
    """
    if modulus < 2:
        raise ValueError('Modulus must be at least 2')

    x = bezout(number, modulus)[0]
    
    if number*x % modulus not in [1, -1]:
        raise ValueError(
                '{} is not invertible modulo {}'
                .format(number, modulus))

    if x < 0:
        return x + modulus

    return x

#-----------------------------

def mod_power(number, exponent, modulus):
    """
    Power of a number relative to a modulus.
        (number: int, exponent: int, modulus: int) -> int

    Notes:  modulus > 1
            exponent can be negative
            val == (num**exp) % mod
    """
    if modulus < 2:
        raise ValueError('Modulus must be at least 2')

    if exponent < 0:
        return pow(mod_inverse(number, modulus), -exponent, modulus)
    
    return pow(number, exponent, modulus)

#=============================

def _jacobi_helper(a, b):
    sign = 1
    while b != 1:
        e, r = padic(a % b, 2)
        if (e % 2, r % 4, b % 8) in [
            (0, 3, 3),
            (0, 3, 7),
            (1, 1, 3),
            (1, 1, 5),
            (1, 3, 5),
            (1, 3, 7)
        ]:
            sign *= -1
        a, b = b, r

    return sign

# - - - - - - - - - - - - - - 

def jacobi(a, b):
    """
    Jacobi symbol (a | b).
        (a: int, b: int) -> int

    Notes:  return_val in [1, 0, -1]
    """
    if b % 2 == 0:
        raise ValueError(
                'Jacobi symbol is undefined when second argument is even')

    if b == 1:
        return 1
    if gcd(a, b) != 1:
        return 0

    return _jacobi_helper(a, b)

#-----------------------------

def euler_criterion(a, p):
    """
    Euler criterion for (a | p)
        (a: int, p: int) -> int

    Notes:  p is prime
            gcd(a, p) == 1
            return_val == 1 if and only if a is a square modulo p
    """
    result = mod_power(a, (p-1)//2, p)

    if result == p - 1:
        return -1
    
    return 1

