
#   numth/interestingnumber.py

from numth.factorization import Factorize
from numth.primality import\
        is_prime, next_prime, prev_prime,\
        next_twin_primes, prev_twin_primes,\
        prime_count, goldbach_partition,\
        primes_in_range
from numth.quadratic import ContinuedFraction, Quadratic, lucas_sequence_nth
from numth.rational import\
        frac,\
        integer_sqrt, sqrt,\
        is_square, which_shape_number

from random import randint, choice
from itertools import product

##############################

def shape_dictionary():
    return {
        3   :   'triangular',
        4   :   'square',
        5   :   'pentagonal',
        6   :   'hexagonal',
        7   :   'heptagonal',
        8   :   'octagonal',
        9   :   'nonagonal',
        10  :   'decagonal',
        11  :   'hendecagonal',
        12  :   'dodecagonal',
        13  :   'tridecagonal',
        14  :   'tetradecagonal',
        15  :   'pentadecagonal',
        16  :   'hexadecagonal',
        17  :   'heptadecagonal',
        18  :   'octadecagonal',
        19  :   'enneadecagonal',
        20  :   'icosogonal'
    }

############################################################
############################################################
#       Interesting number class
############################################################
############################################################

class InterestingNumber:
    """Every number is interesting."""

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
        self.shapes = self.get_shapes()

    ##########################

    def get_fibonacci(self):
        if self.num < 10**5:
            return lucas_sequence_nth(1, -1, 0, 1, self.num)

    ##########################

    def print_fibonacci(self):
        fib_str = str(self.fibonacci)
        if len(fib_str) < 20:
            return (len(fib_str), fib_str)
        else:
            return (len(fib_str), '{}....{}'.format(fib_str[:8], fib_str[-8:]))

    ##########################

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

    ##########################

    def get_shapes(self):
        shapes = []
        for s in range(3,21):
            n = which_shape_number(self.num, s)
            if n is not None:
                shapes.append((s,n))
        return shapes

############################################################
############################################################
#       End
############################################################
############################################################
