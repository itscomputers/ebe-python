#   numth/modular.py
#===========================================================
from functools import reduce

from ..basic import jacobi, padic
from ..types import Quadratic
#===========================================================

def mod_sqrt(number, prime):
    """
    Square root of a number modulo a prime.

    Computes two sqrts such that each ``sqrt**2 % prime == number``.

    params
    + number : int
    + prime : int
        prime number

    return
    (int, int)
    """
    if prime == 2 or number % prime == 0:
        return (number, number)

    if jacobi(number, prime) != 1:
        raise ValueError('{} is not a square modulo {}'.format(number, prime))

    if prime % 4 == 3:
        return mod_sqrt_when_three_mod_four(number, prime)

    s, q = padic(prime - 1, 2)
    m = len(bin(prime)[2:])

    if s * (s - 1) > 8*m + 20:
        return mod_sqrt_cipolla(number, prime)
    
    return mod_sqrt_tonelli_shanks(number, prime, s, q, m)

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def mod_sqrt_minus_one_wilson(prime):
    """
    Square root of -1 modulo a prime (Wilson's Theorem).

    Computes two sqrts such that each ``sqrt**2 % prime == prime - 1``.

    params
    + prime : int
        prime number

    return
    (int, int)
    """
    if prime == 2:
        return (1, 1)
    
    if prime % 4 == 3:
        raise ValueError('-1 is not a square modulo {}'.format(prime))
    
    val = reduce(lambda x, y: (x * y) % prime, range(2, (prime-1)//2 + 1), 1)
    return tuple(sorted([val, prime - val]))

#-----------------------------

def mod_sqrt_minus_one_legendre(prime):
    """
    Square root of -1 modulo a prime (Legendre's method).

    Computes two sqrts such that each ``sqrt**2 % prime == prime - 1``.

    params
    + prime : int
        prime number

    return
    (int, int)
    """
    if prime == 2:
        return (1, 1)
    
    if prime % 4 == 3:
        raise ValueError('-1 is not a square modulo {}'.format(prime))
    
    for x in range(2, prime-1):
        if jacobi(x, prime) == -1:
            val = pow(x, (prime-1)//4, prime)
    return tuple(sorted([val, prime - val]))

#-----------------------------

def mod_sqrt_when_three_mod_four(number, prime):
    """
    Square root of a number modulo a prime congruent to 3 modulo 4.

    Computes two sqrts such that each ``sqrt**2 % prime == number``.

    params
    + number : int
    + prime : int
        prime number % 4 == 3

    return
    (int, int)

    """
    if prime % 4 != 3:
        raise ValueError('Use a different mod_sqrt function')

    val = pow(number, (prime+1)//4, prime)
    return tuple(sorted([val, prime - val]))

#-----------------------------

def _tonelli_shanks_helper(m, c, t, val, prime):
    _t = t
    for _m in range(1, m):
        _t = pow(_t, 2, prime)
        if _t == 1:
            break

    b = pow(c, 2**(m - _m - 1), prime)
    _c = pow(b, 2, prime)
    _t = (t * _c) % prime
    _val = (val * b) % prime

    return _m, _c, _t, _val

# - - - - - - - - - - - - - -    

def mod_sqrt_tonelli_shanks(number, prime, *params):
    """
    Square root of a number modulo a prime (Tonelli-Shanks algorithm).

    Computes two sqrts such that each ``sqrt**2 % prime == number``.

    params
    + number : int
    + prime : int
        prime number
    + params : list(int)
        s, q, m can be passed in if already computed    

    return
    (int, int)
    """
    if params == ():
        s, q = padic(prime-1, 2)
        m = len(bin(prime)[2:])
    else:
        s, q, m = params

    for z in range(1, prime):
        if jacobi(z, prime) == -1:
            break

    m = s
    c = pow(z, q, prime)
    t = pow(number, q, prime)
    val = pow(number, (q+1)//2, prime)

    while t != 1:
        m, c, t, val = _tonelli_shanks_helper(m, c, t, val, prime)

    return tuple(sorted([val, prime - val]))

#-----------------------------

def mod_sqrt_cipolla(number, prime):
    """
    Square root of a number modulo a prime (Cipolla's algorithm).

    Computes two sqrts such that each ``sqrt**2 % prime == number``.

    params
    + number : int
    + prime : int
        prime number

    return
    (int, int)
    """
    for y in range(2, prime):
        root = (y**2 - number) % prime
        if jacobi(root, prime) == -1:
            break

    val = pow(Quadratic(y, 1, root), (prime+1)//2, prime).real
    return tuple(sorted([val, prime - val]))

