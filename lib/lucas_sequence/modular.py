#   lib/lucas_sequence/modular.py
#   - module for lucas sequences relative to a modulus

# ===========================================================
__all__ = [
    "lucas_mod_gen",
    "lucas_mod_by_index",
    "lucas_mod_double_index",
]
# ===========================================================


def lucas_mod_gen(P, Q, modulus):
    """
    Generator for `(P, Q)`-Lucas sequence triple relative to `modulus`.

    Produces sequences U_k, V_k
        * both satifying `next = P * curr - Q * prev`
        * U_0, U_1 = 0, 1
        * V_0, V_1 = 2, P
    and sequence Q_k = Q**k % modulus.

    + P: int
    + Q: int
    + modulus: int --at least 2
    ~> Iterator[Tuple[int, int, int]]
    """
    prev = _term_zero(P, Q, modulus)
    curr = _term_one(P, Q, modulus)

    yield prev
    while True:
        yield curr
        prev, curr = curr, _next_term(prev, curr, P, Q, modulus)


# =============================


def lucas_mod_by_index(k, P, Q, modulus):
    """
    Compute `k`th term of `(P, Q)`-Lucas sequence triple relative to `modulus`
    without computing all preceding terms.

    + k: int
    + P: int
    + Q: int
    + modulus: int
    ~> (U_k, V_k, Q_k): Tuple[int, int, int]
    """
    if k == 0:
        return _term_zero(P, Q, modulus)
    elif k == 1:
        return _term_one(P, Q, modulus)
    elif k % 2 == 0:
        return lucas_mod_double_index(*lucas_mod_by_index(k // 2, P, Q, modulus), modulus)
    return lucas_mod_index_plus_one(
        *lucas_mod_by_index(k - 1, P, Q, modulus), P, Q, modulus
    )


# -----------------------------


def lucas_mod_double_index(U_k, V_k, Q_k, modulus):
    """
    Compute `2k`th term of Lucas sequence triple from `k`th term.

    + U_k: int
    + V_k: int
    + Q_k: int
    + modulus: int
    ~> (U_2k, V_2k, Q_2k): Tuple[int, int, int]
    """
    U = (U_k * V_k) % modulus
    V = (V_k * V_k - 2 * Q_k) % modulus

    return U, V, pow(Q_k, 2, modulus)


# -----------------------------


def lucas_mod_index_plus_one(U_k, V_k, Q_k, P, Q, modulus):
    """
    Compute `k+1`th term of Lucas sequence triple from `k`th term.

    + U_k: int
    + V_k: int
    + Q_k: int
    + P: int
    + Q: int
    + modulus: int
    ~> (U_k1, V_k1, Q_k1): Tuple[int, int, int]
    """
    U = ((P * U_k + V_k) * (modulus + 1) // 2) % modulus
    V = (((P ** 2 - 4 * Q) * U_k + P * V_k) * (modulus + 1) // 2) % modulus

    return U, V, (Q_k * Q) % modulus


# ===========================================================


def _term_zero(P, Q, modulus):
    return (0, 2, 1)


def _term_one(P, Q, modulus):
    return (1, P % modulus, Q % modulus)


def _next_term(prev, curr, P, Q, modulus):
    U, V = map(lambda x, y: (P * x - Q * y) % modulus, curr[:2], prev[:2])
    return (U, V, (Q * curr[2]) % modulus)
