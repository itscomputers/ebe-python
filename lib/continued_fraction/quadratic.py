#   lib/continued_fraction/quadratic.py
#   - module for continued fraction algorithm for square root D

# ===========================================================
from ..basic import gcd, integer_sqrt
from ..types.arithmetic_type import ArithmeticType
from ..types import frac, Quadratic

# ===========================================================
__all__ = [
    "continued_fraction_quotients",
    "continued_fraction_convergents",
    "continued_fraction_pell_numbers",
    "continued_fraction_table",
    "continued_fraction_all",
    "QuadraticContinuedFraction",
    "QuadraticRational",
    "Convergents",
]
# ===========================================================


def continued_fraction_quotients(root, max_length=None):
    """
    Compute the quotients of the continued fraction of `sqrt(root)`.

    + root: int --positive non-square
    + max_length: int --max number of iterations
    ~> List[int]
    """
    cf = QuadraticContinuedFraction(root, store_quotients=True)

    if max_length is None:
        cf.advance_all()
    else:
        cf.advance_until(max_length)

    return cf.quotients


# -----------------------------


def continued_fraction_convergents(root, max_length=None):
    """
    Compute the convergents of the continued fraction of `sqrt(root)`.

    + root: int --positive non-square
    + max_length: int --max number of iterations
    ~> List[Tuple[int, int]]
    """
    cf = QuadraticContinuedFraction(root, store_convergents=True)

    if max_length is None:
        cf.advance_all()
    else:
        cf.advance_until(max_length)

    return cf.convergents


# -----------------------------


def continued_fraction_pell_numbers(root, max_length=None):
    """
    Compute the Pell numbers associated to the continued fraction of `sqrt(root)`.

    + root: int --positive non-square
    + max_length: int --max number of iterations
    ~> List[int]
    """
    cf = QuadraticContinuedFraction(root, store_pell_numbers=True)

    if max_length is None:
        cf.advance_all()
    else:
        cf.advance_until(max_length)

    return cf.pell_numbers


# -----------------------------


def continued_fraction_table(root, max_length=None):
    """
    Compute the continued fraction table for `sqrt(root)`.

    + root: int --positive non-square
    + max_length: int --max number of iterations
    ~> List[Tuple[QuadraticRational, int, QuadraticRational]]
    """
    cf = QuadraticContinuedFraction(root, store_table=True)

    if max_length is None:
        cf.advance_all()
    else:
        cf.advance_until(max_length)

    return cf.table


# -----------------------------


def continued_fraction_all(root, max_length=None):
    """
    Compute all relevant data of continued fraction for `sqrt(root)`.

    + root: int -- positive non-square
    + max_length: int --max number of iterations
    ~> QuadraticContinuedFraction
    """
    cf = QuadraticContinuedFraction(root, store_all=True)

    if max_length is None:
        cf.advance_all()
    else:
        cf.advance_until(max_length)

    return cf


# ===========================================================


