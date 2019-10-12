#   numth/continued_fraction/quadratic.py
#===========================================================
from ..basic import gcd, integer_sqrt
#===========================================================

def continued_fraction_quotients(root):
    """
    Compute the quotients of the continued fraction of sqrt(root).

    The quotients are periodic with `q_0` separate
    and `q_1, ..., q_n = 2*q_0` repeating.

    params
    + root : int
        positive non-square

    return
    list(int)
    """
    cf = ContinuedFraction(root)
    quotients = [cf.quotient]

    while not cf.complete():
        cf.advance()
        quotients.append(cf.quotient)

    return quotients

#-----------------------------

def continued_fraction_convergents(root):
    """
    Compute the convergents of the continued fraction of sqrt(root).

    The convergents after the periodicity can be found using quadratic integers.
    The rational number corresponding to a convergent (numer, denom) is a
    rational approximation of sqrt(root).

    params
    + root : int
        positive non-square

    return
    list((int, int))
    """
    cf = ContinuedFraction(root)
    convergents = []

    while not cf.complete():
        cf.advance()
        convergents.append(cf.convergent.curr)

    return convergents

#-----------------------------

def continued_fraction_pell_numbers(root):
    """
    Compute the Pell numbers associated to the continued fraction of sqrt(root).

    For a convergent `(x, y)`, the Pell number is `x**2 - root * y**2`.

    params
    + root : int
        positive non-square

    return
    list(int)
    """
    cf = ContinuedFraction(root)
    pell_numbers = []

    while not cf.complete():
        cf.advance()
        pell_numbers.append(cf.to_pell_number())

    return pell_numbers

#-----------------------------

def continued_fraction_table(root, max_length=None):
    """
    Compute the continued fraction table for sqrt(root).

    The table rows have columns `alpha`, `quotient`, and `beta`
    satisfying `beta = alpha - quotient` and `next_alpha = 1 / beta`.
    The final `beta` is equal to the initial `beta`,
    which makes the table periodic.

    params
    + root : int
        non-square

    return
    list((QuadraticRational, int, QuadraticRational))
    """
    cf = ContinuedFraction(root)
    rows = [(cf.alpha, cf.quotient, cf.beta)]

    while not cf.complete():
        cf.advance()
        rows.append((cf.alpha, cf.quotient, cf.beta))

        if cf.at_max_length(max_length):
            rows.append(('...', '...', '...'))
            break

    return rows

#-----------------------------

def continued_fraction_all(root, max_length=None):
    """
    Compute all relevant data of continued fraction table for sqrt(root).

    Same as above functionality, but computed simultaneously.
    * optional parameter to only compute the continued fraction up to a point.
    * additional field `complete` is false if computation was terminated
        early because of max_length.
    * period is either the actual period max_length.

    params
    + root : int
        non-square
    + max_length : int
        max number of iterations

    return
    dict
    """
    cf = ContinuedFraction(root)
    result = {
        'quotients'     :   [cf.quotient],
        'convergents'   :   [],
        'pell_numbers'  :   [],
        'table'         :   [(cf.alpha, cf.quotient, cf.beta)]
    }

    while not cf.complete():
        cf.advance()
        result['quotients'].append(cf.quotient)
        result['convergents'].append(cf.convergent.curr)
        result['pell_numbers'].append(cf.to_pell_number())
        result['table'].append((cf.alpha, cf.quotient, cf.beta))

        if cf.at_max_length(max_length):
            break

    result['period'] = cf.period
    result['complete'] = cf.complete()
    return result

#=============================

class QuadraticRational:
    """
    Class to represent `(real + imag * sqrt(root)) / denom` with
    necessary arithmetic for continued fraction algorithm.

    params
    + real : int
    + imag : int
    + denom : int
        non-zero
    + root : int
        positive non-square
    """
    def __init__(self, real, imag, denom, root, approx_root=None):
        self.real = real
        self.imag = imag
        self.denom = denom
        self.root = root
        self.components = (real, imag, denom)
        self.approx_root = approx_root or integer_sqrt(root)

    def __repr__(self):
        return '{}/{} + {}/{} sqrt({})'\
            .format(self.real, self.denom, self.imag, self.denom, self.root)

    def inverse(self):
        """Inverse or reciprocal of QuadraticRational."""
        D = self.real**2 - self.imag**2 * self.root
        d = gcd(self.denom, D)
        m = self.denom // d
        real = self.real * m
        imag = -self.imag * m
        denom = D // d
        if D < 0:
            real, imag, denom = map(lambda x: -x, (real, imag, denom))
        return QuadraticRational(real, imag, denom, self.root, self.approx_root)

    def floor(self):
        """Floor of QuadraticRational."""
        return (self.real + self.imag * self.approx_root) // self.denom

    def minus(self, integer):
        """Difference of integer from QuadraticRational."""
        return QuadraticRational(
            self.real - self.denom * integer,
            self.imag,
            self.denom,
            self.root,
            self.approx_root
        )

    def __eq__(self, other):
        return self.components == other.components and self.root == other.root

#=============================

class Convergents:
    """Class to represent convergent pairs for continued fraction algorithm."""
    def __init__(self):
        self.prev = (0, 1)
        self.curr = (1, 0)

    def next_conv(self, quotient):
        """Calculate next convergent from current and previous."""
        return tuple(map(
            lambda tup: tup[1] + quotient * tup[0],
            zip(self.curr, self.prev)
        ))

    def advance(self, quotient):
        """Replace previous with current and current with next."""
        self.prev, self.curr = self.curr, self.next_conv(quotient)

    def to_pell_number(self, root):
        """Calculate corresponding Pell number."""
        return self.curr[0]**2 - self.curr[1]**2 * root

#=============================

class ContinuedFraction:
    """
    Class for performing continued fraction algorithm.

    params
    + root : int
        positive non-square
    """
    def __init__(self, root):
        """
        Initializes the root, its approximate square root,
        the first row `alpha, quotient, beta` of the table,
        the initial two convergent pairs, and the period.
        """
        self.root = root
        self.approx = integer_sqrt(root)
        self.alpha = QuadraticRational(0, 1, 1, root, self.approx)
        self.quotient = self.alpha.floor()
        self.beta = self.alpha.minus(self.quotient)
        self.convergent = Convergents()
        self.period = 0

    def __repr__(self):
        return 'alpha: {}\nquotient: {}\nbeta : {}\nconvergent: {}'\
            .format(self.alpha, self.quotient, self.beta, self.convergent.curr)

    def to_pell_number(self):
        """Computes corresponding Pell number for stage"""
        return self.convergent.to_pell_number(self.root)

    def advance(self):
        """Replaces values with next in the iteration."""
        self.convergent.advance(self.quotient)
        self.alpha = self.beta.inverse()
        self.quotient = self.alpha.floor()
        self.beta = self.alpha.minus(self.quotient)
        self.period += 1

    def complete(self):
        """Whether the algorithm has reached is at its periodic point."""
        return self.alpha.components == (self.approx, 1, 1)

    def at_max_length(self, max_length=None):
        """Whether the algorithm is at a particular iteration."""
        return (max_length is not None) and self.period >= max_length

