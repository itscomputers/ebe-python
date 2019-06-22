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

    quotient = number // divisor
    remainder = number % divisor
    if divisor < 0 and remainder != 0:
        quotient += 1
        remainder -= divisor

    return quotient, remainder

#-----------------------------

def div_with_small_remainder(number, divisor):
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
    quotient, remainder = div(number, divisor)
    
    if 2 * remainder > abs(divisor):
        remainder -= abs(divisor)
        quotient = (number - remainder) // divisor

    return quotient, remainder 

#-----------------------------

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
    q, r = division(a, b)
    print('{} = {} * {} + {}'.format(a, q, b, r))
    if r != 0:
        euclidean_algorithm(b, r, division)

#-----------------------------

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

#-----------------------------

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

#-----------------------------

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

#=============================

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

#-----------------------------

def is_square(number):
    """
    If a number is a perfect square.

    params
    number : int

    return
    bool
    """
    return integer_sqrt(number)**2 == number

#=============================

def mod_inverse(number, modulus):
    """
    The inverse of under modular multiplication.

    Computes inverse such that ``number * inverse % modulus == 1``

    params
    + number : int
        relatively prime to modulus
    + modulus : int
        greater than 1

    return
    int
    """
    if modulus < 2:
        raise ValueError('Modulus must be at least 2')

    inverse = bezout(number, modulus)[0]
    
    if number * inverse % modulus not in [1, -1]:
        raise ValueError(
                '{} is not invertible modulo {}'
                .format(number, modulus))

    if inverse < 0:
        inverse += modulus

    return inverse

#-----------------------------

def mod_power(number, exponent, modulus):
    """
    Power of a number relative to a modulus.
    
    Computes ``number ** exponent % modulus``, even for negative exponent.

    params
    + number : int
    + exponent : int
    + modulus : int
        greater than 1

    return
    int
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

    Computes the unique solution modulo product of moduli to the system 
        ``x % modulus == residue % modulus``
        for each pair in ``zip(residues, moduli)``

    params
    residues : iterable(int)
    moduli : interable(int)
        all greater than 1 and pair-wise relatively prime

    return
    int
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
    List of numbers which are relatively prime to list of given primes.

    Computes list of x for x < product of primes such that 
    ``gcd(x, product) == 1``.

    params
    primes : list(int)
        primes must be distinct primes

    return
    list(int)
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

    Computes primes up to max_value.

    params
    + max_value : int
    + primes : list(int)
        primes so far
    + numbers_left : list(int)
        numbers left to check

    return
    list(int)
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

    Determines if a number is prime by computing all primes up to its square root.

    params:
    + number : int
    + numbers_left : list(int)
        numbers left to check

    return
    bool
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
    Jacobi symbol.
    
    Computes the Jacobi symbol (a | b), generalization of Lagrange symbol.

    params:
    + a : int
    + b : int
        odd

    return
    int
        1, 0, or -1
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
    Euler criterion.

    Computes the Lagrange symbol (a | p) for p prime.
        * same as jacobi(a | p)
        * jacobi symbol is faster, this is primarily for testing purposes

    params:
    + a : int
        relatively prime to p
    + p : int
        prime

    return
    int
        * 1 if a is a square modulo p
        * -1 if a is not a square modulo p
    """
    result = mod_power(a, (p-1)//2, p)

    if result == p - 1:
        return -1
    
    return 1

