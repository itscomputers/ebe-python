#   numth/primality/lucas.py
#===========================================================
from random import randint
from typing import Set, Tuple, Union

from ..basic import gcd, is_square, jacobi, padic
from ..lucas_sequence import (
    lucas_sequence_by_index,
    lucas_sequence_double_index
)
#===========================================================

def lucas_witness_pair(number: int, P: int, Q: int) -> Tuple[str, bool]:
    """
    Lucas sequence witness for primality.

    Determines if number is composite or probably prime, 
    according to a witness pair.

    params
    + number : int
    + P : int
    + Q : int

    return
    (primality, strong) : (str, bool)
        * ('composite', _) means number is composite
        * ('probable prime', false) means P, Q think number is prime
        * ('probable prime', true) means P, Q strongly think number is priem
    """
    D = P**2 - 4*Q

    valid = _good_parameters(number, P, Q, D)
    if valid is False:
        raise ValueError('Bad parameters')
    if type(valid) is int:
        return 'composite', False

    delta = number - jacobi(D, number)
    s, d = padic(delta, 2)
    strong = False

    U, V, Q_k = lucas_sequence_by_index(d, P, Q, number)
    if U == 0:
        strong = True

    for j in range(s - 1):
        U, V, Q_k = lucas_sequence_double_index(U, V, Q_k, number)
        if V == 0:
            strong = True

    U, V, Q_ = lucas_sequence_double_index(U, V, Q_k, number)
    if U == 0:
        if _trivially_composite(number, delta, V, Q, Q_k):
            return 'composite', False

        return 'probable prime', strong

    return 'composite', False

#-----------------------------

def lucas_witness_pairs(
        number: int,
        witness_pairs: Set[Tuple[int, int]]
    ) -> Tuple[str, bool]:
    """
    Combination of Lucas sequence witnesses for primality

    params
    + number : int
    + witness_pairs : iterable of witness pairs

    return
    (primality, strong) : (str, bool)
        * ('composite', _) if any pair thinks number is composite
        * ('probable prime', false) if all pairs think number is probable prime
        * ('probable prime', true) if all pairs think number is probable prime
        with at least one strong opinion
    """
    strong = False
    for pair in witness_pairs:
        primality, witness_strong = lucas_witness_pair(number, *pair)
        if primality == 'composite':
            return 'composite', False
        if witness_strong:
            strong = True
    
    return 'probable prime', strong

#-----------------------------

def lucas_test(number: int, num_witnesses: int) -> str:
    """
    Lucas test for primality.

    Probabilistic primality test using Lucas sequences.

    params
    + number : int
    + num_witnesses : int

    return
    str
        * 'composite' is deterministic
        * 'probable prime' and 'strong probable prime' are probabilistic
        and incorrect with probability < (4/15) ** num_witnesses
    """
    if number < 3:
        raise ValueError('Number should be at least 3')
    if number % 2 == 0:
        return 'composite'
    
    witness_pairs = _generate_witness_pairs(number, num_witnesses)
    primality, strong = lucas_witness_pairs(number, witness_pairs)
    
    if primality == 'composite' or strong is False:
        return primality

    return 'strong probable prime'

#=============================

def _generate_witness_pairs(
        number: int,
        num_witnesses: int
    ) -> Set[Tuple[int, int]]:
    """Generate witness pairs for primality testing."""
    witnesses = set()       # type: Set[Tuple[int, int]]

    if not is_square(number):
        D = 5
        sgn = 1
        while len(witnesses) < num_witnesses // 2 + 1:
            if jacobi(D * sgn, number) == -1:
                witnesses = witnesses | set([(1, (1 - D * sgn) // 4)])
            D += 2
            sgn *= -1

    while len(witnesses) < num_witnesses:
        P = randint(1, 100*num_witnesses)
        Q = randint(1, 100*num_witnesses)
        if P % number != 0 and Q % number != 0 and (P**2 - 4*Q) % number != 0:
            witnesses = witnesses | set([(P, Q)])

    return witnesses

#=============================

def _good_parameters(
        number: int,
        P: int,
        Q: int,
        D: int
    ) -> Union[bool, int]:
    """Determines if parameters are good or if trivial factor is present."""
    for d in (gcd(P, number), gcd(Q, number), gcd(D, number)):
        if d == number:
            return False
        if d > 1:
            return d
    return True

#-----------------------------

def _trivially_composite(
        number: int,
        delta: int,
        V: int,
        Q: int,
        Q_power: int
    ) -> bool:
    """Computes is number is composite using calculated values."""
    if delta == number + 1:
        if V != (2*Q) % number:
            return True
        if Q_power != (Q * jacobi(Q, number)) % number:
            return True
    else:
        if Q_power != jacobi(Q, number) % number:
            return True

    return False

