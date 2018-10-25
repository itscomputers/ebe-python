
#   numth/somefacts.py

from numth.factorization import Factorize
from numth.primality import\
        is_prime, next_prime, prev_prime,\
        next_twin_prime, prev_twin_prime,\
        prime_counting
from numth.quadratic import ContinuedFraction


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
        self.cf = ContinuedFraction(num)
        self.continued_fraction_table = self.cf.print_table(tablefmt='html')
        self.convergents = None
        self.pell_solutions = None
        self.sum_of_squares = None
        self.four_squares = None
        self.pi_digit = None
        self.complex_factorization = None
        self.pythagorean_triple = None
        self.fibonacci = None
