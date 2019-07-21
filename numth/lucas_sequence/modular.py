#   numth/lucas_sequence/modular.py
#===========================================================

def lucas_sequence_gen(P, Q, modulus):
    """
    Generator for Lucas sequence triple modulo given modulus.

    Produces sequences U_k, V_k
        * both satifying `next = P * curr - Q * prev`
        * U_0, U_1 = 0, 1
        * V_0, V_1 = 2, P
    and sequence Q_k = Q**k % modulus.

    params
    + P : int
    + Q : int
    + modulus : int
        must be > 1

    return
    generator
    """
    prev = _term_zero(P, Q, modulus)
    yield prev

    curr = _term_one(P, Q, modulus)

    while True:
        yield curr
        prev, curr = curr, _next_term(prev, curr, P, Q, modulus)

#=============================

def by_index(k, P, Q, modulus):
    """
    Compute kth terms of Lucas sequence triple modulo given modulus.

    params
    + k : int
    + P : int
    + Q : int
    + modulus : int
        P, Q, modulus are Lucas sequence params

    return
    (U_k, V_k, Q_k) : tuple
    """
    if k == 0:
        return _term_zero(P, Q, modulus)
    elif k == 1:
        return _term_one(P, Q, modulus)
    elif k % 2 == 0:
        return double_index(*by_index(k // 2, P, Q, modulus), modulus)
    else:
        return index_plus_one(*by_index(k - 1, P, Q, modulus), P, Q, modulus)

#-----------------------------

def double_index(U_k, V_k, Q_k, modulus):
    """
    Given kth elements of Lucas sequence triple, produces (2k)th elements.

    params
    + U_k : int
    + V_k : int
    + Q_k : int
    + modulus : int
        modulus is from Lucas sequence params

    return
    (U_2k, V_2k, Q_2k) : tuple
    """
    U = (U_k * V_k) % modulus
    V = (V_k * V_k - 2 * Q_k) % modulus
    
    return U, V, pow(Q_k, 2, modulus)

#-----------------------------

def index_plus_one(U_k, V_k, Q_k, P, Q, modulus):
    """
    Given kth elements of Lucas sequence triple, produces next elements.

    params
    + U_k : int
    + V_k : int
    + Q_k : int
    + P : int
    + Q : int
    + modulus : int
        P, Q, modulus are Lucas sequence params

    return
    (U_k1, V_k1, Q_k1) : tuple
    """
    U = ((P*U_k + V_k) * (modulus + 1) // 2) % modulus
    V = (((P**2 - 4*Q) * U_k + P*V_k) * (modulus + 1) // 2) % modulus

    return U, V, (Q_k * Q) % modulus

#===========================================================

def _term_zero(P, Q, modulus):
    return (0, 2, 1)

def _term_one(P, Q, modulus):
    return (1, P % modulus, Q % modulus)

def _next_term(prev, curr, P, Q, modulus):
    U, V = map(lambda x, y: (P * x - Q * y) % modulus, curr[:2], prev[:2])
    return (U, V, (Q * curr[2]) % modulus)

