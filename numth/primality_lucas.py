#   numth/primality_lucas.py
#===========================================================
from random import randint

from .basic import gcd, is_square, jacobi, padic
from .quadratic import Quadratic
from .rational import Rational
#===========================================================

def lucas_witness_pair(number, P, Q):
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

    U, V, Q_k = _by_index(d, P, Q, number)
    if U == 0:
        strong = True

    for j in range(s - 1):
        U, V, Q_k = _double_index(U, V, Q_k, number)
        if V == 0:
            strong = True

    U, V, Q_ = _double_index(U, V, Q_k, number)
    if U == 0:
        if _trivially_composite(V, Q, Q_k, number, delta):
            return 'composite', False

        return 'probable prime', strong

    return 'composite', False

#-----------------------------

def lucas_witness_pairs(number, witness_pairs):
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

def lucas_test(number, num_witnesses):
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

def _generate_witness_pairs(number, num_witnesses):
    witnesses = set()

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

def _good_parameters(number, P, Q, D):
    for d in (gcd(P, number), gcd(Q, number), gcd(D, number)):
        if d == number:
            return False
        if d > 1:
            return d
    return True

#-----------------------------

def _trivially_composite(V, Q, Q_power, number, delta):
    if delta == number + 1:
        if V != (2*Q) % number:
            return True
        if Q_power != (Q * jacobi(Q, number)) % number:
            return True
    else:
        if Q_power != jacobi(Q, number) % number:
            return True

    return False

#=============================

def _double_index(U, V, Q_k, mod):
    return (U*V) % mod, (V*V - 2*Q_k) % mod, pow(Q_k, 2, mod)

#-----------------------------

def _index_plus_one(U, V, Q_k, P, Q, mod):
    return (
        ((P*U + V) * (mod + 1) // 2) % mod,
        (((P**2 - 4*Q) * U + P*V) * (mod + 1) // 2) % mod,
        (Q_k * Q) % mod
    )

#-----------------------------

def _by_index(k, P, Q, mod):
    if k == 0:
        return (0, 2, 1)
    elif k == 1:
        return (1, P % mod, Q % mod)
    elif k % 2 == 0:
        return _double_index(*_by_index(k//2, P, Q, mod), mod)
    else:
        return _index_plus_one(*_by_index(k-1, P, Q, mod), P, Q, mod)

#=============================

def _get_quadratic_element(P, D, modulus):
    imag = ((modulus + 1) // 2) % modulus
    real = (P * imag) % modulus
    return Quadratic(real, imag, D)

#-----------------------------

def _extract_from_quadratic(quadratic_element, modulus):
    U = (2 * quadratic_element.imag) % modulus
    V = (2 * quadratic_element.real) % modulus
    return U, V

#=============================

def _lucas_sequence(P, Q, mod):
    U_, V_, Q_ = (0, 2, 1)
    yield (U_, V_, Q_)

    U__, V__, Q__ = (1, P % mod, Q % mod)
    yield (U__, V__, Q__)

    while True:
        U_, U__ = U__, (P*U__ - Q*U_) % mod
        V_, V__ = V__, (P*V__ - Q*V_) % mod
        Q_, Q__ = Q__, (Q * Q__) % mod
        yield(U__, V__, Q__)
