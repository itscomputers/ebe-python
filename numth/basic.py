#   numth/basic.py
#===========================================================
from functools import reduce
from itertools import product
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
            number == (base ** exp) * rest
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

#=============================

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

#-----------------------------

def _chinese_remainder_coeffs(moduli, moduli_product):
    def coeff(modulus):
        partial = moduli_product // modulus
        return (partial * mod_inverse(partial, modulus)) % moduli_product

    return map(coeff, moduli)

#-----------------------------

def chinese_remainder_theorem(residues, moduli):
    """
    Chinese remainder theorem.
        (residues: iterable, moduli: iterable) -> int
    Notes:  return_val is the unique solution to the system
                x % modulus == residue % modulus 
                for each pair in zip(residues, moduli)
            requires that moduli are pair-wise relatively prime
    """
    moduli_product = reduce(lambda x, y: x * y, moduli, 1)
    
    return sum(map(
        lambda x, y: (x * y) % moduli_product,
        _chinese_remainder_coeffs(moduli, moduli_product),
        residues)
    ) % moduli_product

#-----------------------------

def prime_to(*primes):
    """
    List of numbers which are prime to the given primes.
        (primes: iterable of int) -> list
    Notes:  return_val is list of x for x < product of primes
                such that gcd(x, product) == 1
    """
    primes_product = reduce(lambda x, y: x * y, primes, 1)
    coeffs = list(_chinese_remainder_coeffs(primes, primes_product))

    return sorted(
        sum(map(
            lambda x, y: (x * y) % primes_product,
            _chinese_remainder_coeffs(primes, primes_product),
            residues)
        ) % primes_product \
    for residues in product(*(range(1, x) for x in primes)))

#=============================

def prime_sieve(max_value, primes=None, numbers_left=None):
    """
    Sieve of Eratosthenes.
        (max_value: int, primes: list, numbers_left: iterable) -> list
    Notes:  return_value is list of primes less than max_value
    """
    if primes is None and numbers_left is None:
        primes = []
        numbers_left = (x for x in range(2, max_value + 1))
    try:
        min_value = next(numbers_left)
    except StopIteration:
        return primes

    if min_value**2 >= max_value:
        return primes + [min_value] + list(numbers_left)

    return prime_sieve(
        max_value,
        primes + [min_value],
        (x for x in numbers_left if x % min_value != 0)
    )

#-----------------------------

def is_prime__naive(number, numbers_left=None):
    """
    Primality testing using Sieve of Eratosthenes.
        (number: int, numbers_left: iterable) -> bool
    Notes:  return_value is whether number is prime
    """
    if number < 2:
        return False

    if numbers_left is None:
        numbers_left = (x for x in range(2, integer_sqrt(number) + 1))
    
    try:
        min_value = next(numbers_left)
    except StopIteration:
        return True

    if number % min_value == 0:
        return False

    return is_prime__naive(
        number,
        (x for x in numbers_left if x % min_value != 0)
    )

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

