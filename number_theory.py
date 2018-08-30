
#   ~/itscomputers/number_theory/number_theory.py

from random import randint
from random import choice

import modular as mod
import primality as pr
import factorization as fac

##############################

def div( a, b, method=None ):
    """division algorithm
    (a, b) -> [q, r] 
    with a = q*b + r and 0 <= r < |b|"""
    
    if b > 0 or a == 0:
        q, r = a // b, a % b
    else:
        q, r = a // b + 1, (a % b) + abs(b)
    
    if (method == 'small remainder') and (r > abs(b) // 2):
        q += b // abs(b)
        r -= abs(b)

    return [ q, r ]

##############################

def euclidean_algorithm( a, b, method=None ):
    """euclidean algorithm 
    (a, b) -> prints (a = q*b + r), b -> a, r -> b until r == 0
    optional 3rd argument div2"""
    
    q, r = div( a, b, method )
    print( a, '=', q, '*', b, '+', r )
    if r == 0:
        print()
    else:
        euclidean_algorithm( b, r, method )

##############################

def gcd( a, b ):
    """greatest common divisor
    (a, b) -> d 
    where d is largest positive integer such that d|a and d|b"""
    
    if [a, b] == [0, 0]:
        raise ValueError( 'gcd(0,0) is undefined' )
    if b == 0:
        return abs(a)
    else:
        return gcd( b, div( a, b, method='small remainder' )[1] )

##############################

def bezout( a, b ):
    """bezout lemma: there exists x, y such that ax + by = gcd(a,b)
    (a, b) -> [x, y] where ax + by = gcd(a,b)"""

    if [ a, b ] == [ 0, 0 ]:
        raise ValueError( 'gcd(0,0) is undefined' )

    if a % b == 0:
        if b > 0:
            return [ 0, 1 ]
        elif b < 0:
            return [ 0, -1 ]
    
    elif b % a == 0:
        if a > 0:
            return [ 1, 0 ]
        elif a < 0:
            return [ -1, 0 ]
    
    else:
        _a, _b = a, b
        q, r = div(_a,_b)
        x, y = 1, -q
        _a, _b = _b, r
        _q, _r = div(_a,_b)
        _x, _y = -_q, q*_q + 1
        
        while a*_x + b*_y != 0:
            q, r = _q, _r
            _a, _b = _b, r
            _q, _r = div(_a,_b)
            x, _x = _x, (x - _q*_x)
            y, _y = _y, (y - _q*_y)
        
        if a*x + b*y > 0:
            return [ x, y ]
        else:
            return [ -x, -y ]

##############################

def padic( a, p ):
    """p-adic representation of a number
    a -> [e, b] where a == p^e * b"""

    if p < 2:
        raise ValueError( 'p-adic base must be at least 2' )

    e = 0
    while a % p == 0:
        e += 1
        a //= p
    
    return [ e, a ]

##############################

