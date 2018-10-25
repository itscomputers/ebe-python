
#   numth/quadratic.py

from numth.main import\
        mod_inverse,\
        mod_sqrt_minus_one,\
        generator_range,\
        generator_nth
from numth.rational import Rational, frac, sqrt, is_square 
import tabulate

##############################

def _default_values(cat):
    if cat == 'decimal':
        return 20
    if cat == 'continued fraction':
        return 10

##############################

def quad(real, imag, root, mod=None):
    """Shortcut for creating instance of Quadratic class."""
    return Quadratic(real, imag, root, mod)

##############################

def gaussian(real, imag):
    """Shortcut for creating Gaussian integer or rational."""
    return Quadratic(real, imag, -1)

##############################

def gaussian_divisor(prime):
    """
    Find Gaussian integer divisor of a prime.

    Args:   int:        prime       must be a prime number

    Return: Gaussian:   d           d is irreducible and divides prime
    """
    if prime % 4 == 3:
        raise ValueError('{} does not split over Z[i]'.format(prime))

    s = min(mod_sqrt_minus_one(prime))
    d = gaussian(prime, 0).gcd(gaussian(s, 1))

    return d

############################################################
############################################################
#       Quadratic ring class
############################################################
############################################################

class Quadratic:
    """
    Quadratic integer class.

    Args:   int:            real, imag, root, mod
    
    Return: Quadratic:   real + imag * sqrt(root)  [optional: % mod]
    """
    def __init__(self, real, imag, root, mod=None):
        """Initialize quadratic element."""
        if (mod is not None) and (isinstance(mod, int) or mod < 2):
            raise ValueError('Invalid modulus')
        self.mod = mod
        self.real = self.r(real)
        self.imag = self.r(imag)
        self.root = self.r(root)

    ##########################

    def __repr__(self):
        """Print quadratic element."""
        if self.root == -1 or (self.mod and self.root == self.mod - 1):
            root_disp = '\u2139'
        elif isinstance(self.root, int):
            root_disp = '\u221a{}'.format(self.root)
        else:
            root_disp = '\u221a({})'.format(self.root)
       
        if abs(self.imag) == 1:
            imag_part = root_disp
        else:
            imag_part = '{} {}'.format(abs(self.imag), root_disp)

        if self.imag == 0:
            return format(self.real)
        elif self.real == 0:
            if self.imag > 0:
                return imag_part
            else:
                return '-' + imag_part
        elif self.imag < 0:
            return '{} - {}'.format(self.real, imag_part)
        else:
            return '{} + {}'.format(self.real, imag_part)

    ##########################

    def r(self, num):
        if self.mod is not None:
            return num % self.mod
        else:
            return num

    ##########################

    def norm(self):
        """Norm of quadratic element."""
        return self.r(self.real**2 - self.root * self.imag**2)

    ##########################

    def conjugate(self):
        """Conjugate of quadratic element."""
        return Quadratic(self.real, -self.imag, self.root, self.mod)

    ##########################

    def inverse(self):
        """Inverse of quadratic element."""
        norm = self.r(self.norm())
        if self.mod is not None:
            norm_inverse = mod_inverse(norm, self.mod)
        elif abs(norm) == 1:
            norm_inverse = norm
        else:
            norm_inverse = frac(norm).inverse()
        
        new_real = self.real * norm_inverse
        new_imag = -self.imag * norm_inverse
        return Quadratic(new_real, new_imag, self.root, self.mod)

    ##########################

    def pell_number(self, convergent):
        if isinstance(convergent, Rational):
            a, b = convergent.numer, convergent.denom
        else:
            a, b = convergent
        return int((a + b*self) * (a + b*self.conjugate()))

    ##########################

    def canonical(self):
        if self.root == -1:
            canon = self
            if abs(canon.real) < abs(canon.imag):
                canon = canon * Quadratic(0, 1, -1)
            if canon.real < 0:
                canon = -canon
            return canon
        else:
            raise ValueError('canonical not defined for sqrt({})'.format(self.root))

    ##########################

    def gcd(self, other):
        if self.root == -1:
            if isinstance(other, int):
                other = Quadratic(other, 0, self.root)
            if other == 0:
                return self.canonical()
            else:
                return other.gcd(self % other)
        else:
            raise ValueError('canonical not defined for sqrt({})'.format(self.root))

    ##########################

    def __neg__(self):
        return Quadratic(-self.real, -self.imag, self.root, self.mod)

    def __int__(self):
        return int(self.real + self.imag * sqrt(self.root))

    def __float__(self):
        return float(self.real + self.imag * sqrt(self.root))

    def __round__(self):
        f = float(self)
        if f >= 0:
            return int(float(self) + .5)
        else:
            return int(float(self) - .5)

    def decimal(self, num_digits=None):
        if num_digits is None:
            num_digits = _default_values('decimal')
        if self.imag > 1:
            sqrt_digits = num_digits
        else:
            sqrt_digits = num_digits + len(str(int(1/self.imag)))
        return (self.real +\
                self.imag *\
                sqrt(self.root, num_digits=sqrt_digits)\
                ).decimal(num_digits)

    ##########################

    def __add__(self, other):
        if isinstance(other, int):
            other = Quadratic(other, 0, self.root, self.mod)
        if self.root != other.root:
            raise ValueError('Incompatible quadratic integers')
        new_real = self.real + other.real
        new_imag = self.imag + other.imag
        return Quadratic(new_real, new_imag, self.root, self.mod)

    def __radd__(self, other):
        return self + other

    def __iadd__(self, other):
        return self + other

    ##########################

    def __sub__(self, other):
        if isinstance(other, int):
            other = Quadratic(other, 0, self.root, self.mod)
        if self.root != other.root:
            raise ValueError('Incompatible quadratic integers')
        return -other + self 

    def __rsub__(self, other):
        return -self + other

    def __isub__(self, other):
        return self - other

    ##########################

    def __mul__(self, other):
        if not isinstance(other, Quadratic):
            other = Quadratic(other, 0, self.root, self.mod)
        if self.root != other.root:
            raise ValueError('Incompatible quadratic integers')
        new_real = self.real * other.real + self.root * self.imag * other.imag
        new_imag = self.real * other.imag + self.imag * other.real
        return Quadratic(new_real, new_imag, self.root, self.mod)

    def __rmul__(self, other):
        return self * other 
        
    def __imul__(self, other):
        return self * other

    ##########################

    def __truediv__(self, other):
        if not isinstance(other, Quadratic):
            other = Quadratic(other, 0, self.root, self.mod)
        return self * other.inverse() 

    def __rtruediv__(self, other):
        return Quadratic(other, 0, self.root, self.mod) / self

    def __itruediv__(self, other):
        return self / other

    ##########################

    def __floordiv__(self, other):
        if self.mod:
            return self / other
        else:
            new = self / other
            new_real = int(new.real)
            new_imag = int(new.imag)
            return Quadratic(new_real, new_imag, self.root, self.mod)

    def __rfloordiv__(self, other):
        return Quadratic(other, 0, self.root, self.mod) // self

    def __ifloordiv__(self, other):
        return self // other

    ##########################

    def __pow__(self, other):
        if other < 0:
            return self.inverse()**other
        elif other == 0:
            return Quadratic(1, 0, self.root, self.mod)
        elif other == 1:
            return self
        elif other % 2 == 0:
            return (self * self)**(other // 2)
        else:
            return self * (self * self)**(other // 2)

    def __ipow__(self, other):
        return self**other

    ##########################

    def __mod__(self, other):
        if isinstance(other, Quadratic):
            return self - (self // other) * other

        if isinstance(other, int):
            new_real = self.real % other
            new_imag = self.imag % other
            return Quadratic(new_real, new_imag, self.root, self.mod)

    def __rmod__(self, other):
        return Quadratic(other, 0, self.root, self.mod) % self

    def __imod__(self, other):
        return self % other

    ##########################

    def __eq__(self, other):
        if other == 0:
            return self.real == 0 and self.imag == 0
        return      self.real == other.real\
                and self.imag == other.imag\
                and self.root == other.root\
                and self.mod  == other.mod

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if self.mod:
            raise ValueError('Comparison undefined in modular arithmetic')
        return self.norm() < other.norm()

    def __ge__(self, other):
        return not self < other

    def __gt__(self, other):
        if self.mod:
            raise ValueError('Comparison undefined in modular arithmetic')
        return self.norm() > other.norm()

    def __le__(self, other):
        return not self > other

############################################################
############################################################
#       Gaussian integers/rationals
############################################################
############################################################

class Gaussian(Quadratic):

    def __init__(self, real, imag):
        self.real = real
        self.imag = imag
        self.root = -1
        self.mod = None

    ##########################

    def canonical(self):
        canon = self
        if abs(canon.real) < abs(canon.imag):
            canon = canon * Gaussian(0,1)
        if abs(canon.real) < 0:
            canon = -canon
        return canon

    ##########################

    def gcd(self, other):
        if isinstance(other, int):
            other = Gaussian(other, 0)

        if other == 0:
            return self.canonical()
        else:
            return other.gcd(self % other)

############################################################
############################################################
#       Quadratic continued fractions
############################################################
############################################################

class ContinuedFraction:

    def __init__(self, num, num_rows=None):
        if not isinstance(num, int) or num < 2 or is_square(num):
            raise ValueError('only positive non-square integers allowed')
        self.num = Quadratic(0, 1, num)
        self.period = None
        self.length = 0
        self.is_complete = False
        self.table = None
        self.pre_coeff = None
        self.coeffs = []
        self.beta = None
        self.convergents = [(1, 0)]
        self.pell_numbers = None
        self.initialize_table(num_rows)

    ##########################

    def __repr__(self):
        display = _default_values('continued fraction')
        self.print_table(display)
        self.print_coeffs(display)
        return ''

    ##########################

    def initialize_table(self, num_rows=None):
        if num_rows is None:
            num_rows = _default_values('continued fraction')
        alpha = self.num
        q = int(alpha)
        beta = alpha - q
        convergent = (q, 1)
        self.pre_coeff = q
        self.table = [(alpha, q, beta)]
        self.length += 1
        self.beta = beta
        self.convergents.append(convergent)
        self.pell_numbers = [self.num.pell_number(convergent)]
        self.extend(num_rows)
        if self.is_complete:
            self.period = self.length - 1

    ##########################

    def get_next(self):
        if not self.is_complete:
            alpha, q, beta = self.table[-1]

            alpha = 1 / beta
            q = int(alpha)
            beta = alpha - q

            self.coeffs.append(q)
            self.table.append((alpha, q, beta))

            (a0, b0), (a1, b1) = self.convergents[-2:]
            convergent = (q * a1 + a0, q * b1 + b0)
            self.convergents.append(convergent)
            self.pell_numbers.append(self.num.pell_number(convergent))

            if beta == self.beta:
                self.is_complete = True
                self.period = self.length - 1

    ##########################

    def extend(self, num_rows=None):
        while not self.is_complete:
            if num_rows is not None and self.length >= num_rows:
                break
            self.get_next()
            self.length += 1

    ##########################

    def _restrict(self, array, display=None, vertical=True):
        if not self.is_complete or (display is not None and self.length > display):
            array_display = array[:display]
            if vertical:
                array_display.append(('\u22ee',) * len(array[0]))
            else:
                array_display.append('...')
            return array_display
        else:
            return array

    ##########################

    def print_table(self, display=None, tablefmt='fancy_grid'):
        table = [ [str(x) for x in row] for row in self.table ]
        table = self._restrict(table, display)
        headers = ['alpha', 'q', 'beta']
        print('\n' + tabulate.tabulate(table, headers=headers, tablefmt=tablefmt))

    ##########################

    def print_coeffs(self, display=None):
        coeffs = [str(x) for x in self.coeffs]
        coeffs = self._restrict(coeffs, display, vertical=False)
        print('[ {} ; {} ]'.format(self.pre_coeff, ', '.join(coeffs)))

    ##########################

    def print_convergents(self, display=None, tablefmt='fancy_grid'):
        convergents = [[
            Rational(c[0], c[1]).display(), 
            Rational(c[0], c[1]).decimal(10)
            ] for c in self.convergents[1:] ]
        convergents = self._restrict(convergents, display)
        headers = ['convergent', 'convergent']
        tabulate.PRESERVE_WHITESPACE=True
        print('\n' + tabulate.tabulate(
            convergents,
            headers=headers,
            tablefmt=tablefmt,
            floatfmt='.10f'))

    ##########################

    def convergents_gen(self):
        a0, b0 = 1, 0
        a1, b1 = self.pre_coeff, 1
        i = 0
        while True:
            yield Rational(a1, b1)
            q = self.coeffs[i]
            a0, a1 = a1, q*a1 + a0
            b0, b1 = b1, q*b1 + b0
            i = (i + 1) % self.period

    ##########################

    def _solution_to_element(self, solution):
        a, b = solution
        return a + b*self.num

    ##########################

    def _element_to_solution(self, element):
        y = int((element - element.conjugate())\
                / (2 * (self.num - self.num.real)))
        x = int((element + element.conjugate()) / 2 - y * self.num.real)
        return (x, y)

    ##########################

    def pell_solutions_gen(self, include_minus_one=False):
        first_solution = self.convergents[-2]
        first_element = self._solution_to_element(first_solution)
        if not include_minus_one and self.pell_numbers[-2] != 1:
            first_element = first_element**2
            first_solution = self._element_to_solution(first_element)
        solution = first_solution
        element = first_element
        while True:
            yield solution
            element = element * first_element
            solution = self._element_to_solution(element)

    ##########################

    def convergents_range(self, lower, upper):
        return generator_range(self.convergents_gen, lower, upper)

    ##########################

    def convergent_nth(self, n):
        return generator_nth(self.convergents_gen, n)

    ##########################

    def pell_solutions_range(self, lower, upper):
        return generator_range(
                self.pell_solutions_gen, lower, upper)

    ##########################

    def pell_solution_nth(self, n):
        return generator_nth(self.pell_solutions_gen, n)

    ##########################

    def find_convergents(self, denom_digits):
        psg = self.pell_solutions_gen(True)
        lower_ps = (1, 0)
        upper_ps = next(psg)
        while len(str(upper_ps[1])) < denom_digits:
            lower_ps, upper_ps = upper_ps, next(psg)

        first, second = None, None
        while first is None and second is None:
            offset_element = self._solution_to_element(lower_ps)
            for c in self.convergents[1:]:
                element = self._solution_to_element(c)
                convergent = self._element_to_solution(element * offset_element)
                if len(str(convergent[1])) >= denom_digits:
                    if first is None:
                        first = convergent
                    else:
                        second = convergent
                        break
            lower_ps, upper_ps = upper_ps, next(psg)

        if first[0] * second[1] < first[1] * second[0]:
            lower_bound = Rational(first[0], first[1])
            upper_bound = Rational(second[0], second[1])
        else:
            upper_bound = Rational(first[0], first[1])
            lower_bound = Rational(second[0], second[1])
        
        return lower_bound, upper_bound

############################################################
############################################################
#       End
############################################################
############################################################
