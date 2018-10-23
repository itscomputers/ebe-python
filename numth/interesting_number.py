
#   numth/somefacts.py

from numth.factorization import Factorize
from numth.primality import\
        is_prime, next_prime, prev_prime,\
        next_twin_prime, prev_twin_prime,\
        prime_counting


class InterestingNumber:

    def __init__(self, num):
        self.num = num
        self.factorization = Factorize(num)
        self.is_prime = is_prime(num)
        self.divisors = self.factorization.divisors()
        self.next_prime = next_prime(num)
        self.prev_prime = prev_prime(num)
        self.next_twin_primes = next_twin_primes(num)
        self.prev_twin_primes = prev_twin_primes(num)
        self.square_root = None 
        self.sum_of_squares = None
        self.four_squares = None
        self.pi_digit = None
        self.pell_solution = None
        self.complex_factorization = None
        self.pythagorean_triple = None
        self.fibonacci = None
