#   numth/factorization/quadratic_sieve.py
#===========================================================
from functools import reduce

from ..basic import gcd, integer_sqrt
from ..factorization import factor_trivial
#===========================================================

def rational_sieve_gen(number, prime_base):
    s = RationalSieve(number, prime_base)
    while True:
        curr_size = s.size
        while curr_size == s.size:
            s.add_new_row()
        if set(s.last_row.reduced) == set([0]):
            yield s.relation_to_divisors(s.last_row.relation)
        else:
            yield (1, 1)

#-----------------------------

def rational_sieve(number, prime_base):
    s = RationalSieve(number, prime_base)
    while True:
        curr_size = s.size
        while curr_size == s.size:
            s.add_new_row()
        if set(s.last_row.reduced) == set([0]):
            d, D = s.relation_to_divisors(s.last_row.relation)
            if (1 < d < number):
                return d, D

#=============================

def add(*vectors):
    return list(map(sum, zip(*vectors)))

#-----------------------------

def add_mod_2(*vectors):
    """Add two arrays modulo 2."""
    return list(map(
        lambda t: reduce(
            lambda x, y: (x + y) % 2,
            t,
            0
        ),
        zip(*vectors)
    ))

#===========================================================

class SieveRow:

    def __init__(self, number, vector, place):
        self.number = number
        self.vector = vector
        self.reduced = [x % 2 for x in vector]
        self.relation = [0] * (place - 1) + [1]
        self.pivot = None

    #-------------------------

    def __repr__(self):
        return '{} : {} : {} : {}'\
            .format(self.number, self.vector, self.reduced, self.relation)

    #-------------------------

    def can_reduce_from(self, other):
        return other.pivot is not None and self.reduced[other.pivot] == 1

    #-------------------------

    def reduce_from(self, other):
        self.reduced = add_mod_2(self.reduced, other.reduced)
        self.relation = add_mod_2(self.relation, other.relation)

    #-------------------------

    def get_pivot(self):
        try:
            self.pivot = self.reduced.index(1)
        except ValueError:
            pass

    #-------------------------

    def can_use_to_reduce(self, other):
        return self.pivot is not None \
            and other.pivot is not None \
            and other.pivot < self.pivot \
            and other.reduced[self.pivot] == 1

    #-------------------------

    def use_to_reduce(self, other):
        if self.can_use_to_reduce(other):
            other.reduce_from(self)

#===========================================================

class RationalSieve:

    def __init__(self, modulus, prime_base):
        self.modulus = modulus
        self.start = integer_sqrt(modulus)
        self.prime_base = prime_base
        self.rows = []
        self.last_row = None
        self.index = 0
        self.size = 1

    #-------------------------

    def __repr__(self):
        return '\n'.join(map(repr, self.rows))

    #-------------------------

    def sieve_row_from(self, number):
        remaining, factorization = factor_trivial(
            pow(number, 2, self.modulus),
            self.prime_base
        )
        
        if remaining != 1:
            return None

        vector = []
        for p in self.prime_base:
            if p in factorization:
                vector.append(factorization[p])
            else:
                vector.append(0)
        
        return SieveRow(number, vector, self.size)

    #-------------------------

    def add_new_row(self):
        self.index = self.index + 1
        number = self.start + self.index
        new_row = self.sieve_row_from(number)
        
        if new_row is None:
            return None

        self.size = self.size + 1
        for row in self.rows:
            row.relation = row.relation + [0]

        for row in self.rows:
            if new_row.can_reduce_from(row):
                new_row.reduce_from(row)

        new_row.get_pivot()

        for row in self.rows:
            if new_row.can_use_to_reduce(row):
                new_row.use_to_reduce(row)

        self.rows = self.rows + [new_row]
        self.last_row = new_row

    #-------------------------

    def relation_rows(self, relation):
        return [self.rows[i] for i, x in enumerate(relation) if x == 1]

    #-------------------------

    def relation_to_sqrts(self, relation):
        rows = self.relation_rows(relation)
        first = reduce(lambda x, y: x * y, map(lambda r: r.number, rows), 1)
        vector_sum = add(*map(lambda r: r.vector, rows))
        second = reduce(
            lambda x, y: x * y, 
            map(
                lambda x: x[0]**(x[1]//2),
                zip(self.prime_base, vector_sum)
            ),
            1
        )
        return first, second

    #-------------------------

    def relation_to_divisors(self, relation):
        s, t = self.relation_to_sqrts(relation)
        return [gcd(x, self.modulus) for x in (s - t, s + t)]

