#   lib/algebraic_structures/modular_ring.py
#   - class for ring of integers relative to a modulus

# ===========================================================
from collections import Counter
from functools import reduce

from ..basic import gcd, mod_inverse, mod_power, prime_to
from ..factorization import factor
from ..modular import carmichael_lambda, euler_phi, mod_sqrt

# ===========================================================
__all__ = [
    "ModularRing",
]
# ===========================================================


class ModularRing:

    """
    Class for computations in the ring of integers relative to a modulus.
    """

    def __init__(self, modulus):
        self.modulus = modulus
        if modulus == 2:
            self.orders = {1: 1}
            self.inverses = {1: 1}
        else:
            self.orders = {1: 1, modulus - 1: 2}
            self.inverses = {1: 1, modulus - 1: modulus - 1}

        self._factorization = None
        self._euler = None
        self._carmichael = None
        self._carmichael_factorization = None
        self._multiplicative_group = None
        self._generator = None
        self._cyclic_group_dict = None
        self._discrete_log_dict = None

    # =========================

    def factorization(self):
        """Factorize the modulus."""
        if self._factorization is None:
            self._factorization = factor(self.modulus)
        return self._factorization

    # -------------------------

    def euler(self):
        """Compute size of multiplicative group."""
        if self._euler is None:
            self._euler = euler_phi(self.factorization())
        return self._euler

    # -------------------------

    def carmichael(self):
        """Compute maximum order of element of multiplicative group."""
        if self._carmichael is None:
            self._carmichael = carmichael_lambda(self.factorization())
        return self._carmichael

    # -------------------------

    def carmichael_factorization(self):
        """Factorize the maximum order.  Used for calculating orders."""
        if self._carmichael_factorization is None:
            self._carmichael_factorization = factor(self.carmichael())
        return self._carmichael_factorization

    # -------------------------

    def carmichael_primes(self):
        """Prime factors of maximum order.  Used for calculating orders."""
        return Counter(self.carmichael_factorization()).elements()

    # -------------------------

    def is_cyclic(self):
        """Determine if the multiplicative group is cyclic."""
        return self.euler() == self.carmichael()

    # -------------------------

    def is_field(self):
        """Determine if the modular ring is a field."""
        return self.euler() == self.modulus - 1

    # -------------------------

    def multiplicative_group(self):
        """Compute the multiplicative group."""
        if self._multiplicative_group is None:
            self._multiplicative_group = prime_to(self.factorization())
        return self._multiplicative_group

    # -------------------------

    def generator(self):
        """Find a generator of the multiplicative group if cyclic."""
        if self._generator is None and self.is_cyclic():
            for x in self.multiplicative_group():
                if self.order_of(x) == self.euler():
                    self._generator = x
                    break
        return self._generator

    # -------------------------

    def cyclic_group_dict(self):
        """Realize multiplicative group as a cyclic group for a generator."""
        if self._cyclic_group_dict is None and self.is_cyclic():
            self._cyclic_group_dict = self.cyclic_subgroup_from(self.generator())
            if self._multiplicative_group is None:
                self._multiplicative_group = sorted(self._cyclic_group_dict.values())
        return self._cyclic_group_dict

    # -------------------------

    def discrete_log_dict(self):
        """Compute a discrete log table for multiplicative group if cyclic."""
        if self._discrete_log_dict is None and self.is_cyclic():
            self._discrete_log_dict = {x: e for e, x in self.cyclic_group_dict().items()}
        return self._discrete_log_dict

    # -------------------------

    def all_orders(self):
        """Compute orders of all elements of multiplicative group."""
        if len(self.orders) != self.euler():
            if self.is_cyclic():
                self.generator()
            for x in self.multiplicative_group():
                self.order_of(x)
        return self.orders

    # -------------------------

    def all_inverses(self):
        """Compute inverses of all elements of multiplicative group."""
        if len(self.inverses) != self.euler():
            if self.is_cyclic():
                self.generator()
            for x in self.multiplicative_group():
                self.inverse_of(x)
        return self.inverses

    # -------------------------

    def all_generators(self):
        """Compute all generators of multiplicative group if cyclic."""
        return [x for x, o in self.all_orders().items() if o == self.euler()]

    # =========================

    def elem(self, number):
        """Cast number to element of modular ring."""
        return number % self.modulus

    # -------------------------

    def neg(self, element):
        """Negation of element in modular ring."""
        return self.elem(-element)

    # -------------------------

    def add(self, *elements):
        """Add elements in modular ring."""
        return reduce(lambda x, y: (x + y) % self.modulus, map(self.elem, elements), 0)

    # -------------------------

    def mult(self, *elements):
        """Multiply elements in modular ring."""
        return reduce(lambda x, y: (x * y) % self.modulus, map(self.elem, elements), 1)

    # -------------------------

    def power_of(self, element, exponent):
        """Compute power of element in modular ring."""
        return mod_power(element, exponent, self.modulus)

    # -------------------------

    def inverse_of(self, element):
        """Compute inverse of element of multiplicative group."""
        if element not in self.inverses:
            if self._generator is not None:
                inverse = self.exp_of(-self.log_of(element) % self.euler())
            else:
                inverse = mod_inverse(element, self.modulus)
            self.inverses[element] = inverse
            self.inverses[inverse] = element
        return self.inverses[element]

    # -------------------------

    def sqrt_of(self, element):
        """Compute square roots of element of multiplicative group if modulus is prime."""
        if self._generator is not None:
            index = self.log_of(element)
            if index % 2 == 0:
                sqrt = self.exp_of((index // 2))
                return tuple(sorted([sqrt, self.neg(sqrt)]))
        if self.is_field():
            return mod_sqrt(element, self.modulus)

    # -------------------------

    def log_of(self, element):
        """Compute exponent of element of multiplicative relative to generator."""
        return self.discrete_log_dict()[self.elem(element)]

    # -------------------------

    def exp_of(self, index):
        """Compute power of generator in multiplicative group."""
        return self.cyclic_group_dict()[index]

    # =========================

    def order_of(self, element):
        """Compute order of element of multiplicative group."""
        if element in self.orders:
            return self.orders[element]

        if self._generator is not None:
            order = self.euler() // gcd(self.log_of(element), self.euler())
            self.orders[element] = order
            return order

        elem = self.elem(element)
        powers = {1: elem}
        for p in self.carmichael_primes():
            new_powers = {
                p * e: self.power_of(x, p)
                for e, x in powers.items()
                if p * e not in powers.keys()
            }
            try:
                order = min(e for e, x in new_powers.items() if x == 1)
                self.orders[element] = order
                return order

            except ValueError:
                powers = {**powers, **new_powers}

    # -------------------------

    def cyclic_subgroup_from(self, element):
        """Compute subgroup generated by element of multiplicative group."""
        subgroup = {0: 1}
        curr_elem = element
        curr_power = 1
        while curr_elem != 1:
            subgroup[curr_power] = curr_elem
            curr_elem = self.mult(curr_elem, element)
            curr_power += 1

        if element not in self.orders:
            self.orders[element] = curr_power

        return subgroup
