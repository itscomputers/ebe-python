
#   numth/interestingnumber.py

from numth.factorization import Factorize
from numth.primality import\
        is_prime, next_prime, prev_prime,\
        next_twin_primes, prev_twin_primes,\
        prime_count, goldbach_partition
from numth.quadratic import ContinuedFraction, Quadratic
from numth.rational import frac, is_square, integer_sqrt, sqrt

from random import randint, choice
from time import time

class InterestingNumber:

    def __init__(self, num, TIMED=False):
        self.num = num
        self.factorize = Factorize(num)
        self.is_prime = is_prime(num, 10, 4)
        self.next_prime = next_prime(num, [2,3,5,7], 10, 4)
        self.next_twin_primes = next_twin_primes(num, [2,3,5,7], 10, 4)
        self.goldbach_partition = goldbach_partition(num, [2,3,5,7], 10, 4)
        if is_square(num):
            self.sqrt = {'sqrt' : integer_sqrt(num)}
        else:
            cf = ContinuedFraction(num, num_rows=8)
            self.sqrt = {
                'sqrt'      :   sqrt(num, 20).decimal(20),
                'cf'        :   cf,
                'table'     :   cf.get_table(tablefmt='html'),
                'coeffs'    :   cf.get_coeffs(),
                'approx'    :   cf.find_convergents(3)
            }
        self.factorization = self.factorize.factorization
        self.divisors = self.factorize.divisors()
        self.euler_phi = self.factorize.euler_phi
        self.carmichael_lambda = self.factorize.carmichael_lambda
        self.two_squares = self.factorize.two_squares()
        self.four_squares = self.factorize.four_squares()
        self.fibonacci = self.get_fibonacci()
        self.pythagorean_triple = self.get_pythagorean_triple()

    def get_fibonacci(self):
        if self.num < 10**5:
            gamma = Quadratic(frac(1,2), frac(1,2), 5)
            return int(2 * (gamma**self.num).imag)

    def print_fibonacci(self):
        fib_str = str(self.fibonacci)
        if len(fib_str) < 20:
            return (len(fib_str), fib_str)
        else:
            return (len(fib_str), '{}....{}'.format(fib_str[:8], fib_str[-8:]))

    def get_pythagorean_triple(self):
        if self.two_squares is not None:
            m, n = self.two_squares

        else:
            a = self.divisors[len(self.divisors) // 2]
            b = self.num // a

            if self.num % 2 == 0:
                if a % 2 == 0:
                    a = a // 2
                else:
                    b = b // 2
                n, m = sorted([a, b])

            else:
                m = (a + b) // 2
                n = abs(b - m)

        m2, n2 = m**2, n**2
        a = m2 - n2
        b = 2 * m * n
        c = m2 + n2

        return tuple(sorted([a, b, c]))

