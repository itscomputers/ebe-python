
#   numth/numth.py

##############################

def div(num, div, SMALL_REM=False):
    """
    Division algorithm.

    Args:   int:    num, div        div != 0
            bool:   SMALL_REM       True -> |r| <= |div|/2
                                    False -> 0 <= r < |div|

    Return: int:    q, r            a == q * b + r
    """
    if div == 0:
        raise ValueError('Attempted division by zero')
    
    if div > 0 or num == 0:
        q, r = num//div, num%div
    else:
        q, r = num//div + 1, (num%div) + abs(div)

    if (SMALL_REM) and (r > abs(div)//2):
        q += div // abs(div)
        r -= abs(div)

    return q, r

##############################

def euclidean_algorithm(a, b, SMALL_REM=False):
    """
    Euclidean algorithm.
    
    Args:   int:    a, b        b != 0

    Return: None:   prints a = q * b + r until r == 0
    """
    q, r = div(a, b, METHOD)
    print('{} = {} * {} + {}'.format(a, q, b, r))
    if r != 0:
        euclidean_algorithm(b, r, METHOD)

##############################

def gcd(a, b):
    """
    Greatest common divisor.
    
    Args:   int:    a, b        (a, b) != (0, 0)

    Return: int:    largest positive integer dividing a and b
    """
    if (a, b) == (0, 0):
        raise ValueError('gcd(0, 0) is undefined')
    while b != 0:
        a, b = b, a%b
    return abs(a)

##############################

def lcm(a, b):
    """
    Least common multiple.
    
    Args:   int:    a, b        a * b != 0

    Return: int:    (smallest positive integer divisible by a and b)
    """
    if a * b == 0:
        raise ValueError('lcm(_,0) is undefined')
    
    return abs(a // gcd(a, b) * b)

##############################

def bezout(a, b):
    """
    Integer solution to Bezout's lemma.

    Args:   int:    a, b        (a, b) != (0, 0)

    Return: int:    x, y        a*x + b*y == gcd(a,b)
    """
    if (a, b) == (0, 0):
        raise ValueError('gcd(0, 0) is undefined')

    if b == 0:
        if a > 0:
            return 1, 0
        else:
            return -1, 0

    a_, b_ = a, b
    q, r = div(a_, b_, METHOD='SMALL')
    xx, x = 0, 1
    yy, y = 1, -q

    while r != 0:
        a_, b_ = b_, r
        q, r = div(a_, b_, METHOD='SMALL')
        xx, x = x, -q*x + xx
        yy, y = y, -q*y + yy

    if a*xx + b*yy > 0:
        return xx, yy
    else:
        return -xx, -yy
        
##############################

def padic(num, base):
    """
    p-adic representation.

    Args:   int:    num, base       base > 1

    Return: int:    exp, rest       num == (base**exp) * rest
                                    rest % base != 0
    """
    if base < 2:
        raise ValueError('p-adic base must be at least 2')

    exp = 0
    rest = num
    while rest % base == 0:
        exp += 1
        rest //= base
    return exp, rest

############################################################
############################################################
#       Modular functions
############################################################
############################################################

def mod_inverse(num, mod):
    """
    Modular inverse.

    Args:   int:    num, mod        mod > 1
    
    Return: int:    inv             (num * inv) % mod == 1
    """
    if mod < 2:
        raise ValueError('Modulus must be at least 2')
    if gcd(num, mod) != 1:
        raise ValueError('{} is not invertible modulo {}'.format(num, mod))

    return bezout(num, mod)[0] % mod

##############################

def mod_power(num, exp, mod):
    """
    Power of a number relative to a modulus.

    Args:   int:    num, exp, mod       mod > 1
    
    Return: int:    val                 val == (num**exp) % mod
    """
    if mod < 2:
        raise ValueError('Modulus must be at least 2')

    if exp < 0:
        return pow(mod_inverse(num, mod), -exp, mod)
    else:
        return pow(num, exp, mod) 

##############################

def jacobi(a, b):
    """
    Jacobi symbol.

    Args:   int:    a, b        b odd

    Return: int:    val         val in [1, 0, or -1]
    """
    if b % 2 == 0:
        raise ValueError(
                'Jacobi symbol ( {} | {} ) is undefined'.format(num, mod))

    if b == 1:
        return 1
    if gcd(a, b) != 1:
        return 0

    exp, a_ = padic(a % b, 2)
    if (exp % 2 == 1) and (b % 8 in [3, 5]):
        sgn = -1
    else:
        sgn = 1
    if a_ == 1:
        return sgn
    else:
        if (b % 4 != 1) and (a_ % 4 != 1):
            sgn *= -1
        return sgn * jacobi(b, a_)








############################################################
############################################################
############################################################
############################################################
############################################################

##  testing

#############################

if __name__ == '__main__':
    from random import randint, choice
    
    ##########################
    #   test div
    for j in range(10):
        a, b = (choice([-1,1]) * randint(1,10**6) for i in range(2))
        q, r = div(a, b)
        assert( a == q*b + r )
        assert( r < abs(b) )
        q, r = div(a, b, 'SMALL')
        assert( a == q*b + r )
        assert( (r <= abs(b)//2) and (r > -abs(b)//2) )

    #########################
    #   test gcd
    for j in range(10):
        a, b = (choice([-1,1]) * randint(1,10**6) for i in range(2))
        d = gcd(a, b)
        assert( (a%d, b%d) == (0, 0) )
        assert( gcd(a//d, b//d) == 1 )

    ##########################
    #   test lcm
    for j in range(10):
        a, b = (choice([-1,1]) * randint(1,10**6) for i in range(2))
        m = lcm(a, b)
        assert( (m%a, m%b) == (0, 0) )
        assert( gcd(m//a, m//b) == 1 )

    ##########################
    #   test bezout
    for j in range(10):
        a, b = (choice([-1,1]) * randint(1,10**6) for i in range(2))
        x, y = bezout(a, b)
        d = gcd(a, b)
        assert( a*x + b*y == d )

    ##########################
    #   test padic
    for j in range(10):
        num, base = choice([-1,1])*randint(1,10**6), randint(2,10**6)
        exp, rest = padic(num, base)
        assert( num == base**exp * rest )
        assert( rest % base != 0 )

    ##########################
    #   test mod_inverse
    for j in range(10):
        num, mod = choice([-1,1])*randint(1,10**6), randint(2,10**6)
        while gcd(num, mod) != 1:
            num += 1
        inv = mod_inverse(num, mod)
        assert( inv > 0 and inv < mod )
        assert( (num * inv) % mod == 1 )

    ##########################
    #   test mod_power
    for j in range(10):
        num, exp, mod = (randint(1,10**4) for i in range(3))
        ans = mod_power(num, exp, mod)
        assert( (num**exp) % mod == ans )
        if gcd(num, mod) == 1:
            inv = mod_power(num, -exp, mod)
            assert( mod_inverse(ans, mod) == inv )

    ##########################
    #   test jacobi
    jacobi_row_15 = [0,1,1,0,1,0,0,-1,1,0,0,-1,0,-1,-1]
    assert( [jacobi(a, 15) for a in range(15)] == jacobi_row_15 )