class QuadraticContinuedFraction:

    """
    Continued fraction algorithm for `sqrt(root)`.

    + root: int --positive non-square
    """

    def __init__(
        self,
        root,
        store_all=False,
        store_quotients=False,
        store_convergents=False,
        store_pell_numbers=False,
        store_table=False,
    ):
        """Initialize the continued fraction algorithm and data."""
        self.root = root
        self.approx = integer_sqrt(root)

        self.alpha = QuadraticRational(0, 1, 1, root, self.approx)
        self.quotient = self.alpha.floor
        self.beta = self.alpha - self.quotient
        self.convergent = Convergents()

        self.step = 0
        self.period = None

        self._storage_flags = {
            "quotients": store_all or store_quotients,
            "convergents": store_all or store_convergents,
            "pell_numbers": store_all or store_pell_numbers,
            "table": store_all or store_table,
        }
        self.data = dict()
        self._initialize_data()

    def _initialize_data(self):
        """Setup data storage."""
        if self._storage_flags["quotients"]:
            self.data["quotients"] = [self.quotient]
        if self._storage_flags["convergents"]:
            self.data["convergents"] = []
        if self._storage_flags["pell_numbers"]:
            self.data["pell_numbers"] = []
        if self._storage_flags["table"]:
            self.data["table"] = [(self.alpha, self.quotient, self.beta)]

    # -------------------------

    def __repr__(self):
        """Current state of the algorithm."""
        return "\n".join(
            [
                "step: {}".format(self.step),
                "alpha: {}".format(self.alpha),
                "quotient: {}".format(self.quotient),
                "beta: {}".format(self.beta),
                "convergent: {}".format(self.convergent.curr),
                "period: {}".format(self.period),
            ]
        )

    # -------------------------

    @property
    def quotients(self):
        if "quotients" in self.data:
            return self.data["quotients"]

    @property
    def convergents(self):
        if "convergents" in self.data:
            return self.data["convergents"]

    @property
    def pell_numbers(self):
        if "pell_numbers" in self.data:
            return self.data["pell_numbers"]

    @property
    def table(self):
        if "table" in self.data:
            return self.data["table"]

    # -------------------------

    def advance(self):
        """Advance to the next step in the algorithm."""
        self.convergent.advance(self.quotient)
        self.alpha = self.beta.inverse
        self.quotient = self.alpha.floor
        self.beta = self.alpha - self.quotient

        self.step += 1
        if self.alpha.arguments == (self.approx, 1, 1, self.root):
            self.period = self.step

        if self._storage_flags["quotients"]:
            self.data["quotients"].append(self.quotient)
        if self._storage_flags["convergents"]:
            self.data["convergents"].append(self.convergent.curr)
        if self._storage_flags["pell_numbers"]:
            self.data["pell_numbers"].append(self.convergent.to_pell_number(self.root))
        if self._storage_flags["table"]:
            self.data["table"].append((self.alpha, self.quotient, self.beta))

    # -------------------------

    def advance_until(self, max_length):
        """Advance until period complete of `max_length` reached."""
        while self.period is None and self.step < max_length:
            self.advance()

    def advance_all(self):
        """Advance until period complete."""
        while self.period is None:
            self.advance()


# ===========================================================


class QuadraticRational(ArithmeticType):

    """
    Class to represent `(real + imag * sqrt(root)) / denom` with
    necessary arithmetic for continued fraction algorithm.

    + real: int
    + imag: int
    + denom: int --non-zero
    + root : int --positive non-square
    """

    def __init__(self, real, imag, denom, root, approx_root=None):
        self._real = int(real)
        self._imag = int(imag)
        self._denom = int(denom)
        self.root = int(root)
        self.arguments = (real, imag, denom, root)
        self.approx_root = approx_root or integer_sqrt(root)

    def __repr__(self):
        return repr(self.to_quadratic)

    # -------------------------

    def _eq_QuadraticRational(self, other):
        return self.arguments == other.arguments

    def _eq_Quadratic(self, other):
        return self.signature == other.signature

    # -------------------------

    @property
    def real(self):
        return frac(self._real, self._denom)

    @property
    def imag(self):
        return frac(self._imag, self._denom)

    @property
    def signature(self):
        return (self.real, self.imag, self.root)

    @property
    def to_quadratic(self):
        return Quadratic(self.real, self.imag, self.root)

    # -------------------------

    @property
    def floor(self):
        """Floor of QuadraticRational."""
        return (self._real + self._imag * self.approx_root) // self._denom

    @property
    def inverse(self):
        """Inverse or reciprocal of QuadraticRational."""
        D = self._real ** 2 - self._imag ** 2 * self.root
        d = gcd(self._denom, D)
        m = self._denom // d

        def adjust(x):
            return -x if D < 0 else x

        return QuadraticRational(
            *map(adjust, (self._real * m, -self._imag * m, D // d)),
            self.root,
            self.approx_root
        )

    def _add_int(self, other):
        return QuadraticRational(
            self._real + self._denom * other,
            self._imag,
            self._denom,
            self.root,
            self.approx_root,
        )


# ===========================================================


class Convergents:

    """
    Class to represent pairs of convergents for continued fraction algorithm.
    """

    def __init__(self):
        self.prev = (0, 1)
        self.curr = (1, 0)

    # -------------------------

    def next_conv(self, quotient):
        """Calculate next convergent from current and previous."""
        return tuple(
            map(lambda tup: tup[1] + quotient * tup[0], zip(self.curr, self.prev))
        )

    def advance(self, quotient):
        """Replace previous with current and current with next."""
        self.prev, self.curr = self.curr, self.next_conv(quotient)

    def to_pell_number(self, root):
        """Calculate corresponding Pell number."""
        return self.curr[0] ** 2 - self.curr[1] ** 2 * root
