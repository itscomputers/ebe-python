#   numth/continued_fraction/quadratic.py
#===========================================================
from typing import Any, Dict, List, Tuple

from ..basic import gcd, integer_sqrt
from ..types import Quadratic
#===========================================================

def continued_fraction_quotients(root: int) -> List[int]:
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

    while not cf.complete():
        cf.advance()
        cf.record_quotient()

    return cf.quotients

#-----------------------------

def continued_fraction_convergents(root: int) -> List[Tuple[int, int]]:
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

    while not cf.complete():
        cf.advance()
        cf.record_convergent()

    return cf.convergents

#-----------------------------

def continued_fraction_pell_numbers(root: int) -> List[int]:
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

    while not cf.complete():
        cf.advance()
        cf.record_pell_number()

    return cf.pell_numbers

#-----------------------------

def continued_fraction_table(
        root: int,
        max_length: int = None
    ) -> List[Tuple['QuadraticRational', int, 'QuadraticRational']]:
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

    while not cf.complete():
        cf.advance()
        cf.record_row()

        if cf.at_max_length(max_length):
            break

    return cf.table

#-----------------------------

def continued_fraction_all(
        root: int,
        max_length: int = None
    ) -> Dict[str, Any]:
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

    while not cf.complete():
        cf.advance()
        cf.record_all()

        if cf.at_max_length(max_length):
            break

    return {
        'quotients'     :   cf.quotients,
        'convergents'   :   cf.convergents,
        'pell_numbers'  :   cf.pell_numbers,
        'table'         :   cf.table,
        'period'        :   cf.period,
        'complete'      :   cf.complete()
    }

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
    def __init__(self,
            real: int,
            imag: int,
            denom: int,
            root: int,
            approx_root: int = None
        ):
        self.real = real
        self.imag = imag
        self.denom = denom
        self.root = root
        self.components = (real, imag, denom)
        self.approx_root = approx_root or integer_sqrt(root)

    def __repr__(self) -> str:
        return '{}/{} + {}/{} sqrt({})'\
            .format(self.real, self.denom, self.imag, self.denom, self.root)

    def inverse(self) -> 'QuadraticRational':
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

    def floor(self) -> int:
        """Floor of QuadraticRational."""
        return (self.real + self.imag * self.approx_root) // self.denom

    def minus(self, integer) -> 'QuadraticRational':
        """Difference of integer from QuadraticRational."""
        return QuadraticRational(
            self.real - self.denom * integer,
            self.imag,
            self.denom,
            self.root,
            self.approx_root
        )

    def __eq__(self, other: Any) -> bool:
        return self.components == other.components and self.root == other.root

#=============================

class Convergents:
    """Class to represent convergent pairs for continued fraction algorithm."""
    def __init__(self):
        self.prev = (0, 1)
        self.curr = (1, 0)

    def next_conv(self, quotient: int) -> Tuple[Any, ...]:
        """Calculate next convergent from current and previous."""
        return tuple(map(
            lambda tup: tup[1] + quotient * tup[0],
            zip(self.curr, self.prev)
        ))

    def advance(self, quotient: int) -> None:
        """Replace previous with current and current with next."""
        self.prev, self.curr = self.curr, self.next_conv(quotient)

    def to_pell_number(self, root: int) -> int:
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
    def __init__(self, root: int):
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

        self.quotients = [self.quotient]
        self.convergents = []       #   type: List[Tuple[int, int]]
        self.pell_numbers = []      #   type: List[int]
        self.table = [(self.alpha, self.quotient, self.beta)]


    def __repr__(self) -> str:
        return 'alpha: {}\nquotient: {}\nbeta : {}\nconvergent: {}'\
            .format(self.alpha, self.quotient, self.beta, self.convergent.curr)

    def to_pell_number(self) -> int:
        """Computes corresponding Pell number for stage"""
        return self.convergent.to_pell_number(self.root)

    def advance(self) -> None:
        """Replaces values with next in the iteration."""
        self.convergent.advance(self.quotient)
        self.alpha = self.beta.inverse()
        self.quotient = self.alpha.floor()
        self.beta = self.alpha.minus(self.quotient)
        self.period += 1

    def record_quotient(self) -> None:
        self.quotients.append(self.quotient)

    def record_convergent(self) -> None:
        self.convergents.append(self.convergent.curr)

    def record_pell_number(self) -> None:
        self.pell_numbers.append(self.to_pell_number())

    def record_row(self) -> None:
        self.table.append((self.alpha, self.quotient, self.beta))

    def record_all(self) -> None:
        self.record_quotient()
        self.record_convergent()
        self.record_pell_number()
        self.record_row()

    def complete(self) -> bool:
        """Whether the algorithm has reached is at its periodic point."""
        return self.alpha.components == (self.approx, 1, 1)

    def at_max_length(self, max_length: int = None) -> bool:
        """Whether the algorithm is at a particular iteration."""
        return (max_length is not None) and self.period >= max_length

