
#   ~/itscomputers/algebraic_extensions.py

from approximation import *
from root_D import *

############################################################

##  first, Z[ gamma ] where gamma is a root of x^3 - x^2 - x - 1
##  an element A = [ a0, a1, a2 ] means a0 + a1*gamma + a2*gamma^2

def multiply( A, B ):
    a0, a1, a2 = A
    b0, b1, b2 = B
    
    ab0 = a0*b0 + a1*b2 + a2*b1 + a2*b2
    ab1 = a0*b1 + a1*b0 + a1*b2 + a2*b1 + 2*a2*b2
    ab2 = a0*b2 + a1*b1 + a2*b0 + a1*b2 + a2*b1 + 2*a2*b2

    return [ ab0, ab1, ab2 ]

def power( A, n ):
    if n == 0:
        return [1, 0, 0]
    elif n == 1:
        return A
    elif n % 2 == 0:
        return power( multiply(A,A), n//2 )
    else:
        return multiply( A, power( multiply(A,A), n//2 ) )

def stairs( n ):

    a, b, c, d = 1, -1, -1, -1
    delta0 = b**2 - 3*a*c
    delta1 = 2*(b**3) - 9*a*b*c + 27*(a**2)*d
    delta = 18*a*b*c*d - 4*(b**3)*d + (b**2)*(c**2) -\
                4*a*(c**3) - 27*(a**2)*(d**2)

    assert( delta1**2 - 4*(delta0**3) == -27*(a**2)*delta )

    C = sqrt( (delta1 +\
                3*a*sqrt( -3*delta, precision='Decimal' ) )\
                / 2, 3, precision='Decimal' )

    sqrt3 = sqrt(3, precision='Decimal', digits=26)
    R = C / 2 + 2 / C
    S = (C / 2 - 2 / C) * sqrt3

    gamma = (1 - 2*R) / 3
    beta_real = (1 + R) / 3
    beta_imag = -S / 3
    beta = [ beta_real, beta_imag ]



    gamma1_squared = gamma1**2
    gamma2 = [ gamma2_real, gamma2_imag ]
    gamma2_squared = QuadraticRing(-1).power( gamma2, 2 )
    gamma3 = [ gamma3_real, gamma3_imag ]
    gamma3_squared = QuadraticRing(-1).power( gamma3, 2 )

    g1 = [1, gamma1, gamma1_squared]
    g2 = [1, gamma2[0], gamma2_squared[0]]
    g3 = [1, gamma3[0], gamma3_squared[0]]

#   c1 = (1 - 2 / R) / 3
#   c2 = (1 + 1 / R) / 3
#   c3 = (1 + 1 / R) / 3

    c1_denom = gamma1_squared\
                - 2*gamma1*gamma2_real\
                - (gamma2_real**2 + gamma2_imag**2)

    c1 = gamma1_squared / c1_denom

#   return [g1, g2, g3, c1, c2, c3, C, R, S]

    gamma = [0, 1, 0]
    gamma_n = power( gamma, n )

    c1g1 = c1 * sum( g1[i] * gamma_n[i] for i in range(3) )
#   c2g2 = c2 * sum( g2[i] * gamma_n[i] for i in range(3) )
#   c3g3 = c3 * sum( g3[i] * gamma_n[i] for i in range(3) )

    return round(c1g1)
    return c1g1 + c2g2 + c3g3


    
def rstairs( n ):
    result = [1, 1, 2]
    if n < 3:
        return result[n]
    while len(result) < n+1:
        result.append( result[-1] + result[-2] + result[-3] )
    return result[n]
