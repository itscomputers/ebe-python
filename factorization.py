
##  ~/itscomputers/number_theory/factorization.py

import number_theory as nt
import modular as mod
import primality as pr

##########################

def pollard( number, seed, const ):
    """find factor using Pollard's rho method
    (a, x0, n) -> factor d of a using the sequence
    x0, x1, x2, ..., where next x is f(x) = x^2 + n"""

    f = lambda x : (x**2 + const) % number

    r = f( seed % number )
    R = f(r)
    d = nt.gcd( R-r, number )

    while d == 1:
        r = f(r)
        R = f( f(R) )
        d = nt.gcd( R-r, number )

    return d

##########################

def find_divisor( number, seeds=[2,3,5,6,8], consts=[1,2,-1] ):
    """find factor using various seeds/polynomials in pollard
    number -> d, where d | number and d > 1"""

    for n in consts:
        for x0 in seeds:
            d = pollard( number, x0, n )
            if d != number:
                return d

    return number

##########################

def factor( number, L=100, seeds=[2,3,5,6,8], consts=[1,2,-1] ):
    """prime factorization
    number -> list of prime factors of number
    (keeps track of nonprime factors that were not factored)"""

    a = abs( number )
    if a < 2:
        return None
    
    result = []
    for prime in pr.prime_range( 2, L ):
        if a % prime == 0:
            e, a = nt.padic( a, prime )
            result += e * [ prime ]
            if a == 1:
                return result 

    unfactored = [ a ]
    bad = []

    while unfactored != []:
        b = unfactored[0]
        unfactored.remove( b )
        if pr.is_prime( b ):
            result.append( b )
        else:
            d = find_divisor(b,seeds,consts)
            if d == b:
                bad.append( b )
                result.append( b )
            else:
                for x in [ d, b//d ]:
                    if pr.is_prime( x ):
                        result.append( x )
                    else:
                        unfactored.append( x )

    if bad != []:
        raise ValueError( 'factorization failed' )

    return result

##########################
            
def multiplicity( number=None, factorization=None ):
    """factorization with multiplicity
    F -> { p1:e1, p2:e2, ... }""" 

    if factorization == None:
        if number == None:
            factorization = []
        else:
            factorization = factor(number)

    return { prime : factorization.count(prime) \
                for prime in sorted( set(factorization) ) }
    
##########################

def print_factorization( number=None, factorization=None ):
    """prints factorization from list of prime divisors
    F -> p1^e1 * p2^e2 * ..."""

    if factorization == None:
        if number == None:
            factorization = []
        else:
            factorization = factor(number)

    result = []
    for prime, exp in sorted( multiplicity(None,factorization).items() ):
        if exp == 1:
            result.append( str(prime) )
        else:
            result.append( str(prime) + '^' + str(exp) )

    return ' * '.join( result )

##########################

def divisors( number=None, factorization=None ):
    """extracts list of divisors from list of prime divisors
    F -> [ d1, d2, ... ]"""

    if factorization == None:
        if number == None:
            factorization = []
        else:
            factorization = factor(number)

    result = [ 1 ]
    for prime in factorization:
        result += [ prime*d for d in result if prime*d not in result ]

    return sorted( result )

##########################


