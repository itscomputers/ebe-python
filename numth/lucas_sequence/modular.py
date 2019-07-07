#   numth/modular/lucas_sequence.py
#===========================================================

def term_zero(P, Q, modulus):
    return (0, 2, 1)

def term_one(P, Q, modulus):
    return (1, P % modulus, Q % modulus)

def next_term(prev, curr, P, Q, modulus):
    U, V = map(lambda x, y: (P * x - Q * y) % modulus, curr[:2], prev[:2])
    return (U, V, (Q * curr[2]) % modulus)

def lucas_sequence_gen(P, Q, modulus):
    prev = term_zero(P, Q, modulus)
    yield prev

    curr = term_one(P, Q, modulus)

    while True:
        yield curr
        prev, curr = curr, next_term(prev, curr, P, Q, modulus)

def double_index(U_k, V_k, Q_k, modulus):
    U = (U_k * V_k) % modulus
    V = (V_k * V_k - 2 * Q_k) % modulus
    
    return U, V, pow(Q_k, 2, modulus)

def index_plus_one(U_k, V_k, Q_k, P, Q, modulus):
    U = ((P*U_k + V_k) * (modulus + 1) // 2) % modulus
    V = (((P**2 - 4*Q) * U_k + P*V_k) * (modulus + 1) // 2) % modulus

    return U, V, (Q_k * Q) % modulus

def by_index(k, P, Q, modulus):
    if k == 0:
        return term_zero(P, Q, modulus)
    elif k == 1:
        return term_one(P, Q, modulus)
    elif k % 2 == 0:
        return double_index(*by_index(k // 2, P, Q, modulus), modulus)
    else:
        return index_plus_one(*by_index(k - 1, P, Q, modulus), P, Q, modulus)

